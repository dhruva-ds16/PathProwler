#!/usr/bin/env python3
"""
Gobuster Pro - Interactive TUI Dashboard
Real-time directory busting and vhost scanning with live monitoring
"""

import subprocess
import os
import json
import re
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header, Footer, Button, Input, Label, Static, 
    DataTable, TabbedContent, TabPane, Log, ProgressBar,
    Select, Switch, Checkbox
)
from textual.binding import Binding
from textual.reactive import reactive
from textual import work
from textual.worker import Worker, WorkerState


class WelcomeBanner(Static):
    """Welcome banner widget"""
    
    def compose(self) -> ComposeResult:
        banner = """
[bold cyan]╔═══════════════════════════════════════╗[/]
[bold cyan]║[/]  [bold magenta]🐾 PathProwler[/] [dim]v2.0[/]              [bold cyan]║[/]
[bold cyan]║[/]  [dim]Prowl through paths & discover[/]  [bold cyan]║[/]
[bold cyan]║[/]  [dim]hidden treasures with precision[/] [bold cyan]║[/]
[bold cyan]╚═══════════════════════════════════════╝[/]
        """
        yield Static(banner, id="welcome-banner")


class ScanStats(Static):
    """Widget to display scan statistics"""
    
    directories_found = reactive(0)
    files_found = reactive(0)
    vhosts_found = reactive(0)
    subdomains_found = reactive(0)
    scan_status = reactive("Idle")
    elapsed_time = reactive("0s")
    
    def compose(self) -> ComposeResult:
        yield Static("📊 Live Statistics", classes="stats-title")
        yield Static(id="stats-content")
    
    def watch_directories_found(self, value: int) -> None:
        self.update_stats()
    
    def watch_files_found(self, value: int) -> None:
        self.update_stats()
    
    def watch_vhosts_found(self, value: int) -> None:
        self.update_stats()
    
    def watch_subdomains_found(self, value: int) -> None:
        self.update_stats()
    
    def watch_scan_status(self, value: str) -> None:
        self.update_stats()
    
    def watch_elapsed_time(self, value: str) -> None:
        self.update_stats()
    
    def update_stats(self) -> None:
        stats_widget = self.query_one("#stats-content", Static)
        total = self.directories_found + self.files_found + self.vhosts_found + self.subdomains_found
        
        # Status indicator with color
        status_color = "green" if self.scan_status == "Running" else "yellow" if self.scan_status == "Idle" else "cyan"
        
        stats_widget.update(f"""
╭─────────────────────────╮
│ [bold {status_color}]● {self.scan_status:^18}[/] │
│ [dim]⏱️  {self.elapsed_time:^19}[/] │
╰─────────────────────────╯

[bold green]📁 Directories[/]
   [cyan]▸[/] {self.directories_found:>4} [dim]found[/]

[bold yellow]📄 Files[/]
   [cyan]▸[/] {self.files_found:>4} [dim]found[/]

[bold magenta]🌐 VHosts[/]
   [cyan]▸[/] {self.vhosts_found:>4} [dim]found[/]

[bold blue]🔍 Subdomains[/]
   [cyan]▸[/] {self.subdomains_found:>4} [dim]found[/]

╭─────────────────────────╮
│ [bold white]Total Results: {total:>4}[/]  │
╰─────────────────────────╯
        """)


class ScanConfig(Static):
    """Widget for scan configuration"""
    
    def compose(self) -> ComposeResult:
        yield Label("🎯 Target Configuration", classes="section-title")
        yield Label("Target URL:")
        yield Input(placeholder="http://target.com", id="target-url")
        
        yield Label("Wordlist Directory:")
        yield Input(
            value="/usr/share/wordlists/seclists",
            id="wordlist-dir"
        )
        
        with Horizontal(classes="config-row"):
            with Vertical():
                yield Label("Threads:")
                yield Input(value="50", id="threads")
            with Vertical():
                yield Label("Timeout (s):")
                yield Input(value="10", id="timeout")
        
        yield Label("Extensions (comma-separated):")
        yield Input(placeholder="php,html,txt,asp,jsp", id="extensions")
        
        yield Label("Status Codes:")
        yield Input(value="200,204,301,302,307,401,403", id="status-codes")
        
        with Horizontal(classes="config-row"):
            with Vertical():
                yield Label("Scan Mode:")
                yield Select(
                    [("All (Dir + Files + Subdomains)", "all"),
                     ("Directories Only", "dir"),
                     ("Files Only", "files"),
                     ("VHost Only", "vhost"),
                     ("DNS Only", "dns"),
                     ("Subdomain Enum (DNS + VHost)", "subdomain")],
                    value="all",
                    id="scan-mode"
                )
            with Vertical():
                yield Label("Domain (for VHost):")
                yield Input(placeholder="target.com", id="domain")
        
        with Horizontal(classes="config-row"):
            yield Checkbox("Recursive", id="recursive")
            yield Checkbox("Verbose", id="verbose")
        
        with Horizontal(classes="button-row"):
            yield Button("🚀 Start Scan", variant="success", id="start-scan")
            yield Button("⏹️  Stop", variant="error", id="stop-scan")
            yield Button("💾 Export", variant="primary", id="export-results")


class ResultsTable(DataTable):
    """Custom DataTable for displaying scan results"""
    
    def on_mount(self) -> None:
        self.add_columns("Type", "Path", "Status", "Size", "Full URL")
        self.cursor_type = "row"
        self.zebra_stripes = True


class PathProwlerDashboard(App):
    """PathProwler - Prowl through paths and discover hidden treasures 🐾"""
    
    CSS = """
    Screen {
        background: $surface;
        layers: base overlay;
    }
    
    .section-title {
        background: $primary;
        color: $text;
        padding: 1;
        text-align: center;
        text-style: bold;
        border: heavy $primary-darken-2;
    }
    
    .stats-title {
        background: $accent;
        color: $text;
        padding: 1;
        text-align: center;
        text-style: bold;
        border: heavy $accent-darken-2;
    }
    
    ScanStats {
        width: 32;
        height: 100%;
        border: heavy $primary;
        padding: 1 2;
        background: $panel;
        border-title-align: center;
        border-title-color: $accent;
        border-title-style: bold;
    }
    
    ScanConfig {
        height: 100%;
        border: heavy $accent;
        padding: 1 2;
        overflow-y: auto;
        background: $panel;
        border-title-align: center;
        border-title-color: $primary;
        border-title-style: bold;
    }
    
    .config-row {
        height: auto;
        margin: 1 0;
    }
    
    .button-row {
        height: auto;
        margin-top: 2;
        align: center middle;
    }
    
    Input {
        margin-bottom: 1;
        border: solid $primary-lighten-1;
        background: $boost;
    }
    
    Input:focus {
        border: heavy $accent;
    }
    
    Button {
        margin: 0 1;
        min-width: 18;
        border: heavy;
    }
    
    Button:hover {
        background: $primary;
        border: heavy $accent;
    }
    
    Log {
        border: heavy $warning;
        height: 100%;
        background: $panel;
        scrollbar-background: $panel;
        scrollbar-color: $warning;
    }
    
    DataTable {
        height: 100%;
        border: heavy $success;
        background: $panel;
    }
    
    DataTable > .datatable--header {
        background: $success;
        color: $text;
        text-style: bold;
    }
    
    DataTable > .datatable--cursor {
        background: $accent 50%;
    }
    
    ProgressBar {
        margin: 1 0;
        height: 3;
    }
    
    ProgressBar > .bar--bar {
        color: $success;
    }
    
    ProgressBar > .bar--indeterminate {
        color: $warning;
    }
    
    #main-container {
        height: 100%;
    }
    
    #left-panel {
        width: 35%;
        height: 100%;
    }
    
    #right-panel {
        width: 65%;
        height: 100%;
        border-left: heavy $primary;
    }
    
    TabPane {
        padding: 1 2;
        background: $panel;
    }
    
    TabbedContent {
        border: heavy $primary;
    }
    
    Tabs {
        background: $primary-darken-2;
    }
    
    Tab {
        background: $panel;
        color: $text-muted;
    }
    
    Tab:hover {
        background: $primary-lighten-1;
        color: $text;
    }
    
    Tab.-active {
        background: $primary;
        color: $text;
        text-style: bold;
    }
    
    Label {
        color: $text-muted;
        text-style: bold;
        margin-bottom: 0;
    }
    
    Checkbox {
        background: $boost;
        border: solid $primary;
        padding: 0 1;
    }
    
    Checkbox:focus {
        border: heavy $accent;
    }
    
    Select {
        border: solid $primary-lighten-1;
        background: $boost;
    }
    
    Select:focus {
        border: heavy $accent;
    }
    
    #stats-content {
        padding: 1 0;
        color: $text;
    }
    
    #welcome-banner {
        text-align: center;
        padding: 1;
        background: $panel;
        border: heavy $accent;
        margin-bottom: 1;
    }
    
    WelcomeBanner {
        height: auto;
        dock: top;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("s", "start_scan", "Start Scan", show=True),
        Binding("x", "stop_scan", "Stop Scan", show=True),
        Binding("e", "export", "Export", show=True),
        Binding("c", "clear_results", "Clear Results", show=False),
    ]
    
    TITLE = "🐾 PathProwler - Interactive Reconnaissance Dashboard"
    
    def __init__(self):
        super().__init__()
        self.scan_worker: Optional[Worker] = None
        self.results = {
            'directories': [],
            'files': [],
            'vhosts': []
        }
        self.results_dir = None
        self.start_time = None
        self.scan_processes = []
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield WelcomeBanner()
        
        with Horizontal(id="main-container"):
            with Vertical(id="left-panel"):
                yield ScanStats()
                yield ScanConfig()
            
            with Vertical(id="right-panel"):
                with TabbedContent():
                    with TabPane("📋 Results", id="results-tab"):
                        yield ResultsTable(id="results-table")
                    
                    with TabPane("📝 Console Log", id="log-tab"):
                        yield Log(id="console-log", highlight=True, markup=True)
                    
                    with TabPane("📊 Directory Scan", id="dir-tab"):
                        yield Log(id="dir-log", highlight=True)
                    
                    with TabPane("📄 File Scan", id="file-tab"):
                        yield Log(id="file-log", highlight=True)
                    
                    with TabPane("🌐 VHost Scan", id="vhost-tab"):
                        yield Log(id="vhost-log", highlight=True)
                    
                    with TabPane("🔍 DNS Scan", id="dns-tab"):
                        yield Log(id="dns-log", highlight=True)
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize the dashboard"""
        self.log_message("🐾 PathProwler Dashboard initialized successfully", "success")
        self.log_message("💡 Configure your scan settings and press 'Start Scan' or 's'", "info")
        self.log_message("📚 Use Tab to navigate between result views", "info")
    
    def log_message(self, message: str, level: str = "info") -> None:
        """Log a message to the console with enhanced formatting"""
        console_log = self.query_one("#console-log", Log)
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Enhanced color scheme and icons
        formats = {
            "info": ("cyan", "ℹ️"),
            "success": ("green", "✓"),
            "warning": ("yellow", "⚠️"),
            "error": ("red", "✗"),
            "scan": ("magenta", "🔍")
        }
        color, icon = formats.get(level, ("white", "•"))
        
        console_log.write_line(f"[dim]{timestamp}[/] [{color}]{icon}[/] {message}")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "start-scan":
            self.action_start_scan()
        elif event.button.id == "stop-scan":
            self.action_stop_scan()
        elif event.button.id == "export-results":
            self.action_export()
    
    def action_start_scan(self) -> None:
        """Start the scan"""
        if self.scan_worker and self.scan_worker.state == WorkerState.RUNNING:
            self.log_message("Scan already running!", "warning")
            return
        
        # Get configuration
        target = self.query_one("#target-url", Input).value
        if not target:
            self.log_message("Please enter a target URL", "error")
            return
        
        # Clear previous results
        self.action_clear_results()
        
        # Update stats
        stats = self.query_one(ScanStats)
        stats.scan_status = "Running..."
        
        self.log_message(f"Starting scan on {target}", "success")
        self.start_time = datetime.now()
        
        # Start the scan worker
        self.scan_worker = self.run_scan()
    
    def action_stop_scan(self) -> None:
        """Stop the running scan"""
        if self.scan_worker:
            self.scan_worker.cancel()
            self.log_message("Scan stopped by user", "warning")
            
            # Kill any running processes
            for proc in self.scan_processes:
                try:
                    proc.terminate()
                except:
                    pass
            self.scan_processes.clear()
            
            stats = self.query_one(ScanStats)
            stats.scan_status = "Stopped"
    
    def action_clear_results(self) -> None:
        """Clear all results"""
        table = self.query_one("#results-table", ResultsTable)
        table.clear()
        
        self.results = {
            'directories': [],
            'files': [],
            'vhosts': [],
            'subdomains': []
        }
        
        stats = self.query_one(ScanStats)
        stats.directories_found = 0
        stats.files_found = 0
        stats.vhosts_found = 0
        stats.subdomains_found = 0
    
    def action_export(self) -> None:
        """Export results to files"""
        if not self.results_dir:
            self.log_message("No results to export", "warning")
            return
        
        # Export to JSON
        json_file = os.path.join(self.results_dir, "results.json")
        with open(json_file, 'w') as f:
            json.dump({
                'target': self.query_one("#target-url", Input).value,
                'timestamp': datetime.now().isoformat(),
                'results': self.results
            }, f, indent=2)
        
        self.log_message(f"Results exported to {self.results_dir}", "success")
    
    def _extract_target_name(self, target):
        """Extract domain or IP from target URL for directory naming"""
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
    
    @work(exclusive=True, thread=True)
    def run_scan(self) -> None:
        """Run the gobuster scan in a worker thread"""
        # Get configuration
        target = self.query_one("#target-url", Input).value
        wordlist_dir = self.query_one("#wordlist-dir", Input).value
        threads = self.query_one("#threads", Input).value or "50"
        timeout = self.query_one("#timeout", Input).value or "10"
        extensions = self.query_one("#extensions", Input).value
        status_codes = self.query_one("#status-codes", Input).value
        scan_mode = self.query_one("#scan-mode", Select).value
        domain = self.query_one("#domain", Input).value
        recursive = self.query_one("#recursive", Checkbox).value
        verbose = self.query_one("#verbose", Checkbox).value
        
        # Extract domain/IP from target for directory name
        target_name = self._extract_target_name(target)
        self.results_dir = f"pathprowler_{target_name}"
        
        # Create results directory (append counter if exists)
        base_dir = self.results_dir
        counter = 1
        while os.path.exists(self.results_dir):
            self.results_dir = f"{base_dir}_{counter}"
            counter += 1
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Wordlists
        dir_wordlist = os.path.join(wordlist_dir, "Discovery/Web-Content/raft-medium-directories.txt")
        file_wordlist = os.path.join(wordlist_dir, "Discovery/Web-Content/raft-medium-files.txt")
        vhost_wordlist = os.path.join(wordlist_dir, "Discovery/DNS/subdomains-top1million-5000.txt")
        dns_wordlist = os.path.join(wordlist_dir, "Discovery/DNS/subdomains-top1million-110000.txt")
        
        # Run scans based on mode
        if scan_mode in ["all", "dir"]:
            self.run_gobuster_dir(target, dir_wordlist, threads, timeout, status_codes, 
                                 extensions, recursive, verbose, "directories")
        
        if scan_mode in ["all", "files"]:
            self.run_gobuster_dir(target, file_wordlist, threads, timeout, status_codes,
                                 extensions or "php,html,txt,asp,jsp", recursive, verbose, "files")
        
        if scan_mode == "vhost" and domain:
            self.run_gobuster_vhost(target, vhost_wordlist, threads, timeout, domain, verbose)
        
        if scan_mode == "dns" and domain:
            self.run_gobuster_dns(target, dns_wordlist, threads, timeout, domain, verbose)
        
        if scan_mode in ["all", "subdomain"] and domain:
            # Run both DNS and VHost for comprehensive subdomain enumeration
            self.app.call_from_thread(
                self.log_message,
                "Starting comprehensive subdomain enumeration (DNS + VHost)",
                "success"
            )
            self.run_gobuster_dns(target, dns_wordlist, threads, timeout, domain, verbose)
            self.run_gobuster_vhost(target, vhost_wordlist, threads, timeout, domain, verbose)
            self.merge_subdomain_results()
        
        # Update final status
        self.app.call_from_thread(self.scan_complete)
    
    def run_gobuster_dir(self, target, wordlist, threads, timeout, status_codes, 
                        extensions, recursive, verbose, scan_type):
        """Run gobuster directory scan"""
        output_file = os.path.join(self.results_dir, f"{scan_type}.txt")
        
        cmd = [
            "gobuster", "dir",
            "-u", target,
            "-w", wordlist,
            "-t", threads,
            "-o", output_file,
            "--timeout", f"{timeout}s",
            "-k",
            "-s", status_codes,
        ]
        
        if extensions:
            cmd.extend(["-x", extensions])
        
        if recursive:
            cmd.extend(["--wildcard", "-R", "-d", "3"])
        
        if not verbose:
            cmd.append("-q")
        
        log_id = "dir-log" if scan_type == "directories" else "file-log"
        
        self.app.call_from_thread(
            self.log_message,
            f"Starting {scan_type} scan: {' '.join(cmd)}",
            "info"
        )
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            self.scan_processes.append(process)
            
            # Read output line by line
            for line in process.stdout:
                line = line.strip()
                if line:
                    # Log to specific tab
                    log_widget = self.query_one(f"#{log_id}", Log)
                    self.app.call_from_thread(log_widget.write_line, line)
                    
                    # Parse and add to results
                    self.parse_and_add_result(line, scan_type)
            
            process.wait()
            
            if process.returncode == 0:
                self.app.call_from_thread(
                    self.log_message,
                    f"{scan_type.capitalize()} scan completed successfully",
                    "success"
                )
            
        except Exception as e:
            self.app.call_from_thread(
                self.log_message,
                f"Error in {scan_type} scan: {e}",
                "error"
            )
    
    def run_gobuster_vhost(self, target, wordlist, threads, timeout, domain, verbose):
        """Run gobuster vhost scan"""
        output_file = os.path.join(self.results_dir, "vhosts.txt")
        
        cmd = [
            "gobuster", "vhost",
            "-u", target,
            "-w", wordlist,
            "-t", threads,
            "-o", output_file,
            "--timeout", f"{timeout}s",
            "-k",
            "--domain", domain
        ]
        
        if not verbose:
            cmd.append("-q")
        
        self.app.call_from_thread(
            self.log_message,
            f"Starting vhost scan: {' '.join(cmd)}",
            "info"
        )
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            self.scan_processes.append(process)
            
            for line in process.stdout:
                line = line.strip()
                if line:
                    log_widget = self.query_one("#vhost-log", Log)
                    self.app.call_from_thread(log_widget.write_line, line)
                    self.parse_and_add_result(line, "vhosts")
            
            process.wait()
            
            if process.returncode == 0:
                self.app.call_from_thread(
                    self.log_message,
                    "VHost scan completed successfully",
                    "success"
                )
            
        except Exception as e:
            self.app.call_from_thread(
                self.log_message,
                f"Error in vhost scan: {e}",
                "error"
            )
    
    def run_gobuster_dns(self, target, wordlist, threads, timeout, domain, verbose):
        """Run gobuster DNS subdomain scan"""
        output_file = os.path.join(self.results_dir, "subdomains.txt")
        
        cmd = [
            "gobuster", "dns",
            "-d", domain,
            "-w", wordlist,
            "-t", threads,
            "-o", output_file,
            "--timeout", f"{timeout}s",
        ]
        
        if not verbose:
            cmd.append("-q")
        
        self.app.call_from_thread(
            self.log_message,
            f"Starting DNS scan: {' '.join(cmd)}",
            "info"
        )
        
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            self.scan_processes.append(process)
            
            for line in process.stdout:
                line = line.strip()
                if line:
                    log_widget = self.query_one("#dns-log", Log)
                    self.app.call_from_thread(log_widget.write_line, line)
                    self.parse_and_add_dns_result(line, domain)
            
            process.wait()
            
            if process.returncode == 0:
                self.app.call_from_thread(
                    self.log_message,
                    "DNS scan completed successfully",
                    "success"
                )
            
        except Exception as e:
            self.app.call_from_thread(
                self.log_message,
                f"Error in DNS scan: {e}",
                "error"
            )
    
    def parse_and_add_result(self, line: str, scan_type: str) -> None:
        """Parse gobuster output and add to results"""
        # Format: /path (Status: 200) [Size: 1234]
        match = re.search(r'(\S+)\s+\(Status: (\d+)\)', line)
        if match:
            path, status = match.groups()
            size_match = re.search(r'\[Size: (\d+)\]', line)
            size = size_match.group(1) if size_match else "N/A"
            
            target = self.query_one("#target-url", Input).value
            full_url = f"{target}{path}" if scan_type != "vhosts" else path
            
            result = {
                'path': path,
                'status': status,
                'size': size,
                'full_url': full_url
            }
            
            # Add to results
            self.results[scan_type].append(result)
            
            # Update table
            table = self.query_one("#results-table", ResultsTable)
            type_label = scan_type.rstrip('s').capitalize()
            
            self.app.call_from_thread(
                table.add_row,
                type_label,
                path,
                status,
                size,
                full_url
            )
            
            # Update stats
            stats = self.query_one(ScanStats)
            if scan_type == "directories":
                stats.directories_found += 1
            elif scan_type == "files":
                stats.files_found += 1
            elif scan_type == "vhosts":
                stats.vhosts_found += 1
            elif scan_type == "subdomains":
                stats.subdomains_found += 1
            
            # Update elapsed time
            if self.start_time:
                elapsed = (datetime.now() - self.start_time).total_seconds()
                stats.elapsed_time = f"{int(elapsed)}s"
    
    def parse_and_add_dns_result(self, line: str, domain: str) -> None:
        """Parse gobuster DNS output and add to results"""
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
                potential_ip = parts[-1]
                if re.match(r'^\d+\.\d+\.\d+\.\d+$', potential_ip):
                    ip = potential_ip
            
            full_url = f"http://{subdomain}"
            
            result = {
                'path': subdomain,
                'status': 'Found',
                'size': ip,
                'full_url': full_url
            }
            
            # Add to results
            self.results['subdomains'].append(result)
            
            # Update table
            table = self.query_one("#results-table", ResultsTable)
            
            self.app.call_from_thread(
                table.add_row,
                "Subdomain",
                subdomain,
                "Found",
                ip,
                full_url
            )
            
            # Update stats
            stats = self.query_one(ScanStats)
            stats.subdomains_found += 1
            
            # Update elapsed time
            if self.start_time:
                elapsed = (datetime.now() - self.start_time).total_seconds()
                stats.elapsed_time = f"{int(elapsed)}s"
    
    def merge_subdomain_results(self) -> None:
        """Merge and deduplicate subdomain results from DNS and VHost scans"""
        # Create a set of unique subdomains based on the 'path' field
        seen = set()
        unique_results = []
        
        for result in self.results['subdomains']:
            subdomain = result['path']
            if subdomain not in seen:
                seen.add(subdomain)
                unique_results.append(result)
        
        # Update with deduplicated results
        self.results['subdomains'] = unique_results
        
        # Update stats
        stats = self.query_one(ScanStats)
        stats.subdomains_found = len(unique_results)
        
        # Save merged results to a combined file
        if self.results_dir:
            merged_file = os.path.join(self.results_dir, "subdomains_all.txt")
            with open(merged_file, 'w') as f:
                f.write("# Combined Subdomain Enumeration Results\n")
                f.write(f"# Total Unique Subdomains: {len(unique_results)}\n")
                f.write("# Format: subdomain | IP | Source\n\n")
                
                for result in sorted(unique_results, key=lambda x: x['path']):
                    f.write(f"{result['path']} | {result['size']} | {result['status']}\n")
            
            self.app.call_from_thread(
                self.log_message,
                f"Merged {len(unique_results)} unique subdomains to: {merged_file}",
                "success"
            )
    
    def scan_complete(self) -> None:
        """Called when scan is complete"""
        stats = self.query_one(ScanStats)
        stats.scan_status = "Completed"
        
        total = stats.directories_found + stats.files_found + stats.vhosts_found
        self.log_message(f"Scan complete! Found {total} total results", "success")
        self.log_message(f"Results saved to: {self.results_dir}", "info")


def main():
    app = PathProwlerDashboard()
    app.run()


if __name__ == "__main__":
    main()
