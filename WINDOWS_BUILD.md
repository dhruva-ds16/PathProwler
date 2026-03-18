# Building PathProwler on Windows

## Prerequisites

1. **Install Go**
   - Download from: https://go.dev/dl/
   - Install Go 1.19 or higher
   - Verify: `go version`

2. **Install Feroxbuster**
   - Download from: https://github.com/epi052/feroxbuster/releases
   - Or install via Cargo: `cargo install feroxbuster`

## Build Steps

```powershell
# Navigate to project directory
cd C:\Users\5147382\Automation

# Download dependencies
go mod download

# Generate go.sum
go mod tidy

# Build
go build -o pathprowler.exe .

# Run
.\pathprowler.exe
```

## Quick Build Script

Save as `build.ps1`:

```powershell
Write-Host "🐾 Building PathProwler (Go Edition)..." -ForegroundColor Cyan
Write-Host ""

# Check if Go is installed
if (!(Get-Command go -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Go not found! Please install Go 1.19+" -ForegroundColor Red
    Write-Host "Download from: https://go.dev/dl/" -ForegroundColor Yellow
    exit 1
}

# Get dependencies
Write-Host "📦 Downloading dependencies..." -ForegroundColor Yellow
go mod download
go mod tidy

# Build
Write-Host "🔨 Building..." -ForegroundColor Yellow
go build -o pathprowler.exe .

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Build successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Run with: .\pathprowler.exe" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit 1
}
```

## Run

```powershell
.\pathprowler.exe
```

## Cross-Compile for Linux/Mac

```powershell
# Linux
$env:GOOS="linux"; $env:GOARCH="amd64"; go build -o pathprowler-linux

# macOS
$env:GOOS="darwin"; $env:GOARCH="amd64"; go build -o pathprowler-macos
```
