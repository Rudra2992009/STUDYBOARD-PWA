# STUDYBOARD PWA - Setup Script for Windows

Write-Host "======================================" -ForegroundColor Green
Write-Host "STUDYBOARD PWA - Setup Script" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""

# Check Python installation
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "[2/6] Creating virtual environment..." -ForegroundColor Cyan
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists" -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "[3/6] Activating virtual environment..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host ""
Write-Host "[4/6] Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# Install dependencies
Write-Host ""
Write-Host "[5/6] Installing Python dependencies..." -ForegroundColor Cyan
Set-Location backend
pip install -r requirements.txt
Set-Location ..

# Create necessary directories
Write-Host ""
Write-Host "[6/6] Creating directories..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path "generated_images" | Out-Null
New-Item -ItemType Directory -Force -Path "models" | Out-Null

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Activate virtual environment: .\venv\Scripts\Activate.ps1"
Write-Host "2. Start backend: cd backend; python server.py"
Write-Host "3. Open browser: http://localhost:5000"
Write-Host ""
Write-Host "Note: First run will download models (~4GB)" -ForegroundColor Cyan
Write-Host "This may take 10-30 minutes depending on internet speed." -ForegroundColor Cyan
Write-Host ""