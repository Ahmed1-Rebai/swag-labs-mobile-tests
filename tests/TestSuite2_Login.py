import time
import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage


@pytest.mark.parametrize("username", [
    "standard_user",
    "locked_out_user",
    "problem_user",
])
def TC2_login_with_accepted_users(driver, username):
    """Test login avec les 3 utilisateurs acceptés et password 'secret_sauce'.
    
    Tous les 3 users doivent pouvoir se connecter avec le password 'secret_sauce'.
    Si un user échoue à se connecter, c'est un BUG de l'application.
    """
    from pages.home_page import HomePage
    
    login = LoginPage(driver)
    time.sleep(1)
    
    # Entrer directement le username
    login.send_keys(*login.USERNAME, username)
    time.sleep(0.5)
    
    # Entrer le mot de passe
    login.send_keys(*login.PASSWORD, "secret_sauce")
    time.sleep(0.5)
    
    # Cliquer sur le bouton LOGIN
    login.click(*login.LOGIN_BTN)
    time.sleep(3)
    
    # Vérifier qu'on est sur la page PRODUCTS (succès du login)
    try:
        products_element = driver.find_element("accessibility id", "test-PRODUCTS")
        assert products_element is not None, f"PRODUCTS page not found after login for {username}"
    except Exception as e:
        # Fallback: vérifier PRODUCTS dans la page source
        assert "PRODUCTS" in driver.page_source, f"BUG APP - Login échoué pour {username} (accepted user): {str(e)}"
    
    # Logout pour revenir à la page de login
    home = HomePage(driver)
    home.logout()


def TC3_login_with_empty_fields(driver):
    """Test login avec champs vides - ne doit pas se connecter."""
    login = LoginPage(driver)
    time.sleep(1)
    
    # Ne pas remplir les champs, juste cliquer LOGIN
    login.click(*login.LOGIN_BTN)
    time.sleep(2)
    
    # Vérifier qu'on est toujours sur la page de login (pas de redirection)
    assert login.find(*login.USERNAME) is not None, "Should still be on login page"
    
    # Vérifier qu'on n'est PAS sur la page PRODUCTS
    assert "PRODUCTS" not in driver.page_source, "Should not be logged in with empty fields"


def TC4_login_with_wrong_password(driver):
    """Test login avec bon username mais mauvais password - ne doit pas se connecter."""
    login = LoginPage(driver)
    time.sleep(1)
    
    # Entrer un bon username mais un mauvais password
    login.send_keys(*login.USERNAME, "standard_user")
    time.sleep(0.5)
    login.send_keys(*login.PASSWORD, "wrong_password")
    time.sleep(0.5)
    
    # Cliquer LOGIN
    login.click(*login.LOGIN_BTN)
    time.sleep(2)
    
    # Vérifier qu'on est toujours sur la page de login (pas de redirection)
    assert login.find(*login.USERNAME) is not None, "Should still be on login page"
    
    # Vérifier qu'on n'est PAS sur la page PRODUCTS
    assert "PRODUCTS" not in driver.page_source, "Should not be logged in with wrong password"


def TC5_login_with_wrong_username(driver):
    """Test login avec mauvais username et bon password - ne doit pas se connecter."""
    login = LoginPage(driver)
    time.sleep(1)
    
    # Entrer un mauvais username avec le bon password
    login.send_keys(*login.USERNAME, "nonexistent_user")
    time.sleep(0.5)
    login.send_keys(*login.PASSWORD, "secret_sauce")
    time.sleep(0.5)
    
    # Cliquer LOGIN
    login.click(*login.LOGIN_BTN)
    time.sleep(2)
    
    # Vérifier qu'on est toujours sur la page de login (pas de redirection)
    assert login.find(*login.USERNAME) is not None, "Should still be on login page"
    
    # Vérifier qu'on n'est PAS sur la page PRODUCTS
    assert "PRODUCTS" not in driver.page_source, "Should not be logged in with wrong username"


def TC6_login_tc03_empty_password(driver):
    """TC03 – Password vide (Boundary-based testing)
    
    Cas de test : Entrer un username valide mais laisser le password vide.
    Technique : Boundary-based testing (valeur limite / champ obligatoire non rempli)
    Résultat attendu : La connexion doit échouer; l'utilisateur reste sur la page de login.
    """
    login = LoginPage(driver)
    time.sleep(1)
    
    # Entrer username valide
    login.send_keys(*login.USERNAME, "standard_user")
    time.sleep(0.5)
    
    # NE PAS remplir le password (laisser vide)
    # On clique directement sur LOGIN
    login.click(*login.LOGIN_BTN)
    time.sleep(2)
    
    # Vérifier qu'on est toujours sur la page de login (pas de redirection)
    assert login.find(*login.USERNAME) is not None, "Should still be on login page with empty password"
    
    # Vérifier qu'on n'est PAS sur la page PRODUCTS
    assert "PRODUCTS" not in driver.page_source, "Login should fail with empty password"


def TC7_login_tc04_empty_username(driver):
    """TC04 – Username vide (Boundary-based testing)
    
    Cas de test : Laisser le username vide et entrer un password valide.
    Technique : Boundary-based testing (valeur limite / champ obligatoire non rempli)
    Résultat attendu : La connexion doit échouer; l'utilisateur reste sur la page de login.
    """
    login = LoginPage(driver)
    time.sleep(1)
    
    # NE PAS remplir le username (laisser vide)
    # Entrer password valide
    login.send_keys(*login.PASSWORD, "secret_sauce")
    time.sleep(0.5)
    
    # Cliquer sur LOGIN
    login.click(*login.LOGIN_BTN)
    time.sleep(2)
    
    # Vérifier qu'on est toujours sur la page de login (pas de redirection)
    assert login.find(*login.USERNAME) is not None, "Should still be on login page with empty username"
    
    # Vérifier qu'on n'est PAS sur la page PRODUCTS
    assert "PRODUCTS" not in driver.page_source, "Login should fail with empty username"


def TC8_login_tc07_fields_exceeding_limit(driver):
    """TC07 – Champs dépassant la limite (Boundary-based testing)
    
    Cas de test : Entrer des valeurs excessivement longues (200 caractères) 
                  dans les champs username et password.
    Technique : Boundary-based testing (dépassement de limite, validation des entrées)
    
    Résultat attendu : 
    - La connexion doit échouer (aucun user avec un username de 200 chars).
    - L'application NE DOIT PAS retourner d'erreur serveur 500.
    - L'utilisateur reste sur la page de login avec message d'erreur clair.
    
    BUG ATTENDU : L'app retourne 500 au lieu de gérer l'entrée long gracefully.
    """
    login = LoginPage(driver)
    time.sleep(1)
    
    # Générer des chaînes dépassant les limites (200 caractères)
    long_username = "a" * 200  # 200 caractères 'a'
    long_password = "b" * 200  # 200 caractères 'b'
    
    # Entrer les valeurs longues
    login.send_keys(*login.USERNAME, long_username)
    time.sleep(0.5)
    login.send_keys(*login.PASSWORD, long_password)
    time.sleep(0.5)
    
    # Cliquer LOGIN
    login.click(*login.LOGIN_BTN)
    time.sleep(2)
    
    # Vérifier qu'on est toujours sur la page de login (pas de redirection réussie)
    assert login.find(*login.USERNAME) is not None, "Should still be on login page with oversized fields"
    
    # Vérifier qu'on n'est PAS sur la page PRODUCTS
    assert "PRODUCTS" not in driver.page_source, "Login should fail with oversized fields"
    
    # === BUG DETECTION ===
    # L'application devrait rejeter gracefully les entrées trop longues (ex: message "Invalid input")
    # Mais au lieu de cela, elle retourne une erreur 500 (Internal Server Error)
    has_500_error = "500" in driver.page_source
    has_graceful_error = "invalid" in driver.page_source.lower() or \
                         "error" in driver.page_source.lower() or \
                         "too long" in driver.page_source.lower()
    
    # Documenter le bug trouvé
    if has_500_error:
        pytest.fail(
            "BUG FOUND: Server returns 500 error for oversized input.\n"
            "Expected: Graceful error message or client-side validation.\n"
            "Actual: HTTP 500 Internal Server Error.\n"
            "Root cause: Missing input validation on server-side or client-side length limits.\n"
            "Severity: HIGH - Application crashes on boundary input."
        )
    elif not has_graceful_error:
        # Si pas d'erreur 500 ET pas de message d'erreur = problème
        pytest.fail(
            "Unclear behavior: No error 500, but also no clear error message.\n"
            "App should either: reject client-side OR show validation error."
        )
