# Gobuster Pro - Interactive TUI Dashboard

A beautiful, interactive terminal user interface for gobuster directory busting and vhost scanning.

## Features

### 🎨 Interactive Dashboard
- **Real-time monitoring** - Watch scans progress live
- **Multi-tabbed interface** - Separate views for results, logs, and individual scans
- **Live statistics** - Track directories, files, and vhosts found
- **Color-coded output** - Easy to read status codes and results

### ⚡ Powerful Scanning
- **Parallel scanning** - Run directory, file, and vhost scans simultaneously
- **Configurable options** - Threads, timeouts, status codes, extensions
- **Recursive scanning** - Deep directory enumeration
- **Export results** - Save to JSON for further analysis

### 🎯 Easy to Use
- **Keyboard shortcuts** - Quick access to all functions
- **Form-based config** - No command-line arguments needed
- **Live log streaming** - See gobuster output in real-time
- **Organized results** - Clean table view with all findings

## Quick Start

### Automated Installation (Recommended)

**Windows (PowerShell):**
```powershell
.\install.ps1
```

**Linux/macOS (Bash):**
```bash
chmod +x install.sh
./install.sh
```

The installer will:
- ✅ Check Python and gobuster installation
- ✅ Create a virtual environment
- ✅ Install all dependencies
- ✅ Offer to run the TUI immediately

### Manual Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

**See [INSTALLATION.md](INSTALLATION.md) for detailed installation instructions.**

## Usage

### Start the Dashboard

**Using run scripts (recommended):**
```bash
.\run.ps1    # Windows
./run.sh     # Linux/Mac
```

**Or manually:**
```bash
python gobuster_tui.py
```

### Keyboard Shortcuts
- `s` - Start scan
- `x` - Stop scan
- `e` - Export results
- `q` - Quit application
- `Tab` - Navigate between tabs
- `Arrow keys` - Navigate interface

### Configuration

Fill in the form on the left panel:

1. **Target URL** - The website to scan (e.g., http://target.com)
2. **Wordlist Directory** - Path to SecLists (default: /usr/share/wordlists/seclists)
3. **Threads** - Number of concurrent threads (default: 50)
4. **Timeout** - Request timeout in seconds (default: 10)
5. **Extensions** - File extensions to search (e.g., php,html,txt)
6. **Status Codes** - HTTP codes to match (default: 200,204,301,302,307,401,403)
7. **Scan Mode** - Choose what to scan:
   - All (Dir + Files + VHost)
   - Directories Only
   - Files Only
   - VHost Only
8. **Domain** - Required for VHost scanning (e.g., target.com)
9. **Recursive** - Enable recursive directory scanning
10. **Verbose** - Show detailed output

### Tabs

- **📋 Results** - Combined table of all findings
- **📝 Console Log** - General application logs
- **📊 Directory Scan** - Live directory scan output
- **📄 File Scan** - Live file scan output
- **🌐 VHost Scan** - Live vhost scan output

## Screenshots

### Main Dashboard
```
┌─────────────────────────────────────────────────────────────────────┐
│ Gobuster Pro - Interactive TUI Dashboard                           │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────┐ ┌─────────────────────────────────────────────┐│
│ │ 📊 Statistics   │ │ 📋 Results                                  ││
│ │                 │ │ ┌───────────────────────────────────────┐   ││
│ │ Status: Running │ │ │Type │Path    │Status│Size │Full URL  │   ││
│ │ Elapsed: 45s    │ │ │Dir  │/admin  │200   │1234 │http://...│   ││
│ │                 │ │ │File │/config │403   │567  │http://...│   ││
│ │ 📁 Dirs: 12     │ │ └───────────────────────────────────────┘   ││
│ │ 📄 Files: 8     │ │                                             ││
│ │ 🌐 VHosts: 3    │ │                                             ││
│ │ Total: 23       │ │                                             ││
│ └─────────────────┘ └─────────────────────────────────────────────┘│
│ ┌─────────────────┐                                                 │
│ │ 🎯 Config       │                                                 │
│ │ [Input fields]  │                                                 │
│ │ [🚀 Start Scan] │                                                 │
│ └─────────────────┘                                                 │
└─────────────────────────────────────────────────────────────────────┘
```

## Output

Results are saved to timestamped directories:
```
gobuster_results_20260317_173045/
├── directories.txt    # Raw gobuster directory output
├── files.txt         # Raw gobuster file output
├── vhosts.txt        # Raw gobuster vhost output
└── results.json      # Structured JSON export
```

## Tips

1. **Start with default settings** - They work well for most targets
2. **Increase threads** for faster scans (100-200 on fast networks)
3. **Use recursive mode** to find deeply nested directories
4. **Export results** before closing to save your findings
5. **Monitor the Console Log tab** for errors and warnings
6. **Use VHost scanning** when testing virtual host configurations

## Troubleshooting

### "Gobuster not found"
Install gobuster:
```bash
# Debian/Ubuntu
sudo apt install gobuster

# Or with Go
go install github.com/OJ/gobuster/v3@latest
```

### "Missing wordlists"
Install SecLists:
```bash
git clone https://github.com/danielmiessler/SecLists.git /usr/share/wordlists/seclists
```

### Scan not starting
- Check that target URL includes http:// or https://
- Verify wordlist directory path is correct
- Ensure gobuster is in your PATH

## Advanced Usage

### Custom Wordlists
Change the wordlist directory to use your own wordlists. The tool expects:
- `Discovery/Web-Content/raft-medium-directories.txt`
- `Discovery/Web-Content/raft-medium-files.txt`
- `Discovery/DNS/subdomains-top1million-5000.txt`

### Integration with Burp Suite
The CLI version (`gobuster_scan.py`) supports proxy settings:
```bash
python gobuster_scan.py -u http://target.com -p http://127.0.0.1:8080
```

## Comparison: CLI vs TUI

| Feature | CLI (`gobuster_scan.py`) | TUI (`gobuster_tui.py`) |
|---------|-------------------------|------------------------|
| Interactive | ❌ | ✅ |
| Real-time monitoring | ❌ | ✅ |
| Multiple output formats | ✅ (JSON, CSV, HTML) | ✅ (JSON) |
| Proxy support | ✅ | ❌ (coming soon) |
| Custom User-Agent | ✅ | ❌ (coming soon) |
| Ease of use | Medium | Easy |
| Automation friendly | ✅ | ❌ |

Use **CLI** for automation and scripting.  
Use **TUI** for interactive exploration and monitoring.

## License

This tool is for authorized security testing only. Always obtain permission before scanning.
