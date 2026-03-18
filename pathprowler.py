#!/usr/bin/env python3
"""
Gobuster Pro - Advanced Directory Busting and VHost Scanning Tool
Uses raft medium wordlists for comprehensive enumeration

Features:
- Parallel scanning (dir, files, vhost, dns)
- DNS subdomain enumeration
- Progress tracking and live output
- Multiple output formats (txt, json, csv, html)
- Recursive directory scanning
- Status code filtering
- Smart retry logic
- Comprehensive logging
"""

import subprocess
import argparse
import sys
import os
import json
import csv
import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import time

class GobusterScanner:
    def __init__(self, target, wordlist_dir="/usr/share/wordlists/seclists", threads=50, 
                 timeout=10, status_codes=None, output_format="txt", verbose=False,
                 recursive=False, recursive_depth=3, user_agent=None, cookies=None,
                 proxy=None, delay=0, display_only=False):
        self.target = target.rstrip('/')
        self.wordlist_dir = wordlist_dir
        self.threads = threads
        self.timeout = timeout
        self.status_codes = status_codes or "200,204,301,302,307,401,403"
        self.output_format = output_format
        self.verbose = verbose
        self.recursive = recursive
        self.recursive_depth = recursive_depth
        self.user_agent = user_agent
        self.cookies = cookies
        self.proxy = proxy
        self.delay = delay
        self.display_only = display_only
        
        # Extract domain/IP from target for directory name
        target_name = self._extract_target_name(target)
        self.results_dir = f"pathprowler_{target_name}" if not display_only else None
        
        # Raft medium wordlists
        self.dir_wordlist = os.path.join(wordlist_dir, "Discovery/Web-Content/raft-medium-directories.txt")
        self.file_wordlist = os.path.join(wordlist_dir, "Discovery/Web-Content/raft-medium-files.txt")
        self.dns_wordlist = os.path.join(wordlist_dir, "Discovery/DNS/subdomains-top1million-110000.txt")
        
        # Results storage
        self.all_results = {
            'directories': [],
            'files': [],
            'vhosts': [],
            'subdomains': []
        }
        
        # Create results directory (append counter if exists) - skip if display_only
        if not self.display_only:
            base_dir = self.results_dir
            counter = 1
            while os.path.exists(self.results_dir):
                self.results_dir = f"{base_dir}_{counter}"
                counter += 1
            os.makedirs(self.results_dir, exist_ok=True)
            
            # Setup logging
            self.setup_logging()
        else:
            # Display-only mode: use console logging only
            logging.basicConfig(
                level=logging.DEBUG if self.verbose else logging.INFO,
                format='%(asctime)s [%(levelname)s] %(message)s',
                handlers=[logging.StreamHandler(sys.stdout)]
            )
            logging.info("PathProwler initialized in DISPLAY-ONLY mode (no files will be saved)")
    
    def _extract_target_name(self, target):
        """Extract domain or IP from target URL for directory naming"""
        import re
        from urllib.parse import urlparse
        
        # Parse URL
        parsed = urlparse(target)
        host = parsed.netloc or parsed.path
        
        # Remove port if present
        host = host.split(':')[0]
        
        # Clean up for filesystem (replace dots with underscores for IPs, keep domain as-is)
        # Check if it's an IP address
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', host):
            # IP address - replace dots with underscores
            return host.replace('.', '_')
        else:
            # Domain name - keep as-is but remove invalid chars
            return re.sub(r'[^a-zA-Z0-9.-]', '_', host)
        
    def validate_wordlists(self, check_dns=False):
        """Check if wordlists exist"""
        missing = []
        if not os.path.exists(self.dir_wordlist):
            missing.append(self.dir_wordlist)
        if not os.path.exists(self.file_wordlist):
            missing.append(self.file_wordlist)
        if check_dns and not os.path.exists(self.dns_wordlist):
            missing.append(self.dns_wordlist)
            
        if missing:
            logging.error("Missing wordlists:")
            for wl in missing:
                logging.error(f"    - {wl}")
            logging.info("Install SecLists: git clone https://github.com/danielmiessler/SecLists.git /usr/share/wordlists/seclists")
            return False
        logging.info("All wordlists validated successfully")
        return True
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_file = os.path.join(self.results_dir, "scan.log")
        log_level = logging.DEBUG if self.verbose else logging.INFO
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        logging.info(f"PathProwler initialized. Log file: {log_file}")
    
    def check_gobuster_installed(self):
        """Check if gobuster is installed"""
        try:
            result = subprocess.run(['gobuster', 'version'], capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                logging.info(f"Gobuster found: {version}")
                return True
        except FileNotFoundError:
            logging.error("Gobuster not found. Install: apt install gobuster or go install github.com/OJ/gobuster/v3@latest")
            return False
        return False
    
    def run_gobuster_dir(self, wordlist, output_file, extensions=None, scan_type="dir"):
        """Run gobuster directory enumeration with advanced options"""
        cmd = [
            "gobuster", "dir",
            "-u", self.target,
            "-w", wordlist,
            "-t", str(self.threads),
            "--timeout", f"{self.timeout}s",
            "-k",  # Skip SSL verification
            "-s", self.status_codes,  # Status codes to match
        ]
        
        # Only add output file if not in display-only mode
        if not self.display_only:
            cmd.extend(["-o", output_file])
        
        # Add optional parameters
        if extensions:
            cmd.extend(["-x", extensions])
        
        if self.recursive:
            cmd.extend(["--wildcard", "-R", "-d", str(self.recursive_depth)])
        
        if self.user_agent:
            cmd.extend(["-a", self.user_agent])
        
        if self.cookies:
            cmd.extend(["-c", self.cookies])
        
        if self.proxy:
            cmd.extend(["-p", self.proxy])
        
        if self.delay > 0:
            cmd.extend(["--delay", f"{self.delay}ms"])
        
        if not self.verbose:
            cmd.append("-q")
        
        logging.info(f"Running: {' '.join(cmd)}")
        
        try:
            # Run with real-time output if verbose
            if self.verbose:
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate(timeout=1200)
                returncode = process.returncode
            else:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
                stdout, stderr, returncode = result.stdout, result.stderr, result.returncode
            
            # Parse results (only from file if not display-only)
            if not self.display_only:
                self.parse_gobuster_output(output_file, scan_type)
            else:
                # In display-only mode, parse from stdout
                self.parse_gobuster_output_from_text(stdout, scan_type)
            
            return {
                'success': returncode == 0,
                'output': output_file if not self.display_only else "console",
                'stderr': stderr,
                'stdout': stdout
            }
        except subprocess.TimeoutExpired:
            logging.error(f"Gobuster timed out for {wordlist}")
            return {'success': False, 'output': output_file, 'stderr': 'Timeout'}
        except Exception as e:
            logging.error(f"Error running gobuster: {e}")
            return {'success': False, 'output': output_file, 'stderr': str(e)}
    
    def run_gobuster_vhost(self, wordlist, output_file, domain):
        """Run gobuster vhost enumeration with advanced options"""
        cmd = [
            "gobuster", "vhost",
            "-u", self.target,
            "-w", wordlist,
            "-t", str(self.threads),
            "--timeout", f"{self.timeout}s",
            "-k",
        ]
        
        # Only add output file if not in display-only mode
        if not self.display_only:
            cmd.extend(["-o", output_file])
        
        if domain:
            cmd.extend(["--domain", domain])
        
        if self.user_agent:
            cmd.extend(["-a", self.user_agent])
        
        if self.cookies:
            cmd.extend(["-c", self.cookies])
        
        if not self.verbose:
            cmd.append("-q")
        
        logging.info(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
            
            # Parse results
            if not self.display_only:
                self.parse_gobuster_output(output_file, "vhost")
            else:
                self.parse_gobuster_output_from_text(result.stdout, "vhost")
            
            return {
                'success': result.returncode == 0,
                'output': output_file if not self.display_only else "console",
                'stderr': result.stderr
            }
        except subprocess.TimeoutExpired:
            logging.error("Gobuster vhost timed out")
            return {'success': False, 'output': output_file, 'stderr': 'Timeout'}
        except Exception as e:
            logging.error(f"Error running gobuster vhost: {e}")
            return {'success': False, 'output': output_file, 'stderr': str(e)}
    
    def run_gobuster_dns(self, wordlist, output_file, domain):
        """Run gobuster DNS subdomain enumeration"""
        cmd = [
            "gobuster", "dns",
            "-d", domain,
            "-w", wordlist,
            "-t", str(self.threads),
            "--timeout", f"{self.timeout}s",
        ]
        
        # Only add output file if not in display-only mode
        if not self.display_only:
            cmd.extend(["-o", output_file])
        
        if not self.verbose:
            cmd.append("-q")
        
        logging.info(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
            
            # Parse DNS results
            if not self.display_only:
                self.parse_dns_output(output_file, domain)
            else:
                self.parse_dns_output_from_text(result.stdout, domain)
            
            return {
                'success': result.returncode == 0,
                'output': output_file if not self.display_only else "console",
                'stderr': result.stderr
            }
        except subprocess.TimeoutExpired:
            logging.error("Gobuster DNS timed out")
            return {'success': False, 'output': output_file, 'stderr': 'Timeout'}
        except Exception as e:
            logging.error(f"Error running gobuster DNS: {e}")
            return {'success': False, 'output': output_file, 'stderr': str(e)}
    
    def parse_dns_output(self, output_file, domain):
        """Parse gobuster DNS output and store results"""
        if not os.path.exists(output_file):
            return
        
        with open(output_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Format: Found: subdomain.domain.com [IP: 1.2.3.4]
                # Or just: subdomain.domain.com
                parts = line.split()
                if parts:
                    subdomain = parts[0].replace('Found:', '').strip()
                    
                    # Extract IP if present
                    ip = "N/A"
                    ip_match = re.search(r'\[IP: ([^\]]+)\]', line)
                    if ip_match:
                        ip = ip_match.group(1)
                    elif len(parts) > 1:
                        # Sometimes format is: subdomain.domain.com 1.2.3.4
                        potential_ip = parts[-1]
                        if re.match(r'^\d+\.\d+\.\d+\.\d+$', potential_ip):
                            ip = potential_ip
                    
                    result = {
                        'path': subdomain,
                        'status': 'Found',
                        'size': ip,  # Using size field for IP
                        'full_url': f"http://{subdomain}"
                    }
                    
                    self.all_results['subdomains'].append(result)
    
    def merge_subdomain_results(self):
        """Merge and deduplicate subdomain results from DNS and VHost scans"""
        # Create a set of unique subdomains based on the 'path' field
        seen = set()
        unique_results = []
        
        for result in self.all_results['subdomains']:
            subdomain = result['path']
            if subdomain not in seen:
                seen.add(subdomain)
                unique_results.append(result)
        
        # Update with deduplicated results
        self.all_results['subdomains'] = unique_results
        
        # Save merged results to a combined file (skip if display-only)
        if not self.display_only:
            merged_file = os.path.join(self.results_dir, "subdomains_all.txt")
            with open(merged_file, 'w') as f:
                f.write("# Combined Subdomain Enumeration Results\n")
                f.write(f"# Total Unique Subdomains: {len(unique_results)}\n")
                f.write("# Format: subdomain | IP | Source\n\n")
                
                for result in sorted(unique_results, key=lambda x: x['path']):
                    f.write(f"{result['path']} | {result['size']} | {result['status']}\n")
            
            logging.info(f"Merged results saved to: {merged_file}")
        else:
            logging.info(f"Merged {len(unique_results)} unique subdomains (display-only mode)")
    
    def parse_gobuster_output(self, output_file, scan_type):
        """Parse gobuster output and store results"""
        if not os.path.exists(output_file):
            return
        
        with open(output_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Parse different output formats
                # Format: /path (Status: 200) [Size: 1234]
                match = re.search(r'(\S+)\s+\(Status: (\d+)\)', line)
                if match:
                    path, status = match.groups()
                    size_match = re.search(r'\[Size: (\d+)\]', line)
                    size = size_match.group(1) if size_match else "N/A"
                    
                    result = {
                        'path': path,
                        'status': status,
                        'size': size,
                        'full_url': f"{self.target}{path}" if scan_type != "vhost" else path
                    }
                    
                    if scan_type == "dir":
                        self.all_results['directories'].append(result)
                    elif scan_type == "files":
                        self.all_results['files'].append(result)
                    elif scan_type == "vhost":
                        self.all_results['vhosts'].append(result)
                    elif scan_type == "dns":
                        self.all_results['subdomains'].append(result)
    
    def parse_gobuster_output_from_text(self, text, scan_type):
        """Parse gobuster output from text/stdout for display-only mode"""
        for line in text.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Parse different output formats
            # Format: /path (Status: 200) [Size: 1234]
            match = re.search(r'(\S+)\s+\(Status: (\d+)\)', line)
            if match:
                path, status = match.groups()
                size_match = re.search(r'\[Size: (\d+)\]', line)
                size = size_match.group(1) if size_match else "N/A"
                
                result = {
                    'path': path,
                    'status': status,
                    'size': size,
                    'full_url': f"{self.target}{path}" if scan_type != "vhost" else path
                }
                
                # Print result immediately in display-only mode
                logging.info(f"[{scan_type.upper()}] {path} (Status: {status}) [Size: {size}]")
                
                if scan_type == "dir":
                    self.all_results['directories'].append(result)
                elif scan_type == "files":
                    self.all_results['files'].append(result)
                elif scan_type == "vhost":
                    self.all_results['vhosts'].append(result)
    
    def parse_dns_output_from_text(self, text, domain):
        """Parse gobuster DNS output from text/stdout for display-only mode"""
        for line in text.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Format: Found: subdomain.domain.com [IP: 1.2.3.4]
            parts = line.split()
            if parts:
                subdomain = parts[0].replace('Found:', '').strip()
                
                # Extract IP if present
                ip = "N/A"
                ip_match = re.search(r'\[IP: ([^\]]+)\]', line)
                if ip_match:
                    ip = ip_match.group(1)
                elif len(parts) > 1:
                    potential_ip = parts[-1]
                    if re.match(r'^\d+\.\d+\.\d+\.\d+$', potential_ip):
                        ip = potential_ip
                
                result = {
                    'path': subdomain,
                    'status': 'Found',
                    'size': ip,
                    'full_url': f"http://{subdomain}"
                }
                
                # Print result immediately in display-only mode
                logging.info(f"[DNS] {subdomain} -> {ip}")
                
                self.all_results['subdomains'].append(result)
    
    def scan_directories(self, extensions=None):
        """Scan for directories using raft medium directories wordlist"""
        logging.info(f"Starting directory enumeration on {self.target}")
        logging.info(f"Wordlist: {self.dir_wordlist}")
        logging.info(f"Threads: {self.threads}")
        logging.info(f"Status codes: {self.status_codes}")
        
        output_file = os.path.join(self.results_dir, "directories.txt") if not self.display_only else "/dev/null"
        start_time = time.time()
        
        result = self.run_gobuster_dir(self.dir_wordlist, output_file, extensions, "dir")
        
        elapsed = time.time() - start_time
        
        if result['success']:
            logging.info(f"Directory scan completed in {elapsed:.2f}s: {result['output']}")
            self.display_results(result['output'])
        else:
            logging.error(f"Directory scan failed: {result['stderr']}")
        
        return result
    
    def scan_files(self, extensions="php,html,txt,asp,aspx,jsp,js,json,xml,bak,old,zip,tar,gz"):
        """Scan for files using raft medium files wordlist"""
        logging.info(f"Starting file enumeration on {self.target}")
        logging.info(f"Wordlist: {self.file_wordlist}")
        logging.info(f"Extensions: {extensions}")
        logging.info(f"Threads: {self.threads}")
        
        output_file = os.path.join(self.results_dir, "files.txt") if not self.display_only else "/dev/null"
        start_time = time.time()
        
        result = self.run_gobuster_dir(self.file_wordlist, output_file, extensions, "files")
        
        elapsed = time.time() - start_time
        
        if result['success']:
            logging.info(f"File scan completed in {elapsed:.2f}s: {result['output']}")
            self.display_results(result['output'])
        else:
            logging.error(f"File scan failed: {result['stderr']}")
        
        return result
    
    def scan_vhosts(self, domain=None, wordlist=None):
        """Scan for virtual hosts"""
        if not wordlist:
            wordlist = os.path.join(self.wordlist_dir, "Discovery/DNS/subdomains-top1million-5000.txt")
        
        logging.info(f"Starting vhost enumeration on {self.target}")
        logging.info(f"Wordlist: {wordlist}")
        logging.info(f"Threads: {self.threads}")
        
        output_file = os.path.join(self.results_dir, "vhosts.txt") if not self.display_only else "/dev/null"
        start_time = time.time()
        
        result = self.run_gobuster_vhost(wordlist, output_file, domain)
        
        elapsed = time.time() - start_time
        
        if result['success']:
            logging.info(f"VHost scan completed in {elapsed:.2f}s: {result['output']}")
            self.display_results(result['output'])
        else:
            logging.error(f"VHost scan failed: {result['stderr']}")
        
        return result
    
    def scan_dns(self, domain=None, wordlist=None, include_vhost=True):
        """Scan for DNS subdomains with optional VHost enumeration"""
        if not domain:
            logging.error("Domain required for DNS scanning")
            return {'success': False, 'output': None, 'stderr': 'No domain provided'}
        
        if not wordlist:
            wordlist = self.dns_wordlist
        
        logging.info("="*60)
        logging.info("SUBDOMAIN ENUMERATION")
        logging.info("="*60)
        logging.info(f"Target Domain: {domain}")
        logging.info(f"Techniques: DNS Resolution" + (" + VHost Scanning" if include_vhost else ""))
        logging.info(f"Wordlist: {wordlist}")
        logging.info(f"Threads: {self.threads}")
        logging.info("="*60)
        
        results = {'dns': None, 'vhost': None}
        
        # Run DNS enumeration
        logging.info("\n[1/2] Starting DNS resolution-based enumeration...")
        output_file_dns = os.path.join(self.results_dir, "subdomains_dns.txt") if not self.display_only else "/dev/null"
        start_time = time.time()
        
        result_dns = self.run_gobuster_dns(wordlist, output_file_dns, domain)
        elapsed_dns = time.time() - start_time
        
        if result_dns['success']:
            logging.info(f"✓ DNS enumeration completed in {elapsed_dns:.2f}s")
            self.display_results(output_file_dns)
            results['dns'] = result_dns
        else:
            logging.error(f"✗ DNS enumeration failed: {result_dns['stderr']}")
        
        # Run VHost enumeration if enabled
        if include_vhost and self.target:
            logging.info("\n[2/2] Starting VHost-based enumeration...")
            output_file_vhost = os.path.join(self.results_dir, "subdomains_vhost.txt") if not self.display_only else "/dev/null"
            start_time = time.time()
            
            result_vhost = self.run_gobuster_vhost(wordlist, output_file_vhost, domain)
            elapsed_vhost = time.time() - start_time
            
            if result_vhost['success']:
                logging.info(f"✓ VHost enumeration completed in {elapsed_vhost:.2f}s")
                self.display_results(output_file_vhost)
                results['vhost'] = result_vhost
            else:
                logging.error(f"✗ VHost enumeration failed: {result_vhost['stderr']}")
        
        # Merge and deduplicate results
        self.merge_subdomain_results()
        
        logging.info("\n" + "="*60)
        logging.info(f"SUBDOMAIN ENUMERATION COMPLETE")
        logging.info(f"Total unique subdomains found: {len(self.all_results['subdomains'])}")
        logging.info("="*60)
        
        return results
    
    def scan_all_parallel(self, extensions=None, vhost_domain=None, dns_domain=None):
        """Run directory, file, vhost, and DNS scans in parallel"""
        logging.info(f"Starting parallel scans on {self.target}")
        start_time = time.time()
        
        tasks = []
        task_names = []
        
        max_workers = 4 if dns_domain else 3
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all scan tasks
            tasks.append(executor.submit(self.scan_directories, extensions))
            task_names.append("Directory scan")
            
            tasks.append(executor.submit(self.scan_files, extensions or "php,html,txt,asp,aspx,jsp"))
            task_names.append("File scan")
            
            if vhost_domain:
                tasks.append(executor.submit(self.scan_vhosts, vhost_domain))
                task_names.append("VHost scan")
            
            if dns_domain:
                tasks.append(executor.submit(self.scan_dns, dns_domain))
                task_names.append("DNS scan")
            
            # Wait for completion with progress
            for idx, future in enumerate(as_completed(tasks)):
                try:
                    future.result()
                    logging.info(f"✓ {task_names[idx]} completed")
                except Exception as e:
                    logging.error(f"✗ {task_names[idx]} failed: {e}")
        
        elapsed = time.time() - start_time
        logging.info(f"All scans completed in {elapsed:.2f}s")
        
        # Generate summary report
        self.generate_summary_report()
    
    def display_results(self, output_file):
        """Display scan results"""
        # Skip file display in display-only mode (results already printed)
        if self.display_only:
            return
            
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            logging.info(f"\n--- Results from {output_file} ---")
            with open(output_file, 'r') as f:
                lines = [l for l in f.readlines() if l.strip() and not l.startswith('#')]
                for line in lines[:20]:  # Show first 20 results
                    print(line.rstrip())
                if len(lines) > 20:
                    logging.info(f"... and {len(lines) - 20} more results")
                logging.info(f"Total findings: {len(lines)}")
        else:
            logging.warning(f"No results found in {output_file}")
    
    def generate_summary_report(self):
        """Generate comprehensive summary report in multiple formats"""
        logging.info("\n" + "="*60)
        logging.info("PATHPROWLER SCAN SUMMARY")
        logging.info("="*60)
        logging.info(f"Target: {self.target}")
        logging.info(f"Directories found: {len(self.all_results['directories'])}")
        logging.info(f"Files found: {len(self.all_results['files'])}")
        logging.info(f"VHosts found: {len(self.all_results['vhosts'])}")
        logging.info(f"Subdomains found: {len(self.all_results['subdomains'])}")
        if not self.display_only:
            logging.info(f"Results directory: {self.results_dir}")
        else:
            logging.info("Mode: DISPLAY-ONLY (no files saved)")
        logging.info("="*60)
        
        # Save in different formats (skip if display-only)
        if not self.display_only:
            if self.output_format == "json" or self.output_format == "all":
                self.save_json_report()
        
            if self.output_format == "csv" or self.output_format == "all":
                self.save_csv_report()
            
            if self.output_format == "html" or self.output_format == "all":
                self.save_html_report()
    
    def save_json_report(self):
        """Save results in JSON format"""
        json_file = os.path.join(self.results_dir, "results.json")
        report = {
            'target': self.target,
            'timestamp': datetime.now().isoformat(),
            'scan_config': {
                'threads': self.threads,
                'timeout': self.timeout,
                'status_codes': self.status_codes,
                'recursive': self.recursive
            },
            'results': self.all_results
        }
        
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logging.info(f"JSON report saved: {json_file}")
    
    def save_csv_report(self):
        """Save results in CSV format"""
        csv_file = os.path.join(self.results_dir, "results.csv")
        
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Type', 'Path', 'Status', 'Size', 'Full URL'])
            
            for result in self.all_results['directories']:
                writer.writerow(['Directory', result['path'], result['status'], result['size'], result['full_url']])
            
            for result in self.all_results['files']:
                writer.writerow(['File', result['path'], result['status'], result['size'], result['full_url']])
            
            for result in self.all_results['vhosts']:
                writer.writerow(['VHost', result['path'], result['status'], result['size'], result['full_url']])
            
            for result in self.all_results['subdomains']:
                writer.writerow(['Subdomain', result['path'], result['status'], result['size'], result['full_url']])
        
        logging.info(f"CSV report saved: {csv_file}")
    
    def save_html_report(self):
        """Save results in HTML format"""
        html_file = os.path.join(self.results_dir, "results.html")
        
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Gobuster Scan Results - {self.target}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        h1 {{ color: #333; }}
        .summary {{ background: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; background: white; }}
        th {{ background: #4CAF50; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background: #f5f5f5; }}
        .status-200 {{ color: green; font-weight: bold; }}
        .status-301, .status-302 {{ color: orange; font-weight: bold; }}
        .status-403 {{ color: red; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>Gobuster Scan Results</h1>
    <div class="summary">
        <h2>Summary</h2>
        <p><strong>Target:</strong> {self.target}</p>
        <p><strong>Scan Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Directories Found:</strong> {len(self.all_results['directories'])}</p>
        <p><strong>Files Found:</strong> {len(self.all_results['files'])}</p>
        <p><strong>VHosts Found:</strong> {len(self.all_results['vhosts'])}</p>
        <p><strong>Subdomains Found:</strong> {len(self.all_results['subdomains'])}</p>
    </div>
    
    <h2>Directories</h2>
    <table>
        <tr><th>Path</th><th>Status</th><th>Size</th><th>Full URL</th></tr>
"""
        
        for result in self.all_results['directories']:
            html_content += f"""        <tr>
            <td>{result['path']}</td>
            <td class="status-{result['status']}">{result['status']}</td>
            <td>{result['size']}</td>
            <td><a href="{result['full_url']}" target="_blank">{result['full_url']}</a></td>
        </tr>\n"""
        
        html_content += """    </table>
    
    <h2>Files</h2>
    <table>
        <tr><th>Path</th><th>Status</th><th>Size</th><th>Full URL</th></tr>
"""
        
        for result in self.all_results['files']:
            html_content += f"""        <tr>
            <td>{result['path']}</td>
            <td class="status-{result['status']}">{result['status']}</td>
            <td>{result['size']}</td>
            <td><a href="{result['full_url']}" target="_blank">{result['full_url']}</a></td>
        </tr>\n"""
        
        html_content += """    </table>
    
    <h2>Subdomains</h2>
    <table>
        <tr><th>Subdomain</th><th>Status</th><th>IP Address</th><th>Full URL</th></tr>
"""
        
        for result in self.all_results['subdomains']:
            html_content += f"""        <tr>
            <td>{result['path']}</td>
            <td class="status-200">{result['status']}</td>
            <td>{result['size']}</td>
            <td><a href="{result['full_url']}" target="_blank">{result['full_url']}</a></td>
        </tr>\n"""
        
        html_content += """    </table>
</body>
</html>
"""
        
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        logging.info(f"HTML report saved: {html_file}")


def main():
    parser = argparse.ArgumentParser(
        description="PathProwler - Advanced Directory Busting and Subdomain Enumeration\nProwl through paths and discover hidden treasures 🐾",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic directory scan
  python pathprowler.py -u http://target.com -m dir
  
  # File scan with custom extensions
  python pathprowler.py -u http://target.com -m files -e php,asp,jsp
  
  # VHost scan
  python pathprowler.py -u http://target.com -m vhost -d target.com
  
  # DNS subdomain enumeration only
  python pathprowler.py -u http://target.com -m dns -d target.com
  
  # Comprehensive subdomain enumeration (DNS + VHost)
  python pathprowler.py -u http://target.com -m subdomain -d target.com
  
  # All scans in parallel with JSON output
  python pathprowler.py -u http://target.com -m all -d target.com -o json
  
  # Recursive scan with custom status codes
  python pathprowler.py -u http://target.com -m dir -R -s "200,301,302,403"
  
  # Maximum speed with proxy
  python pathprowler.py -u http://target.com -m all -t 100 --timeout 5 -p http://127.0.0.1:8080
  
  # Stealth scan with delay and custom user agent
  python pathprowler.py -u http://target.com -m all --delay 100 -a "Mozilla/5.0"
        """
    )
    
    # Required arguments
    parser.add_argument('-u', '--url', required=True, help='Target URL (e.g., http://target.com)')
    
    # Scan configuration
    parser.add_argument('-m', '--mode', choices=['dir', 'files', 'vhost', 'dns', 'subdomain', 'all'], default='all',
                        help='Scan mode (default: all). Use "subdomain" for DNS+VHost enumeration')
    parser.add_argument('-w', '--wordlist-dir', default='/usr/share/wordlists/seclists',
                        help='SecLists wordlist directory (default: /usr/share/wordlists/seclists)')
    parser.add_argument('-t', '--threads', type=int, default=50,
                        help='Number of threads (default: 50, increase for faster scans)')
    parser.add_argument('-e', '--extensions', 
                        help='File extensions to search for (comma-separated, e.g., php,html,txt)')
    parser.add_argument('-d', '--domain', help='Domain for vhost scanning (e.g., target.com)')
    parser.add_argument('--timeout', type=int, default=10, help='Request timeout in seconds (default: 10)')
    
    # Advanced options
    parser.add_argument('-s', '--status-codes', default="200,204,301,302,307,401,403",
                        help='Status codes to match (default: 200,204,301,302,307,401,403)')
    parser.add_argument('-o', '--output-format', choices=['txt', 'json', 'csv', 'html', 'all'], default='txt',
                        help='Output format (default: txt)')
    parser.add_argument('-R', '--recursive', action='store_true',
                        help='Enable recursive directory scanning')
    parser.add_argument('--depth', type=int, default=3,
                        help='Recursive scan depth (default: 3)')
    parser.add_argument('-a', '--user-agent',
                        help='Custom User-Agent string')
    parser.add_argument('-c', '--cookies',
                        help='Cookies to use for requests')
    parser.add_argument('-p', '--proxy',
                        help='Proxy URL (e.g., http://127.0.0.1:8080)')
    parser.add_argument('--delay', type=int, default=0,
                        help='Delay between requests in milliseconds (default: 0)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output')
    parser.add_argument('--display-only', action='store_true',
                        help='Display results only without creating directories or saving files')
    
    args = parser.parse_args()
    
    # Banner
    print("=" * 70)
    print("  ██████╗  ██████╗ ██████╗ ██╗   ██╗███████╗████████╗███████╗██████╗ ")
    print(" ██╔════╝ ██╔═══██╗██╔══██╗██║   ██║██╔════╝╚══██╔══╝██╔════╝██╔══██╗")
    print(" ██║  ███╗██║   ██║██████╔╝██║   ██║███████╗   ██║   █████╗  ██████╔╝")
    print(" ██║   ██║██║   ██║██╔══██╗██║   ██║╚════██║   ██║   ██╔══╝  ██╔══██╗")
    print(" ╚██████╔╝╚██████╔╝██████╔╝╚██████╔╝███████║   ██║   ███████╗██║  ██║")
    print("  ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝")
    print("                    PRO - Advanced Recon Tool")
    print("=" * 70)
    print()
    
    scanner = GobusterScanner(
        target=args.url,
        wordlist_dir=args.wordlist_dir,
        threads=args.threads,
        timeout=args.timeout,
        status_codes=args.status_codes,
        output_format=args.output_format,
        verbose=args.verbose,
        recursive=args.recursive,
        recursive_depth=args.depth,
        user_agent=args.user_agent,
        cookies=args.cookies,
        proxy=args.proxy,
        delay=args.delay,
        display_only=args.display_only
    )
    
    # Check if gobuster is installed
    if not scanner.check_gobuster_installed():
        sys.exit(1)
    
    # Validate wordlists
    check_dns = args.mode in ['dns', 'all']
    if not scanner.validate_wordlists(check_dns=check_dns):
        sys.exit(1)
    
    # Run scans based on mode
    try:
        if args.mode == 'dir':
            scanner.scan_directories(args.extensions)
            scanner.generate_summary_report()
        elif args.mode == 'files':
            scanner.scan_files(args.extensions)
            scanner.generate_summary_report()
        elif args.mode == 'vhost':
            if not args.domain:
                logging.error("Domain (-d) required for vhost scanning")
                sys.exit(1)
            scanner.scan_vhosts(args.domain)
            scanner.generate_summary_report()
        elif args.mode == 'dns':
            if not args.domain:
                logging.error("Domain (-d) required for DNS scanning")
                sys.exit(1)
            scanner.scan_dns(args.domain, include_vhost=False)
            scanner.generate_summary_report()
        elif args.mode == 'subdomain':
            if not args.domain:
                logging.error("Domain (-d) required for subdomain enumeration")
                sys.exit(1)
            scanner.scan_dns(args.domain, include_vhost=True)
            scanner.generate_summary_report()
        elif args.mode == 'all':
            # For 'all' mode, run subdomain enumeration (DNS + VHost) if domain is provided
            if args.domain:
                scanner.scan_dns(args.domain, include_vhost=True)
            scanner.scan_all_parallel(args.extensions, None, None)  # Don't duplicate vhost/dns in parallel
        
        logging.info(f"\n✓ Scan complete! Results saved in: {scanner.results_dir}")
        
    except KeyboardInterrupt:
        logging.warning("\n[!] Scan interrupted by user")
        scanner.generate_summary_report()
        sys.exit(0)
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
