# Script pour démarrer Appium avec les variables Android configurées

# Définir les variables d'environnement Android
$env:ANDROID_HOME = "C:\Users\user\AppData\Local\Android\Sdk"
$env:ANDROID_SDK_ROOT = "C:\Users\user\AppData\Local\Android\Sdk"

# Afficher les variables (vérification)
Write-Host "ANDROID_HOME: $env:ANDROID_HOME" -ForegroundColor Green
Write-Host "ANDROID_SDK_ROOT: $env:ANDROID_SDK_ROOT" -ForegroundColor Green
Write-Host ""
Write-Host "Démarrage d'Appium sur le port 4723..." -ForegroundColor Yellow
Write-Host "Garde cette fenêtre ouverte pendant les tests." -ForegroundColor Yellow
Write-Host ""

# Démarrer Appium
appium --port 4723
