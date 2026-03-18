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
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Build failed!" -ForegroundColor Red
    exit 1
}
