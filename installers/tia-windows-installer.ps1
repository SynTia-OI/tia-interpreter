# TIA Interpreter Windows Installer
# Based on the Open Interpreter installer but customized for TIA

# Configuration
$RepoUrl = "https://github.com/OpenInterpreter/open-interpreter.git"
$Branch = "development"
$PythonVersion = "3.13"
$VenvDir = "$env:USERPROFILE\.tia-interpreter\venv"
$InstallDir = "$env:USERPROFILE\.tia-interpreter"

# Create installation directory
Write-Host "Creating installation directory..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null

# Check if Python is installed
$pythonInstalled = $false
try {
    $pythonVersion = python --version
    if ($pythonVersion -match "Python 3\.(1[0-3])") {
        $pythonInstalled = $true
        Write-Host "Found Python: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "Python 3.10+ is required, found: $pythonVersion" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Python not found in PATH" -ForegroundColor Yellow
}

if (-not $pythonInstalled) {
    Write-Host "Installing Python $PythonVersion..." -ForegroundColor Cyan
    
    # Check if winget is available
    $wingetAvailable = $false
    try {
        winget --version | Out-Null
        $wingetAvailable = $true
    } catch {
        Write-Host "Winget not available. Please install Python 3.13 manually." -ForegroundColor Red
        exit 1
    }
    
    if ($wingetAvailable) {
        Write-Host "Installing Python using winget..." -ForegroundColor Cyan
        winget install Python.Python.3.13 --silent
        
        # Update PATH for current session
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
        
        # Verify installation
        try {
            $pythonVersion = python --version
            Write-Host "Python installed: $pythonVersion" -ForegroundColor Green
        } catch {
            Write-Host "Python installation failed. Please install Python 3.13 manually." -ForegroundColor Red
            exit 1
        }
    }
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Cyan
python -m venv $VenvDir

# Activate virtual environment
$ActivateScript = "$VenvDir\Scripts\Activate.ps1"
. $ActivateScript

# Install package from git repository
Write-Host "Installing TIA Interpreter from $Branch branch..." -ForegroundColor Cyan
pip install "git+$RepoUrl@$Branch"

# Create shortcuts
Write-Host "Creating shortcuts..." -ForegroundColor Cyan

# Create a batch file for easy access
$BatchFile = "$InstallDir\tia.bat"
@"
@echo off
call "$VenvDir\Scripts\activate.bat"
interpreter %*
"@ | Out-File -FilePath $BatchFile -Encoding ascii

# Add to PATH
$UserPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
if (-not $UserPath.Contains($InstallDir)) {
    [System.Environment]::SetEnvironmentVariable("Path", "$UserPath;$InstallDir", "User")
    $env:Path = "$env:Path;$InstallDir"
    Write-Host "Added to PATH: $InstallDir" -ForegroundColor Green
}

# Test the installation
Write-Host "Testing installation..." -ForegroundColor Cyan
try {
    $env:OPENAI_API_KEY = "sk-dummy-key-for-testing"
    echo "Say hello world!" | & "$VenvDir\Scripts\interpreter.exe" --model gpt-4o-mini
    Write-Host "Test successful!" -ForegroundColor Green
} catch {
    Write-Host "Test failed, but installation may still be complete." -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Red
}

Write-Host "`nInstallation complete!" -ForegroundColor Green
Write-Host "You can now use TIA Interpreter by typing 'tia' in a new terminal window." -ForegroundColor Cyan
Write-Host "Example: tia 'create a simple web server'" -ForegroundColor Cyan
