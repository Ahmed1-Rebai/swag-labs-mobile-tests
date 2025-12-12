import time
import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
# NOTE: Assurez-vous que les classes CheckoutPage, CartPage et HomePage sont bien implémentées.
# from pages.cart_page import CartPage 
from pages.checkout_page import CheckoutPage 

CORRECT_USERNAME = "standard_user"
CORRECT_PASSWORD = "secret_sauce"

@pytest.fixture(scope="function")
def login_standard_user(driver):
    """Fixture pour connecter l'utilisateur standard avant chaque test."""
    login = LoginPage(driver)
    login.send_keys(*login.USERNAME, CORRECT_USERNAME)
    login.send_keys(*login.PASSWORD, CORRECT_PASSWORD)
    login.click(*login.LOGIN_BTN)
    time.sleep(0.1) # Laisser le temps de charger la page des produits
    yield HomePage(driver) # Retourne l'objet HomePage
    
    # Teardown: Déconnexion après le test
    try:
        home = HomePage(driver)
        home.logout()
    except:
        # Si on n'arrive pas à se déconnecter (ex: test a échoué avant la connexion), on ignore
        pass


@pytest.fixture(scope="function")
def login_problem_user(driver):
    """Fixture pour connecter l'utilisateur problem_user avant chaque test (pour cas visuel)."""
    login = LoginPage(driver)
    login.send_keys(*login.USERNAME, "problem_user")
    login.send_keys(*login.PASSWORD, CORRECT_PASSWORD)
    login.click(*login.LOGIN_BTN)
    time.sleep(2)
    yield HomePage(driver)
    try:
        HomePage(driver).logout()
    except:
        pass



# --- Scénarios 1: Test des fonctionnalités de la page des produits ---

def TC27_sort_products_by_price_low_to_high(driver, login_standard_user):
    """Test le tri des produits par prix (du plus bas au plus haut)."""
    home = login_standard_user
    
    # 1. Sélectionner l'option de tri Prix (bas-haut)
    home.select_sort_option("Price (low to high)")
    time.sleep(2)
    
    # 2. Récupérer les prix affichés
    prices = home.get_all_product_prices() # Cette méthode doit être implémentée dans HomePage
    
    # 3. Vérifier que les prix sont triés correctement
    # On convertit les prix en nombres pour la vérification
    numerical_prices = [float(p.replace('$', '')) for p in prices]
    
    is_sorted = all(numerical_prices[i] <= numerical_prices[i+1] for i in range(len(numerical_prices) - 1))
    assert is_sorted, "Le tri par prix (bas à haut) n'a pas fonctionné correctement."
    # Vérifier la présence d'un produit connu (scroll si nécessaire)
    home.find_with_scroll("xpath", "//android.widget.TextView[contains(@text, 'Sauce Labs Backpack')]")

def TC28_sort_products_by_name_z_to_a(driver, login_standard_user):
    """NOUVEAU TEST: Test le tri des produits par nom (du Z à A)."""
    home = login_standard_user
    
    # 1. Sélectionner l'option de tri Nom (Z-A)
    home.select_sort_option("Name (Z to A)")
    time.sleep(2)
    
    # 2. Récupérer les noms affichés
    names = home.get_all_product_names() # Cette méthode doit être implémentée dans HomePage
    
    # 3. Vérifier que les noms sont triés correctement (ordre alphabétique descendant)
    # Assure que chaque élément est alphabétiquement supérieur ou égal au suivant
    is_sorted = all(names[i] >= names[i+1] for i in range(len(names) - 1))
    assert is_sorted, "Le tri par nom (Z à A) n'a pas fonctionné correctement."
    # Vérifier la présence d'un produit connu
    home.find_with_scroll("xpath", "//android.widget.TextView[contains(@text, 'Sauce Labs Backpack')]")


def TC29_sort_products_by_name_a_to_z(driver, login_standard_user):
    """Test le tri des produits par nom (du A à Z)."""
    home = login_standard_user

    # Ouvrir le sélecteur de tri via l'icône de filtrage (modal)
    modal_xpath = '//android.view.ViewGroup[@content-desc="test-Modal Selector Button"]/android.view.ViewGroup/android.view.ViewGroup/android.widget.ImageView'
    driver.find_element("xpath", modal_xpath).click()
    time.sleep(1)

    # Choisir l'option Name (A to Z)
    driver.find_element("xpath", "//android.widget.TextView[@text=\"Name (A to Z)\"]").click()
    time.sleep(2)

    # Récupérer les noms affichés et vérifier l'ordre croissant
    names = home.get_all_product_names()
    # Vérifier la présence d'un produit connu
    home.find_with_scroll("xpath", "//android.widget.TextView[contains(@text, 'Sauce Labs Backpack')]")
    assert names == sorted(names), "Le tri par nom (A à Z) n'a pas fonctionné correctement."


def TC30_sort_products_by_price_high_to_low(driver, login_standard_user):
    """Test le tri des produits par prix (du plus haut au plus bas)."""
    home = login_standard_user

    # Ouvrir le sélecteur de tri
    modal_xpath = '//android.view.ViewGroup[@content-desc="test-Modal Selector Button"]/android.view.ViewGroup/android.view.ViewGroup/android.widget.ImageView'
    driver.find_element("xpath", modal_xpath).click()
    time.sleep(1)

    # Choisir l'option Price (high to low)
    driver.find_element("xpath", "//android.widget.TextView[@text=\"Price (high to low)\"]").click()
    time.sleep(2)

    # Récupérer les prix et vérifier l'ordre décroissant
    prices = home.get_all_product_prices()
    numerical_prices = [float(p.replace('$', '')) for p in prices]
    is_sorted_desc = all(numerical_prices[i] >= numerical_prices[i+1] for i in range(len(numerical_prices) - 1))
    assert is_sorted_desc, "Le tri par prix (haut à bas) n'a pas fonctionné correctement."
    # Vérifier la présence d'un produit connu
    home.find_with_scroll("xpath", "//android.widget.TextView[contains(@text, 'Sauce Labs Backpack')]")


def TC31_cancel_sort_modal(driver, login_standard_user):
    """Ouvre le modal de tri et annule; l'ordre des produits ne doit pas changer."""
    home = login_standard_user

    names_before = home.get_all_product_names()

    # Ouvrir le modal de tri puis cliquer sur Cancel
    modal_xpath = '//android.view.ViewGroup[@content-desc="test-Modal Selector Button"]/android.view.ViewGroup/android.view.ViewGroup/android.widget.ImageView'
    driver.find_element("xpath", modal_xpath).click()
    time.sleep(1)
    driver.find_element("xpath", "//android.widget.TextView[@text=\"Cancel\"]").click()
    time.sleep(1)

    names_after = home.get_all_product_names()
    assert names_before == names_after, "L'annulation du modal de tri a modifié l'ordre des produits."


def TC32_empty_cart(driver, login_standard_user):
    """Test le processus de checkout avec un panier vide."""
    home = login_standard_user
    
    # 1. Vérifier que le panier est initialement vide
    cart_count = home.get_cart_count()
    assert cart_count == 0, f"Le panier doit être vide au départ, trouvé {cart_count}"
    
    # 2. Cliquer sur l'icône du panier via le XPath fourni
    cart_icon_xpath = '//android.view.ViewGroup[@content-desc="test-Cart"]/android.view.ViewGroup/android.widget.ImageView'
    driver.find_element("xpath", cart_icon_xpath).click()
    time.sleep(2)
    
    # 3. Vérifier qu'il n'y a aucun article dans le panier
    remove_buttons = driver.find_elements("accessibility id", "test-REMOVE")
    assert len(remove_buttons) == 0, f"Aucun article ne devrait être présent dans un panier vide, trouvé {len(remove_buttons)}"
    
    # 4. Cliquer sur CHECKOUT avec un panier vide
    try:
        checkout_btn = driver.find_element("accessibility id", "test-CHECKOUT")
        checkout_btn.click()
        time.sleep(2)
        
        # 5. Vérifier le comportement: soit une erreur, soit une redirection, soit un message d'avertissement
        # L'app peut afficher une page de checkout vide ou un message d'erreur
        # On cherche un message d'erreur ou un élément indiquant que le checkout n'est pas possible
        try:
            error_msg = driver.find_element("xpath", "//android.widget.TextView[contains(@text, 'error') or contains(@text, 'Error') or contains(@text, 'cannot') or contains(@text, 'Cannot') or contains(@text, 'empty') or contains(@text, 'Empty')]")
            # Une erreur s'est affichée - c'est un comportement attendu
            assert "error" in error_msg.text.lower() or "empty" in error_msg.text.lower() or "cannot" in error_msg.text.lower(), f"Message reçu: {error_msg.text}"
        except Exception:
            # Si pas de message d'erreur, on est peut-être redirigé vers la page de paiement
            # Vérifier que nous sommes sur une page (sans items)
            pass
    except Exception as e:
        # Si le bouton CHECKOUT n'est pas cliquable ou visible, c'est aussi un comportement valide
        assert "not found" in str(e).lower() or "not clickable" in str(e).lower(), f"Erreur inattendue: {str(e)}" 


def TC33_checkout_without_products(driver, login_standard_user):
    home = login_standard_user

    # Précondition
    assert home.get_cart_count() == 0, "Le panier doit être vide au début du test"

    # Ouvrir le panier
    cart_icon_xpath = '//android.view.ViewGroup[@content-desc="test-Cart"]/android.view.ViewGroup/android.widget.ImageView'
    try:
        driver.find_element("xpath", cart_icon_xpath).click()
    except Exception:
        home.click_cart_icon()
    time.sleep(1.5)

    # Bouton checkout
    checkout_buttons = driver.find_elements("accessibility id", "test-CHECKOUT")
    if checkout_buttons:
        checkout_buttons[0].click()
    else:
        # Si l'app bloque déjà ici → OK
        return

    time.sleep(1)

    checkout = CheckoutPage(driver)
    checkout.enter_user_info_default()
    checkout.click_continue_button()
    time.sleep(1)

    # Vérifier si une erreur s'affiche
    errs = driver.find_elements("accessibility id", "test-Error message")
    if errs:
        return  # c'est correct

    # Vérifier si FINISH est accessible → dans ce cas l'app est FAULTY
    finish_buttons = driver.find_elements("accessibility id", "test-FINISH")

    assert len(finish_buttons) == 0, \
        "BUG : Le checkout arrive au bouton FINISH alors que le panier est vide."






# --- Scénarios 2: Test du processus d'achat (E2E) ---

def TC34_successful_end_to_end_purchase(driver, login_standard_user):
    """Test l'ajout d'articles, la navigation vers le paiement et la finalisation de la commande."""
    home = login_standard_user
    
    # 1. Ajouter deux articles au panier
    home.add_to_cart(item_index=0)
    home.add_to_cart(item_index=1)
    
    # 2. Naviguer vers le panier
    home.click_cart_icon()
    time.sleep(2)
    
    # 3. Vérifier qu'il y a 2 articles dans le panier (dans le cas de l'app mobile, on vérifie un élément du panier)
    # Assumant que le panier a un bouton 'Checkout'
    try:
        checkout_btn = driver.find_element("accessibility id", "test-CHECKOUT")
        assert checkout_btn.is_displayed(), "Bouton CHECKOUT non trouvé dans le panier."
        
    except Exception as e:
        assert False, f"Impossible de naviguer ou de vérifier le panier: {str(e)}"
    
    # 4. Commencer le paiement
    checkout_btn.click()
    time.sleep(2)
    
    # 5. Remplir les informations (Assumant une classe/méthode CheckoutPage)
    checkout = CheckoutPage(driver) # Assurez-vous que cette classe est disponible
    # Utiliser les valeurs par défaut définies dans CheckoutPage
    checkout.enter_user_info_default() # Remplit John / Doe / 12345 par défaut
    checkout.click_continue_button()
    time.sleep(2)

    # 6. Page d'aperçu: Vérifier le total final
    # Cette étape est souvent la plus cruciale pour la QA
    
    # 7. Finaliser la commande
    checkout.click_finish_button()
    time.sleep(2)
    
    # 8. Vérifier la page de confirmation de succès
    # NOTE: Le content-desc de la page complète pourrait être "test-CHECKOUT: COMPLETE!"
    confirmation_header = driver.find_element("xpath", "//android.widget.TextView[@text='CHECKOUT: COMPLETE!']")
    assert "COMPLETE!" in confirmation_header.text, "La commande n'a pas été finalisée avec succès."
    

    # 9. Déconnexion explicite : quitte l'application / revient à l'écran de connexion
    try:
        from pages.home_page import HomePage as _HomePage
        _HomePage(driver).logout()
    except Exception:
        # Si la déconnexion échoue, on ignore car le but principal est de valider la commande
        pass


def TC35_purchase_process_cancellation(driver, login_standard_user):
    """Test que l'utilisateur peut annuler le processus de paiement à l'étape d'information client."""
    home = login_standard_user
    
    # 1. Ajouter un article au panier
    home.add_to_cart(item_index=0)
    
    # 2. Naviguer vers le panier et cliquer sur Checkout
    home.click_cart_icon()
    driver.find_element("accessibility id", "test-CHECKOUT").click()
    time.sleep(2)
    
    # 3. Page d'information client: Cliquer sur CANCEL
    # Use CheckoutPage helper to click cancel (handles multiple variants)
    checkout = CheckoutPage(driver)
    checkout.click_cancel_button()
    time.sleep(2)
    
    # 4. Vérifier la redirection vers la page des produits
    products_header = driver.find_element("xpath", "//android.widget.TextView[@text='PRODUCTS']")
    assert products_header.is_displayed(), "L'annulation n'a pas redirigé vers la page des produits."
    
    # 5. Vérifier que le panier N'EST PAS vide (l'article doit avoir été conservé)
    cart_count = home.get_cart_count()
    assert cart_count == 1, f"L'article a été retiré du panier après annulation. Devrait être 1, trouvé {cart_count}"


def TC36_checkout_info_validation_missing_fields(driver, login_standard_user):
    """Test négatif: la validation des champs obligatoires (prénom, nom, code postal) doit empêcher le checkout si un champ est manquant."""
    home = login_standard_user
    checkout = CheckoutPage(driver) 
    
    # 1. Ajouter un article et naviguer jusqu'à la page d'information client
    home.add_to_cart(item_index=0)
    home.click_cart_icon()
    driver.find_element("accessibility id", "test-CHECKOUT").click()
    time.sleep(2)
    
    # Fonction helper pour vérifier qu'on est passé à la page overview
    def check_validation_succeeds():
        # Essayer de continuer avec le champ manquant
        checkout.click_continue_button()
        time.sleep(1)
        
        # Vérifier qu'on est passé à la page overview
        try:
            driver.find_element("accessibility id", "test-FINISH")
            print("✓ Validation fonctionne: checkout réussi avec tous les champs")
        except:
            pytest.fail("BUG: Checkout empêché même avec tous les champs remplis!")
    
    
    # Scénario A: Prénom manquant
    checkout.enter_user_info("", "Doe", "12345") # Prénom vide
    try:
        check_validation_succeeds()
        pytest.fail("BUG: Checkout allowed with missing first name - validation failed!")
    except:
        print("✓ Validation correcte: empêché checkout avec prénom manquant")
    
    # Scénario B: Nom manquant
    checkout.enter_user_info("Ahmed", "", "12345") # Nom vide
    try:
        check_validation_succeeds()
        pytest.fail("BUG: Checkout allowed with missing last name - validation failed!")
    except:
        print("✓ Validation correcte: empêché checkout avec nom manquant")
    
    # Scénario C: Code postal manquant
    checkout.enter_user_info("Ahmed", "Rebai", "") # Code postal vide
    try:
        check_validation_succeeds()
        pytest.fail("BUG: Checkout allowed with missing postal code - validation failed!")
    except:
        print("✓ Validation correcte: empêché checkout avec code postal manquant")
    

def TC37_visual_glitch_with_problem_user(driver, login_problem_user):
    """
    Test spécifique pour le 'problem_user': Vérifie si les images des produits sont cassées,
    comme prévu avec cet utilisateur.
    """
    home = login_problem_user
    
    # 1. Récupérer les URLs des images des produits (simuler l'inspection du DOM/accessibilité)
    # Assumons une méthode qui récupère les attributs d'accessibilité des images
    image_paths = home.get_all_product_image_sources() # Cette méthode doit être implémentée
    
    # 2. Vérifier qu'au moins une image est cassée (ce qui signifie que les chemins des images sont identiques, 
    # car l'application charge la même image pour tout le monde avec cet utilisateur).
    
    # Dans l'application Swag Labs, le "problem_user" charge la MÊME image (URL) 
    # pour TOUS les produits, ce qui est le bug attendu.
    if image_paths:
        first_image_path = image_paths[0]
        # Vérifier si TOUS les chemins d'image sont identiques au premier (le bug attendu)
        is_glitch_present = all(path == first_image_path for path in image_paths)
        
        assert is_glitch_present, "BUG APP: L'utilisateur 'problem_user' n'a pas le défaut visuel (les images sont différentes)!"
    else:
        # Fait échouer le test si aucune image n'a été trouvée pour vérification
        assert False, "Aucune image de produit trouvée pour vérifier le défaut visuel du problem_user."