# Tia Interpreter Windows One-Liner Installer
# This script downloads and runs the Tia Windows Installer from GitHub

# Define the repository and branch
$repo = "SynTia-OI/tia-interpreter"
$branch = "development"
$installerPath = "installers/tia-windows-installer.ps1"

# Create the raw GitHub URL
$url = "https://raw.githubusercontent.com/$repo/$branch/$installerPath"

# PowerShell one-liner to download and execute the installer
Write-Host "Downloading and running Tia Interpreter installer from $url"
Write-Host "You can use this one-liner to install Tia Interpreter:"
Write-Host ""
Write-Host "Invoke-WebRequest -Uri `"$url`" -UseBasicParsing | Invoke-Expression"
Write-Host ""

# Ask for confirmation before proceeding
$confirmation = Read-Host "Do you want to run the installer now? (y/n)"
if ($confirmation -eq 'y') {
    # Download and execute the installer
    try {
        Invoke-WebRequest -Uri $url -UseBasicParsing | Invoke-Expression
    }
    catch {
        Write-Host "Error: Failed to download or execute the installer." -ForegroundColor Red
        Write-Host "Error details: $_" -ForegroundColor Red
        Write-Host "Please check your internet connection and try again." -ForegroundColor Red
    }
}
else {
    Write-Host "Installation cancelled. You can run the installer later using the one-liner above." -ForegroundColor Yellow
}
