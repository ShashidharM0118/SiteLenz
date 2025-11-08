# Wireless Debugging Setup Script for Flutter
# Save as: setup_wireless.ps1

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     Flutter Wireless Debugging Setup - SiteLenz App       ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Function to check if ADB is installed
function Test-ADB {
    try {
        $null = adb version
        return $true
    } catch {
        return $false
    }
}

# Check ADB installation
if (-not (Test-ADB)) {
    Write-Host "❌ ADB is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Android SDK Platform Tools" -ForegroundColor Yellow
    Write-Host "Download from: https://developer.android.com/studio/releases/platform-tools" -ForegroundColor Yellow
    exit
}

Write-Host "✓ ADB found" -ForegroundColor Green
Write-Host ""

# Step 1: Check for USB-connected devices
Write-Host "Step 1: Checking for USB-connected devices..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

$devices = adb devices | Select-String -Pattern "\tdevice$"

if ($devices.Count -eq 0) {
    Write-Host "❌ No devices found via USB" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please:" -ForegroundColor Yellow
    Write-Host "  1. Connect your phone via USB cable" -ForegroundColor White
    Write-Host "  2. Enable USB Debugging in Developer Options" -ForegroundColor White
    Write-Host "  3. Accept the USB debugging prompt on your phone" -ForegroundColor White
    Write-Host "  4. Run this script again" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit
}

Write-Host "✓ Device connected via USB" -ForegroundColor Green
adb devices
Write-Host ""

# Step 2: Enable TCP/IP mode
Write-Host "Step 2: Enabling wireless debugging (TCP/IP mode)..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

adb tcpip 5555
Start-Sleep -Seconds 3

Write-Host "✓ TCP/IP mode enabled on port 5555" -ForegroundColor Green
Write-Host ""

# Step 3: Get device IP address
Write-Host "Step 3: Getting device IP address..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

try {
    $ipOutput = adb shell ip addr show wlan0 2>$null
    $ipMatch = $ipOutput | Select-String -Pattern "inet\s+(\d+\.\d+\.\d+\.\d+)" | Select-Object -First 1
    
    if ($ipMatch) {
        $ip = $ipMatch.Matches.Groups[1].Value
        Write-Host "✓ Device IP Address: $ip" -ForegroundColor Green
    } else {
        Write-Host "⚠ Could not automatically detect IP address" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Please manually find your phone's IP address:" -ForegroundColor White
        Write-Host "  Settings → About Phone → Status → IP Address" -ForegroundColor White
        Write-Host "  OR" -ForegroundColor White
        Write-Host "  Settings → Wi-Fi → Connected Network → Advanced" -ForegroundColor White
        Write-Host ""
        $ip = Read-Host "Enter your phone's IP address (e.g., 192.168.1.100)"
    }
} catch {
    Write-Host "⚠ Could not automatically detect IP address" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please find your phone's IP address from:" -ForegroundColor White
    Write-Host "  Settings → About Phone → Status → IP Address" -ForegroundColor White
    Write-Host ""
    $ip = Read-Host "Enter your phone's IP address (e.g., 192.168.1.100)"
}

Write-Host ""

# Step 4: Disconnect USB
Write-Host "Step 4: Disconnect USB cable" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "Please DISCONNECT the USB cable from your phone now." -ForegroundColor White
Write-Host ""
Read-Host "Press Enter after disconnecting USB cable"
Write-Host ""

# Step 5: Connect wirelessly
Write-Host "Step 5: Connecting wirelessly to $ip..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray

$connectResult = adb connect "${ip}:5555" 2>&1
Write-Host $connectResult

if ($connectResult -like "*connected*" -or $connectResult -like "*already connected*") {
    Write-Host "✓ Successfully connected wirelessly!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to connect wirelessly" -ForegroundColor Red
    Write-Host "Please check:" -ForegroundColor Yellow
    Write-Host "  • Both devices are on the same Wi-Fi network" -ForegroundColor White
    Write-Host "  • IP address is correct" -ForegroundColor White
    Write-Host "  • Wireless debugging is enabled on phone" -ForegroundColor White
}

Start-Sleep -Seconds 2
Write-Host ""

# Step 6: Verify connection
Write-Host "Step 6: Verifying connection..." -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "Connected ADB devices:" -ForegroundColor Cyan
adb devices
Write-Host ""

# Check Flutter
Write-Host "Checking Flutter devices..." -ForegroundColor Cyan
cd e:\projects\major_project\flutter_app
flutter devices

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                    Setup Complete! 🎉                      ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Save IP for future use
$ip | Out-File -FilePath ".\last_phone_ip.txt" -Encoding UTF8
Write-Host "✓ Phone IP saved to: last_phone_ip.txt" -ForegroundColor Green
Write-Host ""

# Quick reference commands
Write-Host "Quick Reference Commands:" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""
Write-Host "  Connect:      " -NoNewline -ForegroundColor White
Write-Host "adb connect ${ip}:5555" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Disconnect:   " -NoNewline -ForegroundColor White
Write-Host "adb disconnect ${ip}:5555" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Run Flutter:  " -NoNewline -ForegroundColor White
Write-Host "flutter run" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Hot Reload:   " -NoNewline -ForegroundColor White
Write-Host "Press 'r' in terminal" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Hot Restart:  " -NoNewline -ForegroundColor White
Write-Host "Press 'R' in terminal" -ForegroundColor Yellow
Write-Host ""

# Create quick connect script
$quickConnectScript = @"
# Quick Connect Script - Generated by setup_wireless.ps1
Write-Host "Connecting to phone at ${ip}:5555..." -ForegroundColor Cyan
adb connect ${ip}:5555
Start-Sleep -Seconds 2
Write-Host ""
Write-Host "Connected devices:" -ForegroundColor Green
adb devices
Write-Host ""
Write-Host "Ready! Run 'flutter run' to start the app." -ForegroundColor Green
"@

$quickConnectScript | Out-File -FilePath ".\quick_connect.ps1" -Encoding UTF8
Write-Host "✓ Quick connect script created: quick_connect.ps1" -ForegroundColor Green
Write-Host "  Run this anytime to reconnect: " -NoNewline -ForegroundColor White
Write-Host ".\quick_connect.ps1" -ForegroundColor Yellow
Write-Host ""

Write-Host "Next time, just run: " -NoNewline -ForegroundColor White
Write-Host ".\quick_connect.ps1" -ForegroundColor Yellow -NoNewline
Write-Host " to connect!" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"
