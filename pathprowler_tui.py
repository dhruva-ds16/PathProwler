#!/usr/bin/env python3
"""
PathProwler - Interactive TUI Dashboard
Beautiful bubble-style terminal interface using Rich and Questionary
"""

import subprocess
import os
import sys
import time
import threading
from datetime import datetime
from typing import Optional, Dict

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.align import Align
from rich import box
from rich.columns import Columns
import questionary
from questionary import Style

# Custom bubble-style theme
custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),
    ('question', 'bold'),
    ('answer', 'fg:#2196f3 bold'),
    ('pointer', 'fg:#673ab7 bold'),
    ('highlighted', 'fg:#673ab7 bold'),
    ('selected', 'fg:#4caf50'),
    ('separator', 'fg:#cc5454'),
    ('instruction', 'fg:#858585'),
    ('text', ''),
])

console = Console()


class PathProwlerTUI:
    """Beautiful bubble-style TUI for PathProwler"""
    
    def __init__(self):
        self.config = {}
        self.stats = {
            'status': 'Idle',
            'directories': 0,
            'files': 0,
            'vhosts': 0,
            'subdomains': 0,
            'start_time': None
        }
        self.scan_process = None
        self.running = False
    
    def show_banner(self):
        """Display welcome banner"""
        banner = Text()
        banner.append("🐾 ", style="bold magenta")
        banner.append("PathProwler", style="bold cyan")
        banner.append(" v2.0\n", style="dim")
        banner.append("Prowl through paths and discover hidden treasures", style="italic dim")
        
        panel = Panel(
            Align.center(banner),
            box=box.DOUBLE,
            border_style="cyan",
            padding=(1, 2)
        )
        console.print(panel)
        console.print()
    
    def get_configuration(self):
        """Interactive configuration using questionary"""
        console.print("[bold cyan]⚙️  Scan Configuration[/]\n")
        
        # Target URL
        self.config['target'] = questionary.text(
            "Target URL:",
            default="http://example.com",
            style=custom_style
        ).ask()
        
        if not self.config['target']:
            console.print("[red]✗ Target URL is required![/]")
            return False
        
        # Scan Mode
        self.config['mode'] = questionary.select(
            "Scan Mode:",
            choices=[
                "🎯 All Scans (Dir + Files + Subdomains)",
                "📁 Directory Busting Only",
                "📄 File Discovery Only",
                "🌐 VHost Scanning Only",
                "🔎 DNS Enumeration Only",
                "🎯 Subdomain Enum (DNS + VHost)"
            ],
            style=custom_style
        ).ask()
        
        # Map display to mode value
        mode_map = {
            "🎯 All Scans (Dir + Files + Subdomains)": "all",
            "📁 Directory Busting Only": "dir",
            "📄 File Discovery Only": "files",
            "🌐 VHost Scanning Only": "vhost",
            "🔎 DNS Enumeration Only": "dns",
            "🎯 Subdomain Enum (DNS + VHost)": "subdomain"
        }
        self.config['mode'] = mode_map[self.config['mode']]
        
        # Domain (if needed)
        if self.config['mode'] in ['vhost', 'dns', 'subdomain', 'all']:
            self.config['domain'] = questionary.text(
                "Domain (for VHost/DNS):",
                default="example.com",
                style=custom_style
            ).ask()
        
        # Advanced options
        show_advanced = questionary.confirm(
            "Configure advanced options?",
            default=False,
            style=custom_style
        ).ask()
        
        if show_advanced:
            self.config['threads'] = questionary.text(
                "Threads:",
                default="50",
                style=custom_style
            ).ask()
            
            self.config['timeout'] = questionary.text(
                "Timeout (seconds):",
                default="10",
                style=custom_style
            ).ask()
            
            self.config['extensions'] = questionary.text(
                "File Extensions (comma-separated):",
                default="php,html,txt,asp,jsp",
                style=custom_style
            ).ask()
            
            self.config['wordlist'] = questionary.text(
                "Wordlist Directory:",
                default="/usr/share/wordlists/seclists",
                style=custom_style
            ).ask()
        else:
            self.config['threads'] = "50"
            self.config['timeout'] = "10"
            self.config['extensions'] = "php,html,txt,asp,jsp"
            self.config['wordlist'] = "/usr/share/wordlists/seclists"
        
        return True
    
    def show_config_summary(self):
        """Display configuration summary"""
        table = Table(
            title="📋 Scan Configuration",
            box=box.ROUNDED,
            border_style="cyan",
            show_header=True,
            header_style="bold cyan"
        )
        
        table.add_column("Parameter", style="bold yellow")
        table.add_column("Value", style="green")
        
        table.add_row("Target", self.config['target'])
        table.add_row("Mode", self.config['mode'])
        if 'domain' in self.config:
            table.add_row("Domain", self.config['domain'])
        table.add_row("Threads", self.config['threads'])
        table.add_row("Timeout", f"{self.config['timeout']}s")
        
        console.print(table)
        console.print()
        
        # Confirm
        return questionary.confirm(
            "Start scan with these settings?",
            default=True,
            style=custom_style
        ).ask()
    
    def create_stats_panel(self):
        """Create statistics panel"""
        elapsed = "0s"
        if self.stats['start_time']:
            elapsed_sec = int(time.time() - self.stats['start_time'])
            elapsed = f"{elapsed_sec}s"
        
        # Status indicator
        status_color = "green" if self.stats['status'] == "Running" else "yellow"
        status_text = Text()
        status_text.append("● ", style=f"bold {status_color}")
        status_text.append(self.stats['status'], style=f"bold {status_color}")
        
        # Stats grid
        stats_text = Text()
        stats_text.append(f"⏱️  {elapsed}\n\n", style="dim")
        stats_text.append(f"📁 Directories: ", style="bold green")
        stats_text.append(f"{self.stats['directories']}\n", style="cyan")
        stats_text.append(f"📄 Files: ", style="bold yellow")
        stats_text.append(f"{self.stats['files']}\n", style="cyan")
        stats_text.append(f"🌐 VHosts: ", style="bold magenta")
        stats_text.append(f"{self.stats['vhosts']}\n", style="cyan")
        stats_text.append(f"🔍 Subdomains: ", style="bold blue")
        stats_text.append(f"{self.stats['subdomains']}\n\n", style="cyan")
        
        total = sum([
            self.stats['directories'],
            self.stats['files'],
            self.stats['vhosts'],
            self.stats['subdomains']
        ])
        stats_text.append(f"Total: ", style="bold white")
        stats_text.append(f"{total}", style="bold cyan")
        
        # Combine status and stats
        content = Text()
        content.append_text(status_text)
        content.append("\n\n")
        content.append_text(stats_text)
        
        return Panel(
            Align.center(content),
            title="📊 Statistics",
            box=box.ROUNDED,
            border_style="cyan",
            padding=(1, 2)
        )
    
    def run_scan(self):
        """Execute the scan"""
        # Build command
        cmd = [
            sys.executable,
            "pathprowler.py",
            "-u", self.config['target'],
            "-m", self.config['mode'],
            "-t", self.config['threads'],
            "--timeout", self.config['timeout'],
            "-w", self.config['wordlist'],
            "--display-only",
            "-v"
        ]
        
        if 'domain' in self.config and self.config['domain']:
            cmd.extend(["-d", self.config['domain']])
        
        if self.config.get('extensions'):
            cmd.extend(["-e", self.config['extensions']])
        
        console.print(f"\n[dim]Command: {' '.join(cmd)}[/]\n")
        
        # Start scan
        self.stats['status'] = "Running"
        self.stats['start_time'] = time.time()
        self.running = True
        
        try:
            self.scan_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # Create live display
            with Live(self.create_stats_panel(), refresh_per_second=2, console=console) as live:
                console.print(Panel(
                    "[bold cyan]Scan Output[/]",
                    box=box.ROUNDED,
                    border_style="yellow"
                ))
                
                # Read output
                for line in iter(self.scan_process.stdout.readline, ''):
                    if not line:
                        break
                    
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Update stats
                    if "[DIR]" in line:
                        self.stats['directories'] += 1
                        console.print(f"[green]✓[/] {line}")
                    elif "[FILES]" in line:
                        self.stats['files'] += 1
                        console.print(f"[yellow]✓[/] {line}")
                    elif "[VHOST]" in line:
                        self.stats['vhosts'] += 1
                        console.print(f"[magenta]✓[/] {line}")
                    elif "[DNS]" in line:
                        self.stats['subdomains'] += 1
                        console.print(f"[cyan]✓[/] {line}")
                    elif "ERROR" in line or "error" in line:
                        console.print(f"[red]✗[/] {line}")
                    elif "completed" in line or "SUCCESS" in line:
                        console.print(f"[green]✓[/] {line}")
                    else:
                        console.print(f"[dim]•[/] {line}")
                    
                    # Update live display
                    live.update(self.create_stats_panel())
                
                self.scan_process.wait()
            
            self.stats['status'] = "Completed"
            console.print(f"\n{self.create_stats_panel()}")
            console.print("\n[bold green]✓ Scan completed successfully![/]\n")
            
        except KeyboardInterrupt:
            console.print("\n[yellow]⚠ Scan interrupted by user[/]")
            if self.scan_process:
                self.scan_process.terminate()
            self.stats['status'] = "Stopped"
        except Exception as e:
            console.print(f"\n[red]✗ Error: {e}[/]")
            self.stats['status'] = "Error"
        finally:
            self.running = False
    
    def run(self):
        """Main TUI loop"""
        try:
            # Clear screen
            console.clear()
            
            # Show banner
            self.show_banner()
            
            # Get configuration
            if not self.get_configuration():
                return
            
            console.print()
            
            # Show summary and confirm
            if not self.show_config_summary():
                console.print("[yellow]Scan cancelled.[/]")
                return
            
            # Run scan
            self.run_scan()
            
            # Ask to run another scan
            console.print()
            if questionary.confirm(
                "Run another scan?",
                default=False,
                style=custom_style
            ).ask():
                self.stats = {
                    'status': 'Idle',
                    'directories': 0,
                    'files': 0,
                    'vhosts': 0,
                    'subdomains': 0,
                    'start_time': None
                }
                self.run()
            else:
                console.print("\n[bold cyan]🐾 Happy Prowling! 🎯[/]\n")
        
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Goodbye! 👋[/]\n")
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/]\n")


def main():
    """Entry point"""
    tui = PathProwlerTUI()
    tui.run()


if __name__ == "__main__":
    main()
