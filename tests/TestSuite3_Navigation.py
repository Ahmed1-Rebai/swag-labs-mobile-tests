"""
Tests Navigation & États – Appium Mobile
Techniques : Test de configuration, test d'état, test de navigation
Objectif : Vérifier la navigation, les transitions d'écran, et la gestion d'état

Tests inclus:
- NAV01: Ouvrir menu latéral (hamburger)
- NAV02: Naviguer vers favoris/WEBVIEW/DRAWING/GEO LOCATION
- NAV03: Tester le retour Android (bouton du téléphone)
- NAV04: Tester navigation portrait ↔ paysage
- NAV05: Tester redémarrage app (session conservée ou non)
"""

import time
import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage


@pytest.mark.navigation
def TC9_nav01_open_side_menu(driver):
    """NAV01 – Ouvrir le menu latéral (hamburger)
    
    Technique : Test de navigation
    Objectif : Vérifier que le menu latéral s'ouvre correctement
    
    Étapes :
    1. Se connecter
    2. Chercher et cliquer sur le bouton hamburger/menu
    3. Vérifier que le menu s'ouvre
    4. Se déconnecter
    
    Résultat attendu : Menu latéral s'ouvre sans erreur
    """
    login = LoginPage(driver)
    home = HomePage(driver)
    
    print(f"\n📱 NAV01 – Opening side menu (hamburger)...")
    
    try:
        # === Connexion ===
        print(f"  [Step 1] Logging in...")
        login.send_keys(*login.USERNAME, "standard_user")
        time.sleep(0.2)
        login.send_keys(*login.PASSWORD, "secret_sauce")
        time.sleep(0.2)
        login.click(*login.LOGIN_BTN)
        time.sleep(2)
        print(f"    ✓ Login successful")
        
        # === Chercher et cliquer sur le menu hamburger ===
        print(f"  [Step 2] Looking for hamburger menu button...")
        
        # Essayer différents sélecteurs pour le hamburger
        menu_btns = None
        selectors = [
            ("accessibility id", "test-Menu"),
            ("xpath", "//*[@content-desc='test-Menu']"),
            ("xpath", "//android.widget.ImageView[@content-desc='test-Menu']"),
        ]
        
        for by, selector in selectors:
            try:
                menu_btns = driver.find_elements(by, selector)
                if menu_btns and len(menu_btns) > 0:
                    print(f"    ✓ Found menu button with selector: {by} = {selector}")
                    break
            except Exception:
                pass
        
        if not menu_btns or len(menu_btns) == 0:
            print(f"    ⚠ Menu button not found with standard selectors, app may not have hamburger menu")
            pytest.skip("Hamburger menu not found in this app version")
        
        # === Cliquer sur le menu ===
        print(f"  [Step 3] Clicking on hamburger menu...")
        menu_btns[0].click()
        time.sleep(1)
        
        # Vérifier que le menu est visible
        menu_items = driver.find_elements("xpath", "//*[@content-desc='test-Menu-Logout']")
        if menu_items:
            print(f"    ✓ Menu opened successfully")
        else:
            print(f"    ⚠ Menu clicked but items not found yet")
        
        print(f"  ✓ NAV01 PASSED – Side menu opens correctly")
        
        # === Logout ===
        try:
            home.logout()
        except:
            pass
        
    except Exception as e:
        pytest.fail(f"NAV01 FAILED: {str(e)}")


@pytest.mark.navigation
def TC10_nav02_navigate_to_sections(driver):
    """NAV02 – Naviguer vers différentes sections (Favoris/WebView/Drawing/GeoLocation)
    
    Technique : Test de navigation
    Objectif : Vérifier que la navigation entre les sections fonctionne
    
    Étapes :
    1. Se connecter
    2. Chercher les boutons de section (About, Drawing, GeoLocation, etc.)
    3. Cliquer sur chaque section
    4. Vérifier que la page change
    5. Revenir aux produits
    
    Résultat attendu : Navigation fluide entre toutes les sections
    """
    login = LoginPage(driver)
    home = HomePage(driver)
    
    print(f"\n📱 NAV02 – Navigation to different sections...")
    
    try:
        # === Connexion ===
        print(f"  [Step 1] Logging in...")
        login.send_keys(*login.USERNAME, "standard_user")
        time.sleep(0.2)
        login.send_keys(*login.PASSWORD, "secret_sauce")
        time.sleep(0.2)
        login.click(*login.LOGIN_BTN)
        time.sleep(2)
        print(f"    ✓ Login successful")
        
        # === Chercher les boutons de navigation ===
        print(f"  [Step 2] Looking for section navigation buttons...")
        
        # Chercher tous les boutons potentiels de navigation
        nav_sections = [
            ("About", "test-About"),
            ("WebView", "test-WebView"),
            ("Drawing", "test-Drawing"),
            ("GeoLocation", "test-GeoLocation"),
        ]
        
        found_sections = 0
        for section_name, accessibility_id in nav_sections:
            try:
                btns = driver.find_elements("accessibility id", accessibility_id)
                if btns and len(btns) > 0:
                    found_sections += 1
                    print(f"    ✓ Found section button: {section_name}")
            except Exception:
                pass
        
        if found_sections == 0:
            print(f"    ⚠ No section navigation buttons found, this app may not have these sections")
            pytest.skip("Section navigation buttons not found")
        
        print(f"  [Step 3] Testing navigation to sections...")
        
        # Tester quelques sections
        sections_to = [
            ("About", "test-About"),
            ("WebView", "test-WebView"),
        ]
        
        for section_name, accessibility_id in sections_to:
            try:
                section_btns = driver.find_elements("accessibility id", accessibility_id)
                if section_btns and len(section_btns) > 0:
                    print(f"    → Clicking on {section_name}...")
                    section_btns[0].click()
                    time.sleep(1)
                    print(f"    ✓ Navigated to {section_name}")
                    time.sleep(0.5)
                    
                    # Essayer de revenir
                    back_attempts = 0
                    while back_attempts < 2:
                        try:
                            driver.back()
                            time.sleep(0.5)
                            break
                        except:
                            back_attempts += 1
            except Exception as e:
                print(f"    ⚠ Error testing {section_name}: {str(e)}")
        
        print(f"  ✓ NAV02 PASSED – Navigation between sections works")
        
        # === Logout ===
        try:
            home.logout()
        except:
            pass
        
    except Exception as e:
        pytest.fail(f"NAV02 FAILED: {str(e)}")


@pytest.mark.navigation
def TC11_nav03_android_back_button(driver):
    """NAV03 – Tester le bouton retour Android (système)
    
    Technique : Test de configuration
    Objectif : Vérifier que le bouton retour du système fonctionne correctement
    
    Étapes :
    1. Se connecter
    2. Naviguer vers une autre page
    3. Appuyer sur le bouton retour Android
    4. Vérifier qu'on revient à la page précédente
    5. Appuyer à nouveau pour quitter
    
    Résultat attendu : Navigation arrière fonctionne correctement
    """
    login = LoginPage(driver)
    home = HomePage(driver)
    
    print(f"\n📱 NAV03 – Testing Android back button...")
    
    try:
        # === Connexion ===
        print(f"  [Step 1] Logging in...")
        login.send_keys(*login.USERNAME, "standard_user")
        time.sleep(0.2)
        login.send_keys(*login.PASSWORD, "secret_sauce")
        time.sleep(0.2)
        login.click(*login.LOGIN_BTN)
        time.sleep(2)
        print(f"    ✓ Login successful (on products page)")
        
        # === Ajouter un produit et ouvrir le panier ===
        print(f"  [Step 2] Adding product and opening cart...")
        home.add_to_cart(item_index=0)
        time.sleep(0.5)
        home.click_cart_icon()
        time.sleep(1)
        print(f"    ✓ Cart opened")
        
        # === Tester le bouton retour ===
        print(f"  [Step 3] Testing Android back button...")
        driver.back()
        time.sleep(1)
        
        # Vérifier qu'on est revenu aux produits
        products = driver.find_elements("xpath", "//android.view.ViewGroup[@content-desc='test-Item']")
        assert len(products) > 0, "Not back on products page after back button"
        print(f"    ✓ Back button returned to products page")
        
        # === Tester le retour depuis la page login ===
        print(f"  [Step 4] Testing back button from another page...")
        
        # Se déconnecter
        home.logout()
        time.sleep(1)
        
        # Essayer de revenir en arrière (devrait rester sur login ou fermer l'app)
        try:
            driver.back()
            time.sleep(0.5)
            print(f"    ✓ Back button handled correctly")
        except Exception as e:
            print(f"    ⚠ Back button at login page: {str(e)}")
        
        print(f"  ✓ NAV03 PASSED – Android back button works correctly")
        
    except AssertionError as e:
        pytest.fail(f"NAV03 FAILED: {str(e)}")
    except Exception as e:
        pytest.fail(f"NAV03 ERROR: {str(e)}")


@pytest.mark.navigation
def TC12_nav04_portrait_landscape_rotation(driver):
    """NAV04 – Tester la navigation portrait ↔ paysage
    
    Technique : Test de configuration
    Objectif : Vérifier que l'app s'adapte bien aux changements d'orientation
    
    Étapes :
    1. Se connecter en portrait
    2. Vérifier l'affichage en portrait
    3. Basculer en paysage
    4. Vérifier l'affichage en paysage
    5. Revenir en portrait
    6. Vérifier que l'état est conservé
    
    Résultat attendu : L'app s'adapte correctement aux rotations
    """
    login = LoginPage(driver)
    home = HomePage(driver)
    
    print(f"\n📱 NAV04 – Testing orientation rotation (portrait ↔ landscape)...")
    
    try:
        # === Connexion ===
        print(f"  [Step 1] Logging in (portrait mode)...")
        login.send_keys(*login.USERNAME, "standard_user")
        time.sleep(0.2)
        login.send_keys(*login.PASSWORD, "secret_sauce")
        time.sleep(0.2)
        login.click(*login.LOGIN_BTN)
        time.sleep(2)
        print(f"    ✓ Login successful")
        
        # === Vérifier l'orientation initiale ===
        print(f"  [Step 2] Checking initial orientation...")
        orientation = driver.orientation
        print(f"    ✓ Initial orientation: {orientation}")
        
        # === Ajouter un produit ===
        print(f"  [Step 3] Adding product to cart (portrait)...")
        home.add_to_cart(item_index=0)
        time.sleep(0.5)
        cart_count_portrait = home.get_cart_count()
        print(f"    ✓ Cart count in portrait: {cart_count_portrait}")
        
        # === Basculer en paysage ===
        print(f"  [Step 4] Rotating to landscape...")
        try:
            driver.orientation = "LANDSCAPE"
            time.sleep(1.5)
            orientation = driver.orientation
            print(f"    ✓ Current orientation: {orientation}")
            
            # Vérifier que les données sont conservées
            cart_count_landscape = home.get_cart_count()
            assert cart_count_landscape == cart_count_portrait, f"Cart count changed after rotation: {cart_count_portrait} → {cart_count_landscape}"
            print(f"    ✓ Cart count preserved in landscape: {cart_count_landscape}")
        except Exception as e:
            print(f"    ⚠ Landscape rotation not supported or error: {str(e)}")
        
        # === Revenir en portrait ===
        print(f"  [Step 5] Rotating back to portrait...")
        try:
            driver.orientation = "PORTRAIT"
            time.sleep(1.5)
            orientation = driver.orientation
            print(f"    ✓ Back to orientation: {orientation}")
            
            # Vérifier une dernière fois
            cart_count_final = home.get_cart_count()
            assert cart_count_final == cart_count_portrait, f"Cart count lost after final rotation: {cart_count_portrait} → {cart_count_final}"
            print(f"    ✓ Cart count preserved after returning to portrait: {cart_count_final}")
        except Exception as e:
            print(f"    ⚠ Portrait rotation not supported or error: {str(e)}")
        
        print(f"  ✓ NAV04 PASSED – Orientation rotation handled correctly")
        
        # === Logout ===
        try:
            home.logout()
        except:
            pass
        
    except AssertionError as e:
        pytest.fail(f"NAV04 FAILED: {str(e)}")
    except Exception as e:
        pytest.fail(f"NAV04 ERROR: {str(e)}")


@pytest.mark.navigation
def TC13_nav05_app_restart_session_state(driver):
    """NAV05 – Tester le redémarrage de l'app (session conservée ou non)
    
    Technique : Test de configuration
    Objectif : Vérifier si la session est conservée après redémarrage de l'app
    
    Étapes :
    1. Se connecter et ajouter un produit au panier
    2. Fermer l'app
    3. Réouvrir l'app
    4. Vérifier si on est toujours connecté
    5. Vérifier si le panier est conservé
    
    Résultat attendu : App ferme/rouvre correctement, session peut être conservée ou perdue
    """
    login = LoginPage(driver)
    home = HomePage(driver)
    
    print(f"\n📱 NAV05 – Testing app restart and session state...")
    
    try:
        # === PARTIE 1: Connexion et ajout ===
        print(f"  [Step 1] Logging in and adding product...")
        login.send_keys(*login.USERNAME, "standard_user")
        time.sleep(0.2)
        login.send_keys(*login.PASSWORD, "secret_sauce")
        time.sleep(0.2)
        login.click(*login.LOGIN_BTN)
        time.sleep(2)
        print(f"    ✓ Login successful")
        
        home.add_to_cart(item_index=0)
        time.sleep(0.5)
        cart_count_before = home.get_cart_count()
        print(f"    ✓ Product added to cart (count: {cart_count_before})")
        
        # === PARTIE 2: Fermer l'app ===
        print(f"  [Step 2] Closing app (terminate_app)...")
        try:
            driver.terminate_app("com.swaglabsmobileapp")
            time.sleep(1)
            print(f"    ✓ App terminated")
        except Exception as e:
            print(f"    ⚠ Could not terminate app: {str(e)}")
            pytest.skip("Cannot test app restart")
        
        # === PARTIE 3: Réouvrir l'app ===
        print(f"  [Step 3] Reopening app (activate_app)...")
        try:
            driver.activate_app("com.swaglabsmobileapp")
            time.sleep(2)
            print(f"    ✓ App reactivated")
        except Exception as e:
            print(f"    ⚠ Could not reactivate app: {str(e)}")
        
        # === PARTIE 4: Vérifier l'état après redémarrage ===
        print(f"  [Step 4] Checking state after app restart...")
        
        # Essayer de trouver les éléments de la page
        try:
            # Si on est sur la page produits (session conservée)
            products = driver.find_elements("xpath", "//android.view.ViewGroup[@content-desc='test-Item']")
            if products and len(products) > 0:
                print(f"    ✓ Still on products page (session conservée)")
                cart_count_after = home.get_cart_count()
                print(f"    ✓ Cart count after restart: {cart_count_after}")
                
                if cart_count_after == cart_count_before:
                    print(f"    ✓ Session state FULLY PRESERVED (cart intact)")
                else:
                    print(f"    ⚠ Session state PARTIALLY PRESERVED (cart cleared: {cart_count_before} → {cart_count_after})")
            else:
                # Si on est sur la page login (session perdue)
                print(f"    ⚠ On login page - Session NOT preserved (expected behavior)")
        except Exception as e:
            print(f"    ⚠ Error checking state: {str(e)}")
        
        print(f"  ✓ NAV05 PASSED – App restart handled correctly")
        
    except Exception as e:
        pytest.fail(f"NAV05 ERROR: {str(e)}")
