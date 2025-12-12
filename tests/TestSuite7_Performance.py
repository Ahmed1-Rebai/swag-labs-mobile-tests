"""
Tests de Performance
Techniques : Performance testing
Objectif : Mesurer temps de réponse
"""

import time
import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.checkout_page import CheckoutPage

# ==================== Performance Tests ====================

@pytest.mark.performance
def TC42_performance_products_page_load_time(driver):
    """Test de Performance : Temps de chargement de l'écran "Products"
    
    Technique : Test de performance (mesure de temps)
    Objectif : Vérifier que la page produits se charge en < 3 secondes
    
    Étapes :
    1. Se connecter avec un utilisateur valide
    2. Mesurer le temps d'affichage de la page PRODUCTS
    3. Vérifier que le temps de réponse est acceptable
    
    Seuil de performance : < 3000ms
    """
    login = LoginPage(driver)
    time.sleep(1)
    
    # === Étape 1 : Connexion ===
    login.send_keys(*login.USERNAME, "standard_user")
    time.sleep(0.1)
    login.send_keys(*login.PASSWORD, "secret_sauce")
    time.sleep(0.1)
    
    # === Étape 2 : Mesurer le temps de chargement de la page PRODUCTS ===
    start_time = time.perf_counter()
    login.click(*login.LOGIN_BTN)
    
    # Attendre que la page PRODUCTS soit affichée
    timeout = 5
    elapsed = 0
    while elapsed < timeout:
        try:
            products_elem = driver.find_element("accessibility id", "test-PRODUCTS")
            if products_elem:
                break
        except:
            pass
        time.sleep(0.1)
        elapsed = time.perf_counter() - start_time
    
    end_time = time.perf_counter()
    load_time_ms = (end_time - start_time) * 1000
    
    # === Étape 3 : Assertions ===
    # Vérifier que la page est affichée
    assert driver.find_element("accessibility id", "test-PRODUCTS") is not None, \
        "Products page should be displayed"
    
    # Vérifier le temps de réponse
    threshold_ms = 3000
    assert load_time_ms < threshold_ms, \
        f"Page load time {load_time_ms:.2f}ms exceeds threshold {threshold_ms}ms"
    
    # Rapport de performance
    print(f"\n✓ Products page loaded in {load_time_ms:.2f}ms (threshold: {threshold_ms}ms)")
    
    # Cleanup
    home = HomePage(driver)
    home.logout()



@pytest.mark.performance
def TC43_performance_full_checkout_process(driver):
    """Test de Performance Fort : Temps complet du processus d'achat end-to-end
    
    Technique : Test de performance avancé (mesure temps total + étapes intermédiaires)
    Objectif : Mesurer les performances du processus complet d'achat depuis le login
               jusqu'à la confirmation de commande
    
    Étapes mesurées :
    1. Login
    2. Ajout de 2 produits au panier
    3. Navigation vers le panier
    4. Passage au checkout
    5. Remplissage du formulaire de livraison
    6. Finalisation de la commande
    
    Seuils de performance :
    - Temps total : < 20 secondes
    - Chaque étape : < 3-6 secondes
    
    Résultat attendu : Processus fluide sans blocages
    """
    login = LoginPage(driver)
    home = HomePage(driver)
    checkout = CheckoutPage(driver)
    
    time.sleep(1)
    overall_start = time.perf_counter()
    
    # === Étape 1 : Connexion (mesurée) ===
    step_start = time.perf_counter()
    login.send_keys(*login.USERNAME, "standard_user")
    time.sleep(0.2)
    login.send_keys(*login.PASSWORD, "secret_sauce")
    time.sleep(0.2)
    login.click(*login.LOGIN_BTN)
    
    # Attendre produits
    timeout = 5
    while (time.perf_counter() - step_start) < timeout:
        try:
            driver.find_element("accessibility id", "test-PRODUCTS")
            break
        except:
            time.sleep(0.1)
    
    login_time = (time.perf_counter() - step_start) * 1000
    print(f"✓ Login completed in {login_time:.2f}ms")
    assert login_time < 5000, f"Login too slow: {login_time:.2f}ms"
    
    # === Étape 2 : Ajout de produits (mesuré) ===
    step_start = time.perf_counter()
    home.add_to_cart(item_index=0)  # Premier produit
    time.sleep(0.5)
    home.add_to_cart(item_index=1)  # Deuxième produit
    
    add_time = (time.perf_counter() - step_start) * 1000
    print(f"✓ Added 2 products in {add_time:.2f}ms")
    assert add_time < 4000, f"Adding products too slow: {add_time:.2f}ms"
    
    # Vérifier panier
    cart_count = home.get_cart_count()
    assert cart_count == 2, f"Expected 2 items in cart, got {cart_count}"
    
    # === Étape 3 : Navigation panier (mesurée) ===
    step_start = time.perf_counter()
    home.click_cart_icon()
    
    # Attendre page panier
    timeout = 3
    while (time.perf_counter() - step_start) < timeout:
        try:
            driver.find_element("accessibility id", "test-CHECKOUT")
            break
        except:
            time.sleep(0.1)
    
    cart_time = (time.perf_counter() - step_start) * 1000
    print(f"✓ Cart navigation in {cart_time:.2f}ms")
    assert cart_time < 3000, f"Cart navigation too slow: {cart_time:.2f}ms"
    
    # === Étape 4 : Checkout (mesuré) ===
    step_start = time.perf_counter()
    # Click checkout button from cart page
    checkout_btn = driver.find_element("accessibility id", "test-CHECKOUT")
    checkout_btn.click()
    
    # Attendre formulaire
    timeout = 3
    while (time.perf_counter() - step_start) < timeout:
        try:
            driver.find_element("accessibility id", "test-First Name")
            break
        except:
            time.sleep(0.1)
    
    checkout_time = (time.perf_counter() - step_start) * 1000
    print(f"✓ Checkout navigation in {checkout_time:.2f}ms")
    assert checkout_time < 3000, f"Checkout navigation too slow: {checkout_time:.2f}ms"
    
    # === Étape 5 : Remplissage formulaire (mesuré) ===
    step_start = time.perf_counter()
    checkout.enter_user_info("John", "Doe", "12345")
    checkout.click_continue_button()
    
    # Attendre page overview
    timeout = 3
    while (time.perf_counter() - step_start) < timeout:
        try:
            driver.find_element("accessibility id", "test-FINISH")
            break
        except:
            time.sleep(0.1)
    
    form_time = (time.perf_counter() - step_start) * 1000
    print(f"✓ Form filling in {form_time:.2f}ms")
    assert form_time < 6000, f"Form filling too slow: {form_time:.2f}ms"
    
    # === Étape 6 : Finalisation commande (mesurée) ===
    step_start = time.perf_counter()
    checkout.click_finish_button()
    
    # Attendre confirmation
    timeout = 5
    while (time.perf_counter() - step_start) < timeout:
        try:
            driver.find_element("accessibility id", "test-BACK HOME")
            break
        except:
            time.sleep(0.1)
    
    finish_time = (time.perf_counter() - step_start) * 1000
    print(f"✓ Order completion in {finish_time:.2f}ms")
    assert finish_time < 5000, f"Order completion too slow: {finish_time:.2f}ms"
    
    # === Résumé performance globale ===
    total_time = (time.perf_counter() - overall_start) * 1000
    threshold_total = 20000  # 20 secondes
    
    print(f"\n🎯 PERFORMANCE SUMMARY:")
    print(f"  Total checkout process: {total_time:.2f}ms (threshold: {threshold_total}ms)")
    print(f"  ✓ Login: {login_time:.2f}ms")
    print(f"  ✓ Add products: {add_time:.2f}ms")
    print(f"  ✓ Cart navigation: {cart_time:.2f}ms")
    print(f"  ✓ Checkout navigation: {checkout_time:.2f}ms")
    print(f"  ✓ Form filling: {form_time:.2f}ms")
    print(f"  ✓ Order completion: {finish_time:.2f}ms")
    
    assert total_time < threshold_total, \
        f"Total checkout time {total_time:.2f}ms exceeds threshold {threshold_total}ms"
    
    print(f"\n✅ FULL CHECKOUT PERFORMANCE TEST PASSED – Process completed in {total_time:.2f}ms")
