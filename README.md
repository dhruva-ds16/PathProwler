<div align="center">

# 🐾 PathProwler

### *Prowl through paths and discover hidden treasures*

[![Version](https://img.shields.io/badge/version-2.0-blue?style=for-the-badge)](https://github.com/yourusername/pathprowler/releases)
[![Python](https://img.shields.io/badge/python-3.8+-green?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-orange?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)](https://github.com/yourusername/pathprowler)

**A powerful reconnaissance tool with dual interfaces (CLI & TUI) for directory busting, file discovery, VHost scanning, and subdomain enumeration.**

Built on [gobuster](https://github.com/OJ/gobuster) with enhanced features and a beautiful interactive dashboard.

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Examples](#-examples)

![PathProwler Demo](https://via.placeholder.com/800x400/1a1b26/7aa2f7?text=PathProwler+TUI+Dashboard)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎨 **Dual Interface**

- 🖥️ **TUI Dashboard** - Beautiful interactive terminal UI
  - Real-time monitoring
  - Live statistics
  - Tabbed result views
  - Keyboard shortcuts

- ⌨️ **CLI Tool** - Powerful command-line interface
  - Automation-friendly
  - Scriptable
  - Multiple output formats
  - Pipe-able results

</td>
<td width="50%">

### 🔍 **Comprehensive Scanning**

- 📁 **Directory Busting** - Hidden paths
- 📄 **File Discovery** - Custom extensions
- 🌐 **VHost Scanning** - Virtual hosts
- 🔎 **DNS Enumeration** - Subdomain resolution
- 🎯 **Dual Subdomain Enum** - DNS + VHost combined

</td>
</tr>
<tr>
<td width="50%">

### ⚡ **Performance**

- 🚀 Parallel scanning (multiple types simultaneously)
- ⚙️ Configurable threads (50-200+)
- ⏱️ Smart timeouts
- 📊 Real-time progress tracking
- 💾 Memory efficient

</td>
<td width="50%">

### 📊 **Output Formats**

- 📋 **JSON** - Structured data
- 📈 **CSV** - Spreadsheet format
- 🌐 **HTML** - Visual reports
- 📝 **TXT** - Raw output
- 🖥️ **Display-only** - No file saving

</td>
</tr>
</table>

### 🎯 **Advanced Features**

```
✓ Recursive Scanning          ✓ Custom Status Codes       ✓ Proxy Support (Burp Suite)
✓ Rate Limiting               ✓ Custom User Agents        ✓ Result Deduplication
✓ Cookie Support              ✓ Domain-based Naming       ✓ Comprehensive Logging
```

## 🚀 Installation

**Windows (PowerShell):**
```powershell
.\install.ps1
```

**Linux/macOS (Bash):**
```bash
chmod +x install.sh
./install.sh
```

**What the installer does:**
```
✓ Checks prerequisites (Python 3.8+, Gobuster)
✓ Creates virtual environment
✓ Installs dependencies (textual, rich)
✓ Offers to launch the TUI
```

### Quick Start

<table>
<tr>
<td width="50%">

**🖥️ TUI Dashboard**
```bash
# Windows
.\run.ps1

# Linux/macOS
./run.sh
```

</td>
<td width="50%">

**⌨️ CLI Tool**
```bash
# Activate venv
source venv/bin/activate

# Run scan
python pathprowler.py -u http://target.com -m all
```

</td>
</tr>
</table>

## 💡 Why PathProwler?

<table>
<tr>
<td>

**🎯 Problem**
- Gobuster is powerful but CLI-only
- No real-time monitoring
- Manual result management
- Separate tools for different scans

</td>
<td>

**✨ Solution**
- Beautiful TUI + powerful CLI
- Live statistics and progress
- Automatic organization by domain/IP
- Unified tool for all scan types

</td>
</tr>
</table>

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [📦 INSTALLATION.md](INSTALLATION.md) | Complete installation guide with troubleshooting |
| [🖥️ README_TUI.md](README_TUI.md) | TUI dashboard features and usage |
| [🔍 SUBDOMAIN_ENUMERATION.md](SUBDOMAIN_ENUMERATION.md) | Comprehensive subdomain scanning guide |
| [📁 DIRECTORY_NAMING.md](DIRECTORY_NAMING.md) | Output organization and naming conventions |
| [🌐 DNS_USAGE.md](DNS_USAGE.md) | DNS enumeration techniques and examples |

## 📚 Usage

### 🖥️ TUI (Interactive Dashboard)

Launch the beautiful terminal interface:

```bash
# Windows
.\run.ps1

# Linux/macOS
./run.sh
```

**Dashboard Features:**
```
✓ Real-time statistics       ✓ Live results table        ✓ Tabbed scan views
✓ Console logging           ✓ Keyboard shortcuts        ✓ Export functionality
```

**Keyboard Shortcuts:**
| Key | Action |
|-----|--------|
| `s` | Start Scan |
| `x` | Stop Scan |
| `e` | Export Results |
| `q` | Quit |
| `Tab` | Navigate Tabs |

### ⌨️ CLI (Command Line)

#### 🎯 Comprehensive Subdomain Enumeration
```bash
# DNS + VHost scanning (recommended)
python pathprowler.py -u http://example.com -m subdomain -d example.com -o all

# Output: pathprowler_example.com/
# - subdomains_dns.txt (DNS results)
# - subdomains_vhost.txt (VHost results)
# - subdomains_all.txt (merged & deduplicated)
# - results.json, results.csv, results.html
```

#### 📁 Directory Busting
```bash
# Basic directory scan
python pathprowler.py -u http://example.com -m dir

# Recursive with custom status codes
python pathprowler.py -u http://example.com -m dir -R -s "200,301,302,403"

# Fast scan with 100 threads
python pathprowler.py -u http://example.com -m dir -t 100
```

#### 📄 File Discovery
```bash
# Scan for specific file types
python pathprowler.py -u http://example.com -m files -e php,asp,jsp,html

# With custom extensions and recursive
python pathprowler.py -u http://example.com -m files -e txt,pdf,zip -R
```

#### 🌐 VHost Scanning
```bash
# Discover virtual hosts
python pathprowler.py -u http://example.com -m vhost -d example.com
```

#### 🔎 DNS Enumeration Only
```bash
# Pure DNS resolution
python pathprowler.py -u http://example.com -m dns -d example.com
```

#### 🚀 All Scans in Parallel
```bash
# Run everything (dir + files + subdomain enumeration)
python pathprowler.py -u http://example.com -m all -d example.com -o all
```

#### ⚙️ Advanced Options
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

<details>
<summary><b>Click to expand common issues</b></summary>

### Python not found
```bash
# Windows
winget install Python.Python.3.11

# Linux
sudo apt install python3 python3-pip

# macOS
brew install python3
```

### Gobuster not found
```bash
# Windows
choco install gobuster

# Linux
sudo apt install gobuster

# macOS
brew install gobuster
```

### Virtual environment issues
```bash
# Re-run installer
.\install.ps1  # Windows
./install.sh   # Linux/Mac
```

### Permission denied (Linux/macOS)
```bash
chmod +x install.sh run.sh
```

**📚 For detailed troubleshooting, see [INSTALLATION.md](INSTALLATION.md)**

</details>

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📝 Improve documentation
- 🚀 Submit pull requests

## ⭐ Show Your Support

If you find PathProwler useful, please consider:

- ⭐ Starring this repository
- 🐣 Sharing it with others
- 💬 Providing feedback

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Credits & Acknowledgments

Built with ❤️ using these amazing tools:

| Tool | Author | Description |
|------|--------|-------------|
| [Gobuster](https://github.com/OJ/gobuster) | OJ Reeves | Core scanning engine |
| [SecLists](https://github.com/danielmiessler/SecLists) | Daniel Miessler | Wordlists |
| [Textual](https://github.com/Textualize/textual) | Textualize | TUI framework |
| [Rich](https://github.com/Textualize/rich) | Will McGugan | Terminal formatting |

---

<div align="center">

### 🐾 Happy Prowling! 🎯

**Made with ❤️ for the security community**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/pathprowler?style=social)](https://github.com/yourusername/pathprowler/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/pathprowler?style=social)](https://github.com/yourusername/pathprowler/network/members)

[Report Bug](https://github.com/yourusername/pathprowler/issues) • [Request Feature](https://github.com/yourusername/pathprowler/issues) • [Documentation](https://github.com/yourusername/pathprowler/wiki)

</div>
