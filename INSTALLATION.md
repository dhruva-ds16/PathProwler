# PathProwler - Installation Guide

Complete installation instructions for Windows, Linux, and macOS.

## Quick Start

### Windows (PowerShell)
```powershell
# Run installation script
.\install.ps1

# Or run manually
python -m venv venv
.\venv\Scripts\pip.exe install -r requirements.txt
.\run.ps1
```

### Linux/macOS (Bash)
```bash
# Make scripts executable
chmod +x install.sh run.sh

# Run installation script
./install.sh

# Or run manually
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./run.sh
```

## Prerequisites

### 1. Python 3.8+
**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-venv python3-pip

# Arch Linux
sudo pacman -S python python-pip

# Fedora
sudo dnf install python3 python3-pip
```

**macOS:**
```bash
# Using Homebrew
brew install python3
```

### 2. Gobuster
**Windows:**
- Download from [GitHub Releases](https://github.com/OJ/gobuster/releases)
- Extract `gobuster.exe` to a directory in your PATH
- Or use Chocolatey: `choco install gobuster`

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install gobuster

# Arch Linux
sudo pacman -S gobuster

# Fedora
sudo dnf install gobuster

# From source
go install github.com/OJ/gobuster/v3@latest
```

**macOS:**
```bash
# Using Homebrew
brew install gobuster
```

### 3. SecLists Wordlists (Optional but Recommended)
**Windows:**
```powershell
# Clone to default location
git clone https://github.com/danielmiessler/SecLists.git C:\wordlists\seclists
```

**Linux/macOS:**
```bash
# Ubuntu/Debian
sudo apt install seclists

# Or clone manually
sudo git clone https://github.com/danielmiessler/SecLists.git /usr/share/wordlists/seclists
```

## Installation Methods

### Method 1: Automated Installation (Recommended)

#### Windows
```powershell
# Navigate to the Automation directory
cd C:\Users\5147382\Automation

# Run installation script
.\install.ps1

# Follow the prompts
```

**What it does:**
1. ✅ Checks Python installation
2. ✅ Checks gobuster installation
3. ✅ Creates virtual environment (`venv/`)
4. ✅ Upgrades pip
5. ✅ Installs all dependencies from `requirements.txt`
6. ✅ Offers to run the TUI immediately

#### Linux/macOS
```bash
# Navigate to the Automation directory
cd ~/Automation

# Make scripts executable
chmod +x install.sh run.sh

# Run installation script
./install.sh

# Follow the prompts
```

### Method 2: Manual Installation

#### Windows
```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Upgrade pip
python -m pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the TUI
python pathprowler_tui.py

# Or run the CLI
python pathprowler.py -u http://target.com -m all
```

#### Linux/macOS
```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the TUI
python pathprowler_tui.py

# Or run the CLI
python pathprowler.py -u http://target.com -m all
```

### Method 3: System-Wide Installation (Not Recommended)

```bash
# Install dependencies globally (not recommended)
pip install textual rich

# Run directly
python pathprowler_tui.py
```

**Note:** System-wide installation is not recommended as it can cause dependency conflicts.

## Running the Tools

### TUI (Terminal User Interface)

#### Windows
```powershell
# Using run script (recommended)
.\run.ps1

# Or manually
.\venv\Scripts\python.exe pathprowler_tui.py
```

#### Linux/macOS
```bash
# Using run script (recommended)
./run.sh

# Or manually
./venv/bin/python pathprowler_tui.py
```

### CLI (Command Line Interface)

#### Windows
```powershell
# Activate venv first
.\venv\Scripts\Activate.ps1

# Run CLI
python pathprowler.py -u http://target.com -m all -d target.com

# Or without activating
.\venv\Scripts\python.exe pathprowler.py -u http://target.com -m all
```

#### Linux/macOS
```bash
# Activate venv first
source venv/bin/activate

# Run CLI
python pathprowler.py -u http://target.com -m all -d target.com

# Or without activating
./venv/bin/python pathprowler.py -u http://target.com -m all
```

## Verification

### Check Installation
```bash
# Check Python
python --version  # or python3 --version

# Check gobuster
gobuster version

# Check virtual environment
ls venv/  # Should see Scripts/ (Windows) or bin/ (Linux/Mac)

# Check installed packages
.\venv\Scripts\pip.exe list  # Windows
./venv/bin/pip list          # Linux/Mac
```

### Test Run
```bash
# Test TUI (should open dashboard)
.\run.ps1      # Windows
./run.sh       # Linux/Mac

# Test CLI (should show help)
python pathprowler.py --help
```

## Troubleshooting

### Python Not Found
**Windows:**
```powershell
# Check if Python is in PATH
where python

# If not found, add to PATH or reinstall Python with "Add to PATH" checked
```

**Linux/macOS:**
```bash
# Check if Python is installed
which python3

# Install if missing
sudo apt install python3  # Ubuntu/Debian
brew install python3      # macOS
```

### Gobuster Not Found
```bash
# Check if gobuster is in PATH
gobuster version

# If not found, install gobuster (see Prerequisites section)
```

### Virtual Environment Creation Failed
```bash
# Ensure venv module is installed
python -m ensurepip --upgrade

# Linux: Install python3-venv
sudo apt install python3-venv
```

### Permission Denied (Linux/macOS)
```bash
# Make scripts executable
chmod +x install.sh run.sh

# If still issues, run with bash
bash install.sh
bash run.sh
```

### PowerShell Execution Policy (Windows)
```powershell
# If you get "execution policy" error
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run with bypass
powershell -ExecutionPolicy Bypass -File install.ps1
```

### Dependencies Installation Failed
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Try installing dependencies one by one
pip install textual
pip install rich

# Check for errors
pip install -r requirements.txt --verbose
```

### TUI Not Displaying Correctly
```bash
# Update terminal
# Windows: Use Windows Terminal (recommended)
# Linux: Ensure terminal supports Unicode and colors

# Update dependencies
pip install --upgrade textual rich
```

## Directory Structure After Installation

```
Automation/
├── venv/                          # Virtual environment (created)
│   ├── Scripts/                   # Windows
│   │   ├── python.exe
│   │   ├── pip.exe
│   │   └── Activate.ps1
│   └── bin/                       # Linux/Mac
│       ├── python
│       ├── pip
│       └── activate
├── gobuster_scan.py               # CLI tool
├── gobuster_tui.py                # TUI tool
├── requirements.txt               # Dependencies
├── install.ps1                    # Windows installer
├── install.sh                     # Linux/Mac installer
├── run.ps1                        # Windows runner
├── run.sh                         # Linux/Mac runner
├── README_TUI.md                  # TUI documentation
├── INSTALLATION.md                # This file
├── SUBDOMAIN_ENUMERATION.md       # Subdomain guide
├── DIRECTORY_NAMING.md            # Directory naming guide
└── DNS_USAGE.md                   # DNS usage guide
```

## Updating

### Update Dependencies
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # Linux/Mac

# Update packages
pip install --upgrade textual rich

# Or reinstall from requirements
pip install -r requirements.txt --upgrade
```

### Update Gobuster
```bash
# Windows (Chocolatey)
choco upgrade gobuster

# Linux
sudo apt update && sudo apt upgrade gobuster  # Ubuntu/Debian
sudo pacman -Syu gobuster                      # Arch

# macOS
brew upgrade gobuster

# From source
go install github.com/OJ/gobuster/v3@latest
```

### Update Scripts
```bash
# Pull latest changes if using git
git pull origin main

# Or download latest versions manually
```

## Uninstallation

### Remove Virtual Environment
```bash
# Windows
Remove-Item -Recurse -Force venv

# Linux/Mac
rm -rf venv
```

### Remove Everything
```bash
# Windows
Remove-Item -Recurse -Force C:\Users\5147382\Automation

# Linux/Mac
rm -rf ~/Automation
```

### Keep Results, Remove Tools
```bash
# Move results to safe location
mv pathprowler_* ~/scan_results/

# Remove tool files
rm pathprowler.py pathprowler_tui.py requirements.txt *.ps1 *.sh *.md
rm -rf venv
```

## Advanced Configuration

### Custom Wordlist Location
```bash
# Edit gobuster_scan.py or use -w flag
python pathprowler.py -u http://target.com -w /custom/path/to/wordlists
```

### Proxy Configuration
```bash
# Use with Burp Suite
python pathprowler.py -u http://target.com -p http://127.0.0.1:8080
```

### Custom Python Version
```bash
# Use specific Python version
python3.11 -m venv venv
./venv/bin/python --version
```

## Docker Installation (Alternative)

### Create Dockerfile
```dockerfile
FROM python:3.11-slim

# Install gobuster
RUN apt-get update && \
    apt-get install -y gobuster git && \
    rm -rf /var/lib/apt/lists/*

# Clone SecLists
RUN git clone https://github.com/danielmiessler/SecLists.git /usr/share/wordlists/seclists

# Copy application
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Run TUI
CMD ["python", "pathprowler_tui.py"]
```

### Build and Run
```bash
# Build image
docker build -t pathprowler .

# Run TUI
docker run -it pathprowler

# Run CLI
docker run -it pathprowler python pathprowler.py -u http://target.com -m all
```

## Support

### Getting Help
- Check documentation in `README_TUI.md`
- Review usage guides in `SUBDOMAIN_ENUMERATION.md`
- Check troubleshooting section above

### Common Issues
1. **"Python not found"** → Install Python and add to PATH
2. **"Gobuster not found"** → Install gobuster
3. **"Permission denied"** → Make scripts executable (`chmod +x`)
4. **"Execution policy"** → Set PowerShell execution policy
5. **"Module not found"** → Activate venv or reinstall dependencies

## Summary

### Quick Installation (Windows)
```powershell
.\install.ps1
.\run.ps1
```

### Quick Installation (Linux/Mac)
```bash
chmod +x install.sh run.sh
./install.sh
./run.sh
```

That's it! You're ready to use Gobuster Pro! 🎉
