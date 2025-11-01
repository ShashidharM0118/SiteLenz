# Flutter Installation and APK Build Script for Windows
# Run this in PowerShell

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "SiteLenz Flutter App Builder" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Flutter is installed
Write-Host "Checking Flutter installation..." -ForegroundColor Yellow
$flutterInstalled = Get-Command flutter -ErrorAction SilentlyContinue

if ($flutterInstalled) {
    Write-Host "✅ Flutter is already installed!" -ForegroundColor Green
    flutter --version
} else {
    Write-Host "❌ Flutter is not installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Flutter using ONE of these methods:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "METHOD 1: Using Chocolatey (Recommended)" -ForegroundColor Cyan
    Write-Host "  1. Open PowerShell as Admin" -ForegroundColor White
    Write-Host "  2. Run: choco install flutter" -ForegroundColor White
    Write-Host ""
    Write-Host "METHOD 2: Manual Installation" -ForegroundColor Cyan
    Write-Host "  1. Download: https://flutter.dev/docs/get-started/install/windows" -ForegroundColor White
    Write-Host "  2. Extract to C:\src\flutter" -ForegroundColor White
    Write-Host "  3. Add to PATH: C:\src\flutter\bin" -ForegroundColor White
    Write-Host ""
    Write-Host "After installation, run this script again!" -ForegroundColor Yellow
    Write-Host ""
    
    # Ask if user wants to open download page
    $response = Read-Host "Open Flutter download page? (y/n)"
    if ($response -eq 'y') {
        Start-Process "https://flutter.dev/docs/get-started/install/windows"
    }
    
    exit
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Setting up Flutter project..." -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Navigate to flutter app directory
$projectPath = "E:\projects\major_project\flutter_app"
if (Test-Path $projectPath) {
    Set-Location $projectPath
    Write-Host "✅ Project directory found" -ForegroundColor Green
} else {
    Write-Host "❌ Project directory not found: $projectPath" -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Running flutter doctor..." -ForegroundColor Yellow
flutter doctor

Write-Host ""
Write-Host "Getting dependencies..." -ForegroundColor Yellow
flutter pub get

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Building APK..." -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will take 5-10 minutes on first build..." -ForegroundColor Yellow
Write-Host ""

# Build release APK
flutter build apk --release

# Check if APK was created
$apkPath = "build\app\outputs\flutter-apk\app-release.apk"
if (Test-Path $apkPath) {
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host "✅ SUCCESS! APK Built Successfully!" -ForegroundColor Green
    Write-Host "=========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📱 APK Location:" -ForegroundColor Cyan
    Write-Host "   $projectPath\$apkPath" -ForegroundColor White
    Write-Host ""
    $apkSize = (Get-Item $apkPath).Length / 1MB
    Write-Host "📦 APK Size: $([math]::Round($apkSize, 2)) MB" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📲 Install on Android:" -ForegroundColor Yellow
    Write-Host "   1. Copy APK to your phone" -ForegroundColor White
    Write-Host "   2. Open APK file on phone" -ForegroundColor White
    Write-Host "   3. Allow installation from unknown sources" -ForegroundColor White
    Write-Host "   4. Install and enjoy!" -ForegroundColor White
    Write-Host ""
    
    # Ask if user wants to open folder
    $response = Read-Host "Open APK folder? (y/n)"
    if ($response -eq 'y') {
        explorer "build\app\outputs\flutter-apk\"
    }
} else {
    Write-Host ""
    Write-Host "=========================================" -ForegroundColor Red
    Write-Host "❌ APK Build Failed" -ForegroundColor Red
    Write-Host "=========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Check errors above and try:" -ForegroundColor Yellow
    Write-Host "  flutter doctor" -ForegroundColor White
    Write-Host "  flutter doctor --android-licenses" -ForegroundColor White
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
