"""
Configuration Appium pour Swag Labs Mobile APK
Supports multiple AVD via udid parameter
"""

# Capacités de base (sans udid - Appium choisira le premier disponible)
BASE_CAPS = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "app": "apps/sauce.apk",
    "appPackage": "com.swaglabsmobileapp",
    "appActivity": "com.swaglabsmobileapp.MainActivity",
    "newCommandTimeout": 300,
}

# Configurations spécifiques par AVD
AVD_CONFIGS = {
    "emulator-5556": {  # Petit téléphone 4.7" (720x1280)
        "deviceName": "Pixel_4_7_Small",
        "udid": "emulator-5556",
    },
    "emulator-5554": {  # Téléphone moyen 6.4" (1080x2400)
        "deviceName": "Pixel_6_4_Medium",
        "udid": "emulator-5554",
    },
    "emulator-5558": {  # Tablette 10" (2560x1600)
        "deviceName": "Pixel_Tablet_10",
        "udid": "emulator-5558",
    },
}

# Capacités par défaut (sans spécifier udid)
caps = {**BASE_CAPS, "deviceName": "Android Emulator"}

# Pour cibler un AVD spécifique, utiliser :
# caps = {**BASE_CAPS, **AVD_CONFIGS["emulator-5556"]}

APPIUM_SERVER = "http://127.0.0.1:4723"