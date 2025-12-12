"""
Script pour inspecter la structure de l'écran de l'app Swag Labs
"""
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config import caps, APPIUM_SERVER
import time

options = UiAutomator2Options()
options.platform_name = caps["platformName"]
options.automation_name = caps["automationName"]
options.device_name = caps["deviceName"]
options.app = caps["app"]
options.app_package = caps["appPackage"]
options.app_activity = caps["appActivity"]
options.new_command_timeout = 300

driver = webdriver.Remote(APPIUM_SERVER, options=options)

try:
    # Attendre que l'app charge
    time.sleep(3)
    
    # Obtenir la source de la page
    page_source = driver.page_source
    
    # Sauvegarder dans un fichier
    with open("page_structure.xml", "w", encoding="utf-8") as f:
        f.write(page_source)
    
    print("✓ Structure de la page sauvegardée dans 'page_structure.xml'")
    print("\nÉléments trouvés:")
    
    # Chercher les boutons avec "menu" ou "login"
    if "menu" in page_source.lower():
        print("  - Éléments contenant 'menu' détectés")
    if "login" in page_source.lower():
        print("  - Éléments contenant 'login' détectés")
    
    # Afficher tous les éléments cliquables
    all_elements = driver.find_elements("xpath", "//*[@clickable='true']")
    print(f"\n✓ Total d'éléments cliquables: {len(all_elements)}")
    
    for i, elem in enumerate(all_elements[:10]):  # Afficher les 10 premiers
        try:
            text = elem.text or elem.get_attribute("content-desc") or "N/A"
            print(f"  {i+1}. {text}")
        except:
            pass
    
finally:
    driver.quit()
    print("\n✓ Session fermée")
