# 🐾 PathProwler

A powerful reconnaissance tool with both CLI and TUI interfaces for directory busting, file discovery, VHost scanning, and subdomain enumeration. Prowl through paths and discover hidden treasures. Built on gobuster with enhanced features and a beautiful interface.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

### 🎨 Dual Interface
*Prowl through paths and discover hidden treasures*
- **TUI (Terminal UI)** - Beautiful interactive dashboard with real-time monitoring
- **CLI** - Powerful command-line interface for automation and scripting

### 🔍 Comprehensive Scanning
- **Directory Busting** - Find hidden directories and paths
- **File Discovery** - Enumerate files with custom extensions
- **VHost Scanning** - Discover virtual hosts
- **DNS Enumeration** - Resolve subdomains via DNS
- **Subdomain Enumeration** - Combine DNS + VHost for maximum coverage

### ⚡ Performance
- **Parallel Scanning** - Run multiple scan types simultaneously
- **Configurable Threads** - Adjust speed (default: 50, max: 200+)
- **Smart Timeouts** - Configurable request timeouts
- **Progress Tracking** - Real-time statistics and status

### 📊 Output Formats
- **JSON** - Structured data for automation
- **CSV** - Spreadsheet-compatible format
- **HTML** - Visual reports with clickable links
- **TXT** - Raw gobuster output

### 🎯 Advanced Features
- **Recursive Scanning** - Deep directory enumeration
- **Custom Status Codes** - Filter by HTTP response codes
- **Proxy Support** - Route through Burp Suite or other proxies
- **Rate Limiting** - Add delays between requests
- **Custom User Agents** - Bypass basic filters
- **Result Deduplication** - Automatic merging of subdomain results

## 🚀 Quick Start

### Installation

**Windows (PowerShell):**
```powershell
.\install.ps1
```

**Linux/macOS (Bash):**
```bash
chmod +x install.sh
./install.sh
```

The installer automatically:
1. ✅ Checks prerequisites (Python, PathProwler)
2. ✅ Creates virtual environment
3. ✅ Installs dependencies
4. ✅ Offers to launch the TUI

### Running the Tools

**TUI Dashboard:**
```bash
.\run.ps1    # Windows
./run.sh     # Linux/Mac
```

**CLI:**
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # Linux/Mac

# Run scans
python pathprowler.py -u http://target.com -m all -d target.com -o all
```

## 📖 Documentation

- **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation guide
- **[README_TUI.md](README_TUI.md)** - TUI dashboard documentation
- **[SUBDOMAIN_ENUMERATION.md](SUBDOMAIN_ENUMERATION.md)** - Subdomain scanning guide
- **[DIRECTORY_NAMING.md](DIRECTORY_NAMING.md)** - Output organization
- **[DNS_USAGE.md](DNS_USAGE.md)** - DNS enumeration guide

## 🎯 Usage Examples

### TUI (Interactive Dashboard)

```bash
# Start the dashboard
.\run.ps1  # Windows
./run.sh   # Linux/Mac

# Configure in the UI:
# - Target URL: http://example.com
# - Domain: example.com
# - Scan Mode: Subdomain Enum (DNS + VHost)
# - Threads: 100
# - Press 's' to start
```

**Features:**
- 📊 Real-time statistics
- 📋 Live results table
- 🔍 Separate tabs for DNS, VHost, Directory, File scans
- 📝 Console log with status messages
- ⌨️ Keyboard shortcuts (s=start, x=stop, e=export, q=quit)

### CLI (Command Line)

#### Comprehensive Subdomain Enumeration
```bash
# DNS + VHost scanning (recommended)
python pathprowler.py -u http://example.com -m subdomain -d example.com -o all

# Output: pathprowler_example.com/
# - subdomains_dns.txt (DNS results)
# - subdomains_vhost.txt (VHost results)
# - subdomains_all.txt (merged & deduplicated)
# - results.json, results.csv, results.html
```

#### Directory Busting
```bash
# Basic directory scan
python pathprowler.py -u http://example.com -m dir

# Recursive with custom status codes
python pathprowler.py -u http://example.com -m dir -R -s "200,301,302,403"

# Fast scan with 100 threads
python pathprowler.py -u http://example.com -m dir -t 100
```

#### File Discovery
```bash
# Scan for specific file types
python pathprowler.py -u http://example.com -m files -e php,asp,jsp,html

# With custom extensions and recursive
python pathprowler.py -u http://example.com -m files -e txt,pdf,zip -R
```

#### VHost Scanning
```bash
# Discover virtual hosts
python pathprowler.py -u http://example.com -m vhost -d example.com
```

#### DNS Enumeration Only
```bash
# Pure DNS resolution
python pathprowler.py -u http://example.com -m dns -d example.com
```

#### All Scans in Parallel
```bash
# Run everything (dir + files + subdomain enumeration)
python pathprowler.py -u http://example.com -m all -d example.com -o all
```

#### Advanced Options
```bash
# Through proxy (Burp Suite)
python pathprowler.py -u http://example.com -m all -p http://127.0.0.1:8080

# Stealth scan with delays
python pathprowler.py -u http://example.com -m dir --delay 200 -t 25

# Custom user agent
python pathprowler.py -u http://example.com -m dir --user-agent "Custom/1.0"

# Custom wordlist location
python pathprowler.py -u http://example.com -m all -w /custom/wordlists
```

## 📁 Output Organization

Results are organized by **domain/IP** for easy identification:

```
pathprowler_example.com/
├── directories.txt          # Directory scan results
├── files.txt               # File scan results
├── subdomains_dns.txt      # DNS enumeration
├── subdomains_vhost.txt    # VHost enumeration
├── subdomains_all.txt      # Merged & deduplicated subdomains
├── results.json            # Structured JSON
├── results.csv             # CSV export
├── results.html            # HTML report
└── scan.log               # Detailed logs
```

**Multiple scans of the same target:**
```
pathprowler_example.com/       # First scan
pathprowler_example.com_1/     # Second scan
pathprowler_example.com_2/     # Third scan
```

## 🛠️ Prerequisites

### Required
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Gobuster** - [GitHub](https://github.com/OJ/gobuster)

### Recommended
- **SecLists** - Wordlists for scanning
  - Windows: `git clone https://github.com/danielmiessler/SecLists.git C:\wordlists\seclists`
  - Linux: `sudo apt install seclists` or clone to `/usr/share/wordlists/seclists`

## 🎨 TUI Screenshots

### Main Dashboard
```
┌─────────────────────────────────────────────────────────────┐
│  🎯 PathProwler - Interactive Reconnaissance Dashboard     │
├─────────────────────────────────────────────────────────────┤
│  📊 Statistics                                              │
│  Status: Running                                            │
│  📁 Directories: 47    📄 Files: 23                        │
│  🌐 VHosts: 12        🔍 Subdomains: 89                    │
│  Total: 171           ⏱️ Time: 45s                         │
├─────────────────────────────────────────────────────────────┤
│  ⚙️ Configuration                                           │
│  Target: http://example.com                                 │
│  Threads: 100    Timeout: 10s                              │
│  Mode: Subdomain Enum (DNS + VHost)                        │
├─────────────────────────────────────────────────────────────┤
│  📋 Results | 🔍 DNS Scan | 🌐 VHost Scan | 📝 Console    │
│  ┌─────────────────────────────────────────────────────┐  │
│  │ Type      | Path              | Status | IP         │  │
│  │ Subdomain | www.example.com   | Found  | 1.2.3.4    │  │
│  │ Subdomain | api.example.com   | Found  | 1.2.3.5    │  │
│  │ Directory | /admin            | 200    | 1234       │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Configuration

### Scan Modes
- `all` - All scans (directories + files + subdomain enumeration)
- `dir` - Directory busting only
- `files` - File discovery only
- `vhost` - VHost scanning only
- `dns` - DNS enumeration only
- `subdomain` - Comprehensive subdomain enum (DNS + VHost)

### Default Settings
- **Threads:** 50 (increase for faster scans)
- **Timeout:** 10 seconds
- **Status Codes:** 200,204,301,302,307,401,403
- **Wordlists:** SecLists (raft-medium)

### Wordlists Used
- **Directories:** `Discovery/Web-Content/raft-medium-directories.txt`
- **Files:** `Discovery/Web-Content/raft-medium-files.txt`
- **VHost:** `Discovery/DNS/subdomains-top1million-5000.txt`
- **DNS:** `Discovery/DNS/subdomains-top1million-110000.txt`

## 🎯 Scan Strategies

### Quick Discovery
```bash
# Fast initial scan
python pathprowler.py -u http://target.com -m subdomain -d target.com -t 100
```

### Comprehensive Recon
```bash
# Everything with all output formats
python pathprowler.py -u http://target.com -m all -d target.com -o all -R
```

### Stealth Scan
```bash
# Slow and quiet
python pathprowler.py -u http://target.com -m dir -t 25 --delay 200 --timeout 15
```

### Maximum Speed
```bash
# Aggressive scanning
python pathprowler.py -u http://target.com -m all -d target.com -t 200 --timeout 3
```

## 🔍 Subdomain Enumeration

PathProwler uses **dual-technique subdomain enumeration**:

### DNS Resolution
- Finds subdomains with DNS records
- Gets IP addresses
- Fast and reliable

### VHost Scanning
- Finds virtual hosts on web server
- Discovers internal subdomains
- Finds dev/staging environments

### Combined Approach
```bash
# Best of both worlds
python pathprowler.py -u http://target.com -m subdomain -d target.com

# Output:
# - subdomains_dns.txt (DNS results)
# - subdomains_vhost.txt (VHost results)
# - subdomains_all.txt (merged & deduplicated)
```

**See [SUBDOMAIN_ENUMERATION.md](SUBDOMAIN_ENUMERATION.md) for detailed guide.**

## 📊 Output Formats

### JSON
```json
{
  "target": "http://example.com",
  "timestamp": "2026-03-18T11:32:00",
  "results": {
    "directories": [...],
    "files": [...],
    "subdomains": [
      {
        "path": "www.example.com",
        "status": "Found",
        "size": "1.2.3.4",
        "full_url": "http://www.example.com"
      }
    ]
  }
}
```

### CSV
```csv
Type,Path,Status,Size/IP,Full URL
Subdomain,www.example.com,Found,1.2.3.4,http://www.example.com
Directory,/admin,200,1234,http://example.com/admin
```

### HTML
Interactive HTML report with:
- Clickable links
- Color-coded status codes
- Sortable tables
- Summary statistics

## 🤝 Integration

### With Other Tools
```bash
# Export for Aquatone
cat pathprowler_example.com/subdomains_all.txt | grep -v "^#" | cut -d'|' -f1 | aquatone

# Export for Nmap
cat pathprowler_example.com/subdomains_all.txt | grep -v "^#" | cut -d'|' -f2 | nmap -iL -

# Export for Nuclei
cat pathprowler_example.com/subdomains_all.txt | grep -v "^#" | cut -d'|' -f1 | nuclei
```

### Automation
```bash
#!/bin/bash
# Automated recon script
DOMAIN=$1
python pathprowler.py -u "http://$DOMAIN" -m subdomain -d "$DOMAIN" -o json
cat "pathprowler_$DOMAIN/subdomains_all.txt" | grep -v "^#" | cut -d'|' -f1 > subdomains.txt
```

## 🐛 Troubleshooting

### Common Issues

**"Python not found"**
```bash
# Install Python 3.8+
# Windows: https://www.python.org/downloads/
# Linux: sudo apt install python3
# macOS: brew install python3
```

**"Gobuster not found"**
```bash
# Install gobuster
# Windows: choco install gobuster
# Linux: sudo apt install gobuster
# macOS: brew install gobuster
```

**"Virtual environment not found"**
```bash
# Run installer
.\install.ps1  # Windows
./install.sh   # Linux/Mac
```

**"Permission denied" (Linux/Mac)**
```bash
chmod +x install.sh run.sh
```

**See [INSTALLATION.md](INSTALLATION.md) for detailed troubleshooting.**

## 📝 License

MIT License - Feel free to use and modify!

## 🙏 Credits

- **Gobuster** - OJ Reeves ([GitHub](https://github.com/OJ/gobuster))
- **SecLists** - Daniel Miessler ([GitHub](https://github.com/danielmiessler/SecLists))
- **Textual** - Textualize ([GitHub](https://github.com/Textualize/textual))
- **Rich** - Will McGugan ([GitHub](https://github.com/Textualize/rich))

## 🚀 Quick Reference

### Installation
```bash
.\install.ps1  # Windows
./install.sh   # Linux/Mac
```

### Run TUI
```bash
.\run.ps1   # Windows
./run.sh    # Linux/Mac
```

### Run CLI
```bash
# Comprehensive scan
python pathprowler.py -u http://target.com -m all -d target.com -o all

# Subdomain enumeration
python pathprowler.py -u http://target.com -m subdomain -d target.com

# Directory busting
python pathprowler.py -u http://target.com -m dir -t 100
```

### Output Location
```
pathprowler_<domain_or_ip>/
├── subdomains_all.txt  # Merged subdomains
├── results.json        # Structured data
└── scan.log           # Detailed logs
```

---

**Happy Prowling! 🐾🎯**
