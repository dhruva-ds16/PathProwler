# PathProwler - Run Script for Windows
# Prowl through paths and discover hidden treasures 🐾
# This script runs the TUI using the virtual environment

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "[!] ERROR: Virtual environment not found" -ForegroundColor Red
    Write-Host "[!] Please run the installation script first: .\install.ps1" -ForegroundColor Red
    exit 1
}

# Run the TUI
Write-Host "[*] Starting PathProwler TUI..." -ForegroundColor Cyan
Write-Host ""
& "venv\Scripts\python.exe" pathprowler_tui.py
