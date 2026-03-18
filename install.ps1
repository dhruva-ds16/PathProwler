# PathProwler - Installation Script for Windows
# Prowl through paths and discover hidden treasures 🐾
# This script creates a virtual environment, installs dependencies, and runs the TUI

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PathProwler - Installation Script  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "[*] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[+] Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[!] ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "[!] Please install Python 3.8+ from https://www.python.org/" -ForegroundColor Red
    exit 1
}

# Check if gobuster is installed
Write-Host "[*] Checking gobuster installation..." -ForegroundColor Yellow
try {
    $gobusterVersion = gobuster version 2>&1
    Write-Host "[+] Found: gobuster" -ForegroundColor Green
} catch {
    Write-Host "[!] WARNING: gobuster is not installed or not in PATH" -ForegroundColor Yellow
    Write-Host "[!] Please install gobuster from https://github.com/OJ/gobuster" -ForegroundColor Yellow
    Write-Host "[!] The tool will not work without gobuster!" -ForegroundColor Yellow
    Write-Host ""
}

# Check if requirements.txt exists
if (-not (Test-Path "requirements.txt")) {
    Write-Host "[!] ERROR: requirements.txt not found" -ForegroundColor Red
    Write-Host "[!] Please ensure you're running this script from the Automation directory" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "[*] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "[*] Virtual environment already exists, skipping creation..." -ForegroundColor Cyan
} else {
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[+] Virtual environment created successfully" -ForegroundColor Green
    } else {
        Write-Host "[!] ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment and install dependencies
Write-Host ""
Write-Host "[*] Installing dependencies..." -ForegroundColor Yellow
& "venv\Scripts\python.exe" -m pip install --upgrade pip | Out-Null
& "venv\Scripts\pip.exe" install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "[+] Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "[!] ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Installation complete
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Installation Complete!              " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To run PathProwler TUI:" -ForegroundColor Cyan
Write-Host "  .\run.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To run CLI version:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\python.exe pathprowler.py -u http://target.com -m all" -ForegroundColor White
Write-Host ""
Write-Host "To activate the virtual environment manually:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""

# Ask if user wants to run the TUI now
Write-Host "Would you like to run the TUI now? (Y/N): " -ForegroundColor Yellow -NoNewline
$response = Read-Host

if ($response -eq "Y" -or $response -eq "y") {
    Write-Host ""
    Write-Host "[*] Starting PathProwler TUI..." -ForegroundColor Cyan
    Write-Host ""
    & "venv\Scripts\python.exe" pathprowler_tui.py
} else {
    Write-Host ""
    Write-Host "[*] You can run the TUI anytime with: .\run.ps1" -ForegroundColor Cyan
}
