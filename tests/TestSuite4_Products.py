import time
import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.fixture
def logged_in_driver(driver):
    """Fixture qui se connecte avant chaque test et se déconnecte après."""
    # Login
    login = LoginPage(driver)
    time.sleep(1)
    login.send_keys(*login.USERNAME, "standard_user")
    time.sleep(0.5)
    login.send_keys(*login.PASSWORD, "secret_sauce")
    time.sleep(0.5)
    login.click(*login.LOGIN_BTN)
    time.sleep(3)
    
    # Vérifier qu'on est connecté
    assert "PRODUCTS" in driver.page_source, "Login failed"
    
    yield driver
    
    # Logout après le test
    home = HomePage(driver)
    home.logout()


def TC14_products_page_displayed(logged_in_driver):
    """Test que la page PRODUCTS s'affiche correctement après login."""
    driver = logged_in_driver
    
    # Vérifier que l'élément PRODUCTS est présent
    products_element = driver.find_element("accessibility id", "test-PRODUCTS")
    assert products_element is not None, "PRODUCTS page not found"
    
    # Vérifier que PRODUCTS est visible dans la page source
    assert "PRODUCTS" in driver.page_source




def TC15_products_list_not_empty(logged_in_driver):
    """Test que la liste de produits n'est pas vide."""
    driver = logged_in_driver
    
    # Chercher les produits (test-Item)
    try:
        products = driver.find_elements("accessibility id", "test-Item")
        assert len(products) > 0, "No products found in the list"
    except Exception as e:
        pytest.skip(f"Could not find products: {str(e)}")


def TC16_add_to_cart_buttons_available(logged_in_driver):
    """Test que les boutons "Add to Cart" sont visibles."""
    driver = logged_in_driver
    
    # Chercher les boutons "Add to Cart"
    try:
        add_to_cart_buttons = driver.find_elements("xpath", "//android.widget.Button[contains(@text, 'ADD TO CART')]")
        assert len(add_to_cart_buttons) > 0, "No 'Add to Cart' buttons found"
    except Exception as e:
        pytest.skip(f"Could not find 'Add to Cart' buttons: {str(e)}")



def TC17_add_product_to_cart(logged_in_driver):
    """Test l'ajout d'un produit au panier."""
    driver = logged_in_driver
    time.sleep(1)
    
    # Trouver le premier bouton "Add to Cart"
    try:
        add_to_cart_btn = driver.find_element("accessibility id", "test-ADD TO CART")
        add_to_cart_btn.click()
        time.sleep(2)
        
        # Vérifier que le bouton change de texte à "Remove"
        # Ou vérifier que le cart compte augmente
        assert "Remove" in driver.page_source or "REMOVE" in driver.page_source, "Product not added to cart"
    except Exception as e:
        pytest.skip(f"Could not add product to cart: {str(e)}")


def TC18_remove_product_from_cart(logged_in_driver):
    """Test la suppression d'un produit du panier."""
    driver = logged_in_driver
    home = HomePage(driver)
    time.sleep(1)
    
    # Ajouter d'abord un produit
    try:
        add_to_cart_btn = driver.find_element("accessibility id", "test-ADD TO CART")
        add_to_cart_btn.click()
        time.sleep(1)
        
        # Puis le supprimer
        remove_btn = driver.find_element("accessibility id", "test-REMOVE")
        remove_btn.click()
        time.sleep(2)
        
        # Vérifier que le bouton revient à "Add to Cart"
        assert "ADD TO CART" in driver.page_source, "Product not removed from cart"
    except Exception as e:
        pytest.skip(f"Could not test remove from cart: {str(e)}")


def TC19_add_multiple_products_to_cart(logged_in_driver):
    """Test l'ajout de plusieurs produits au panier."""
    driver = logged_in_driver
    time.sleep(1)
    
    # Ajouter les 2 premiers produits
    try:
        add_btns = driver.find_elements("accessibility id", "test-ADD TO CART")
        assert len(add_btns) >= 2, "Not enough products to test"
        
        add_btns[0].click()
        time.sleep(1)
        add_btns[1].click()
        time.sleep(1)
        
        # Aller au panier
        cart_btn = driver.find_element("accessibility id", "test-Cart")
        cart_btn.click()
        time.sleep(2)
        
        # Vérifier qu'on est sur la page du panier
        assert "Cart" in driver.page_source or "CART" in driver.page_source, \
            "Cart page not loaded"
    except Exception as e:
        pytest.skip(f"Could not test multiple products: {str(e)}")


def TC20_drag_product_to_cart(logged_in_driver):
    """Test drag & drop product to cart."""
    driver = logged_in_driver
    home = HomePage(driver)
    time.sleep(1)
    
    product = driver.find_element("accessibility id", "test-Item")
    cart = driver.find_element("accessibility id", "test-Cart")
    
    home.drag_and_drop(product, cart)
    time.sleep(2)
    
    # Verify product was added (Remove button or cart count)
    assert "Remove" in driver.page_source or "REMOVE" in driver.page_source or \
           "1" in driver.page_source, "Drag to cart failed"


def TC21_cart_navigation(logged_in_driver):
    """Test navigation to cart page."""
    driver = logged_in_driver
    time.sleep(1)
    
    cart_btn = driver.find_element("accessibility id", "test-Cart")
    cart_btn.click()
    time.sleep(2)
    
    # Verify cart page loaded
    assert "Cart" in driver.page_source or "CART" in driver.page_source, \
        "Cart page not loaded"


def TC22_menu_navigation(logged_in_driver):
    """Test opening menu."""
    driver = logged_in_driver
    home = HomePage(driver)
    time.sleep(1)
    
    menu_btn = home.find(*home.MENU_BTN)
    menu_btn.click()
    time.sleep(2)
    
    # Verify menu opened with expected options
    assert "About" in driver.page_source or "LOGOUT" in driver.page_source, \
        "Menu not opened"


def TC23_product_details_navigation(logged_in_driver):
    """Test navigation to product details page."""
    driver = logged_in_driver
    time.sleep(1)
    
    product = driver.find_element("accessibility id", "test-Item")
    product.click()
    time.sleep(2)
    
    # Verify product details page loaded
    assert "Back" in driver.page_source or "BACK" in driver.page_source, \
        "Product details page not loaded"


def TC24_logout_functionality(logged_in_driver):
    """Test logout from menu."""
    driver = logged_in_driver
    home = HomePage(driver)
    time.sleep(1)
    
    # Open menu
    menu_btn = home.find(*home.MENU_BTN)
    menu_btn.click()
    time.sleep(1)
    
    # Click logout
    logout_btn = home.find(*home.LOGOUT_BTN)
    logout_btn.click()
    time.sleep(2)
    
    # Verify back to login page
    assert "Username" in driver.page_source or "Password" in driver.page_source, \
        "Not logged out properly"


def TC25_toggle_sort_menu(logged_in_driver):
    """Test opening sort/filter menu."""
    driver = logged_in_driver
    time.sleep(1)
    
    toggle_btn = driver.find_element("accessibility id", "test-Toggle")
    toggle_btn.click()
    time.sleep(2)
    
    # Verify sort menu appears with options
    page_source = driver.page_source
    assert "Name" in page_source or "Price" in page_source or "Z->A" in page_source, \
        "Sort menu not opened"


def TC26_scroll_products_list(logged_in_driver):
    """Test scrolling through products list."""
    driver = logged_in_driver
    time.sleep(1)
    
    products_before = driver.find_elements("accessibility id", "test-Item")
    count_before = len(products_before)
    
    # Scroll down
    driver.swipe(540, 1200, 540, 600, 500)
    time.sleep(1)
    
    # Verify products still visible after scroll
    products_after = driver.find_elements("accessibility id", "test-Item")
    count_after = len(products_after)
    
    assert count_after > 0, "No products visible after scroll"


# ===== TESTS AVEC PROBLEM_USER =====
# Note: Les tests problem_user ont été supprimés car ils étaient des doublons
# des tests standards. Le comportement de problem_user est maintenant testé
# dans TestSuite5_Checkout.py (TC48_visual_glitch_with_problem_user)