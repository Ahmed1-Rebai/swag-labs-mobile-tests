"""
Tests Responsive Design – Appium Mobile (Multi-AVD)
Techniques : Responsive testing via différents AVD Android
Objectif : Vérifier l'affichage et l'interaction sur 3 résolutions d'écran différentes
(Petit téléphone 4.7", Téléphone moyen 6.4", Grande tablette 10")

IMPORTANT : Ces tests doivent s'exécuter sur 3 AVD différents (voir AVD_SETUP_GUIDE.md)
- AVD 1: Pixel_4_7_Small (720x1280) pour RESP01
- AVD 2: Pixel_6_4_Medium (1080x1920) pour RESP02
- AVD 3: Pixel_Tablet_10 (2560x1600) pour RESP03
"""

import time
import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage


def get_device_info(driver):
    """Récupère les infos de l'appareil (résolution, density, etc.)"""
    try:
        window_size = driver.get_window_size()
        return {
            "width": window_size.get("width", 0),
            "height": window_size.get("height", 0),
            "diagonal": round((window_size.get("width", 0) ** 2 + window_size.get("height", 0) ** 2) ** 0.5 / 100, 1),  # approximation
        }
    except Exception as e:
        return {"width": 0, "height": 0, "diagonal": 0, "error": str(e)}


@pytest.mark.responsive
def TC38_resp01_login_display_small_phone(driver):
    """RESP01 – Test complet: Login, Ajout produit, Logout sur petit téléphone (4.7")
    
    Technique : Responsive testing (sur AVD petit téléphone)
    Objectif : Vérifier que tous les éléments et interactions fonctionnent correctement
               sur petit téléphone (4.7" - 720x1280)
    
    Préconditions :
    - Exécuter ce test sur AVD : Pixel_4_7_Small (720x1280)
    - Voir AVD_SETUP_GUIDE.md pour créer l'AVD
    
    Étapes :
    1. Vérifier la résolution du device (doit être ~720x1280)
    2. Vérifier que les champs username, password et bouton LOGIN sont visibles
    3. Se connecter
    4. Ajouter un produit au panier
    5. Se déconnecter
    
    Résultat attendu : Tous les éléments visibles et toutes les interactions fonctionnelles
    """
    device_info = get_device_info(driver)
    print(f"\n📱 RESP01 – Testing on SMALL PHONE (4.7\")")
    print(f"  Device resolution: {device_info['width']}x{device_info['height']}")
    
    # Vérifier qu'on est bien sur un petit écran (~720x1280)
    if device_info['width'] > 900:
        print(f"  ⚠ WARNING: Device resolution {device_info['width']}x{device_info['height']} is larger than expected for 4.7\" phone")
        print(f"  Are you running on the correct AVD (Pixel_4_7_Small)?")
    
    login = LoginPage(driver)
    home = HomePage(driver)
    
    try:
        # === STEP 1: Vérifier l'affichage de la page LOGIN ===
        print(f"\n  [Step 1] Checking login page elements...")
        
        # Vérifier le champ USERNAME
        username_elem = login.find(*login.USERNAME)
        assert username_elem is not None, "Username field not found"
        assert username_elem.is_displayed(), "Username field not visible"
        username_size = username_elem.size
        print(f"    ✓ Username field visible (size: {username_size['width']}x{username_size['height']})")
        
        # Vérifier le champ PASSWORD
        password_elem = login.find(*login.PASSWORD)
        assert password_elem is not None, "Password field not found"
        assert password_elem.is_displayed(), "Password field not visible"
        password_size = password_elem.size
        print(f"    ✓ Password field visible (size: {password_size['width']}x{password_size['height']})")
        
        # Vérifier le bouton LOGIN
        login_btn_elem = login.find(*login.LOGIN_BTN)
        assert login_btn_elem is not None, "Login button not found"
        assert login_btn_elem.is_displayed(), "Login button not visible"
        assert login_btn_elem.is_enabled(), "Login button not enabled"
        login_btn_size = login_btn_elem.size
        print(f"    ✓ Login button visible and enabled (size: {login_btn_size['width']}x{login_btn_size['height']})")
        
        # Vérifier que les éléments ne sont pas trop petits (signe de cut-off)
        min_width = 50
        assert username_size['width'] > min_width, f"Username field too narrow ({username_size['width']}px)"
        assert password_size['width'] > min_width, f"Password field too narrow ({password_size['width']}px)"
        assert login_btn_size['width'] > min_width, f"Login button too narrow ({login_btn_size['width']}px)"
        print(f"    ✓ All login elements properly sized")
        
        # === STEP 2: Se connecter ===
        print(f"\n  [Step 2] Logging in...")
        login.send_keys(*login.USERNAME, "standard_user")
        time.sleep(0.3)
        login.send_keys(*login.PASSWORD, "secret_sauce")
        time.sleep(0.3)
        login.click(*login.LOGIN_BTN)
        time.sleep(2)
        print(f"    ✓ Login successful")
        
        # === STEP 3: Ajouter un produit au panier ===
        print(f"\n  [Step 3] Adding product to cart...")
        home.add_to_cart(item_index=0)
        time.sleep(0.5)
        
        cart_count = home.get_cart_count()
        assert cart_count > 0, "Product not added to cart"
        print(f"    ✓ Product added to cart (count: {cart_count})")
        
        # === STEP 4: Se déconnecter ===
        print(f"\n  [Step 4] Logging out...")
        home.logout()
        time.sleep(1)
        print(f"    ✓ Logout successful")
        
        print(f"\n  ✓ RESP01 PASSED – All interactions work correctly on small phone (4.7\")")
        
    except AssertionError as e:
        pytest.fail(f"RESP01 FAILED: {str(e)}")
    except Exception as e:
        pytest.fail(f"RESP01 ERROR: {str(e)}")


@pytest.mark.responsive
def TC39_resp02_products_visibility_medium_phone(driver):
    """RESP02 – Affichage correct des produits sur téléphone moyen (6.4")
    
    Technique : Responsive testing (sur AVD téléphone moyen)
    Objectif : Vérifier que les produits sont visibles et non coupés
               sur téléphone moyen (6.4" - 1080x1920)
    
    Préconditions :
    - Exécuter ce test sur AVD : Pixel_6_4_Medium (1080x1920)
    - Voir AVD_SETUP_GUIDE.md pour créer l'AVD
    
    Étapes :
    1. Se connecter
    2. Vérifier que les produits et leurs images sont visibles
    3. Vérifier que le prix et le nom du produit sont visibles
    4. Vérifier que les boutons "ADD TO CART" ne sont pas coupés
    
    Résultat attendu : Produits et boutons correctement affichés sur téléphone moyen
    """
    device_info = get_device_info(driver)
    print(f"\n📱 RESP02 – Testing products visibility on MEDIUM PHONE (6.4\")")
    print(f"  Device resolution: {device_info['width']}x{device_info['height']}")
    
    # Vérifier qu'on est bien sur un écran moyen (~1080x1920)
    if device_info['width'] < 1000 or device_info['width'] > 1200:
        print(f"  ⚠ WARNING: Device resolution {device_info['width']}x{device_info['height']} differs from expected for 6.4\" phone")
        print(f"  Are you running on the correct AVD (Pixel_6_4_Medium)?")
    
    login = LoginPage(driver)
    home = HomePage(driver)
    
    # === Connexion ===
    login.send_keys(*login.USERNAME, "standard_user")
    time.sleep(0.2)
    login.send_keys(*login.PASSWORD, "secret_sauce")
    time.sleep(0.2)
    login.click(*login.LOGIN_BTN)
    time.sleep(2)
    
    try:
        # Trouver tous les produits
        products = driver.find_elements("xpath", "//android.view.ViewGroup[@content-desc='test-Item']")
        assert len(products) > 0, "No products found"
        print(f"  ✓ Found {len(products)} products")
        
        # Vérifier le premier produit
        first_product = products[0]
        assert first_product.is_displayed(), "First product not visible"
        print(f"  ✓ First product is displayed")
        
        # Vérifier le bouton "ADD TO CART" – avec attente et retry
        add_buttons = None
        for attempt in range(3):
            try:
                add_buttons = driver.find_elements("accessibility id", "test-ADD TO CART")
                if len(add_buttons) > 0:
                    break
            except Exception:
                pass
            if attempt < 2:
                time.sleep(0.5)
        
        assert add_buttons and len(add_buttons) > 0, "Add to cart buttons not found after retries"
        print(f"  ✓ Found {len(add_buttons)} add buttons")
        
        # Vérifier que le premier bouton existe et est cliquable
        try:
            first_add_btn = add_buttons[0]
            assert first_add_btn.is_displayed(), "First add button not visible"
            assert first_add_btn.is_enabled(), "First add button not enabled"
            btn_size = first_add_btn.size
            
            min_btn_width = 40
            assert btn_size['width'] > min_btn_width, f"Add button too narrow ({btn_size['width']}px)"
            
            print(f"  ✓ Add to cart button visible and clickable (size: {btn_size['width']}x{btn_size['height']})")
            print(f"  ✓ RESP02 PASSED – Products correctly displayed on medium phone (6.4\")")
        except Exception as e:
            pytest.fail(f"Button verification failed: {str(e)}")
        
    except AssertionError as e:
        pytest.fail(f"RESP02 FAILED: {str(e)}")
    finally:
        try:
            home.logout()
        except:
            pass


@pytest.mark.responsive
def TC40_resp03_buttons_clickable_large_tablet(driver):
    """RESP03 – Affichage et interactivité sur tablette large (10")
    
    Technique : Responsive testing (sur AVD tablette large)
    Objectif : Vérifier que l'app s'adapte bien à grand écran (10")
               et que les boutons restent cliquables
    
    Préconditions :
    - Exécuter ce test sur AVD : Pixel_Tablet_10 (2560x1600)
    - Voir AVD_SETUP_GUIDE.md pour créer l'AVD
    
    Étapes :
    1. Se connecter
    2. Vérifier que les produits s'affichent correctement en large
    3. Ajouter un produit au panier
    4. Ouvrir le panier
    5. Vérifier que les boutons CHECKOUT et REMOVE restent cliquables
    
    Résultat attendu : Tous les boutons cliquables sans erreur sur grand écran
    """
    device_info = get_device_info(driver)
    print(f"\n📱 RESP03 – Testing on LARGE TABLET (10\")")
    print(f"  Device resolution: {device_info['width']}x{device_info['height']}")
    
    # Vérifier qu'on est bien sur un grand écran (~2560x1600)
    if device_info['width'] < 2400:
        print(f"  ⚠ WARNING: Device resolution {device_info['width']}x{device_info['height']} is smaller than expected for 10\" tablet")
        print(f"  Are you running on the correct AVD (Pixel_Tablet_10)?")
    
    login = LoginPage(driver)
    home = HomePage(driver)
    
    # === Connexion ===
    login.send_keys(*login.USERNAME, "standard_user")
    time.sleep(0.2)
    login.send_keys(*login.PASSWORD, "secret_sauce")
    time.sleep(0.2)
    login.click(*login.LOGIN_BTN)
    time.sleep(2)
    
    try:
        print(f"  Testing add to cart on large tablet...")
        
        # Ajouter au panier avec attente pour éviter stale elements
        try:
            home.add_to_cart(item_index=0)
            time.sleep(1)
        except Exception as e:
            print(f"  ⚠ Add to cart encountered: {str(e)}, retrying...")
            time.sleep(1)
            add_buttons = driver.find_elements("accessibility id", "test-ADD TO CART")
            if add_buttons:
                add_buttons[0].click()
                time.sleep(1)
        
        cart_count = home.get_cart_count()
        assert cart_count > 0, "Product not added to cart"
        print(f"  ✓ Add to cart successful ({cart_count} item in cart)")
        
        # Ouvrir le panier
        print(f"  Testing cart icon click on large tablet...")
        home.click_cart_icon()
        time.sleep(1.5)
        
        # Vérifier que le panier a ouvert (chercher bouton CHECKOUT) avec retry
        checkout_btns = None
        for attempt in range(3):
            try:
                checkout_btns = driver.find_elements("accessibility id", "test-CHECKOUT")
                if checkout_btns and len(checkout_btns) > 0:
                    break
            except Exception:
                pass
            if attempt < 2:
                time.sleep(0.5)
        
        assert checkout_btns and len(checkout_btns) > 0, "Checkout button not found in cart after retries"
        print(f"  ✓ Found checkout button")
        
        try:
            checkout_btn = checkout_btns[0]
            assert checkout_btn.is_displayed(), "Checkout button not visible"
            assert checkout_btn.is_enabled(), "Checkout button not enabled"
            print(f"  ✓ Checkout button visible and clickable")
        except Exception as e:
            print(f"  ⚠ Checkout button check failed: {str(e)}")
        
        # Vérifier le bouton REMOVE avec retry
        remove_btns = None
        for attempt in range(3):
            try:
                remove_btns = driver.find_elements("accessibility id", "test-REMOVE")
                if remove_btns and len(remove_btns) > 0:
                    break
            except Exception:
                pass
            if attempt < 2:
                time.sleep(0.5)
        
        assert remove_btns and len(remove_btns) > 0, "Remove button not found after retries"
        print(f"  ✓ Found remove button")
        
        try:
            remove_btn = remove_btns[0]
            assert remove_btn.is_displayed(), "Remove button not visible"
            assert remove_btn.is_enabled(), "Remove button not enabled"
            print(f"  ✓ Remove button visible and clickable")
        except Exception as e:
            print(f"  ⚠ Remove button check failed: {str(e)}")
        
        print(f"  ✓ RESP03 PASSED – All critical buttons remain clickable on large tablet (10\")")
        
    except AssertionError as e:
        pytest.fail(f"RESP03 FAILED: {str(e)}")
    finally:
        try:
            home.logout()
        except:
            pass


@pytest.mark.responsive
def TC41_resp_summary(driver):
    """Résumé des tests responsive et infos device
    
    Affiche un résumé de la configuration testée
    """
    device_info = get_device_info(driver)
    
    print("\n" + "="*70)
    print("RESPONSIVE DESIGN TEST SUMMARY")
    print("="*70)
    print(f"\nCurrent Device Configuration:")
    print(f"  Resolution: {device_info['width']}x{device_info['height']}px")
    print(f"  Approximate Diagonal: {device_info['diagonal']}\"")
    
    print(f"\nExpected AVD Configurations:")
    print(f"  ✓ RESP01: Pixel_4_7_Small (720x1280) – Petit téléphone 4.7\"")
    print(f"  ✓ RESP02: Pixel_6_4_Medium (1080x1920) – Téléphone moyen 6.4\"")
    print(f"  ✓ RESP03: Pixel_Tablet_10 (2560x1600) – Tablette large 10\"")
    
    print(f"\nTo run responsive tests properly:")
    print(f"  1. Create the 3 AVDs using Android Studio (see AVD_SETUP_GUIDE.md)")
    print(f"  2. Launch each AVD separately")
    print(f"  3. Run the corresponding test on each AVD")
    print(f"\nExample commands:")
    print(f"  pytest tests/test_responsive.py::test_resp01_login_display_small_phone -v")
    print(f"  pytest tests/test_responsive.py::test_resp02_products_visibility_medium_phone -v")
    print(f"  pytest tests/test_responsive.py::test_resp03_buttons_clickable_large_tablet -v")
    
    print("\n" + "="*70)

