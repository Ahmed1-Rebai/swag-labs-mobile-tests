"""
Tests de Stress
Techniques : Stress testing, Load testing basique
Objectif : Tester stabilité sous charge répétée
"""

import time
import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.checkout_page import CheckoutPage

# ==================== Stress Tests ====================

@pytest.mark.stress
def TC44_stress_add_remove_product_cycles(driver):
    """Stress Test : 20 cycles add/remove product
    
    Technique : Stress testing (répétition d'opérations)
    Objectif : Vérifier stabilité de l'app sous opérations répétées
    
    Étapes :
    1. Se connecter
    2. Répéter 20 fois : ajouter un produit → retirer ce produit
    3. Vérifier que le panier est vide à la fin
    4. Vérifier qu'il n'y a pas d'erreur après 20 cycles
    
    Résultat attendu : Tous les 20 cycles complétés sans crash
    """
    login = LoginPage(driver)
    home = HomePage(driver)
    
    # === Connexion ===
    login.send_keys(*login.USERNAME, "standard_user")
    time.sleep(0.1)
    login.send_keys(*login.PASSWORD, "secret_sauce")
    time.sleep(0.1)
    login.click(*login.LOGIN_BTN)
    time.sleep(1)
    
    # === Stress test : 20 cycles ===
    num_cycles = 20
    failed_cycles = 0
    cycle_times = []
    
    print(f"\n🔄 Starting {num_cycles} add/remove cycles...")
    
    for cycle in range(1, num_cycles + 1):
        try:
            cycle_start = time.perf_counter()
            
            # Ajouter le premier produit (index 0)
            home.add_to_cart(item_index=0)
            time.sleep(0.3)
            
            # Vérifier que le panier compte est > 0
            cart_count = home.get_cart_count()
            assert cart_count > 0, f"Cycle {cycle}: Cart count should be > 0 after add"
            
            # Retirer le produit (index 0)
            home.remove_from_cart(item_index=0)
            time.sleep(0.3)
            
            # Vérifier que le panier est revenu à 0
            cart_count = home.get_cart_count()
            assert cart_count == 0, f"Cycle {cycle}: Cart should be empty after remove"
            
            cycle_time = (time.perf_counter() - cycle_start) * 1000
            cycle_times.append(cycle_time)
            
            print(f"  Cycle {cycle}/{num_cycles}: ✓ Pass ({cycle_time:.0f}ms)")
            
        except Exception as e:
            failed_cycles += 1
            print(f"  Cycle {cycle}/{num_cycles}: ✗ FAIL - {str(e)}")
    
    # === Assertions finales ===
    assert failed_cycles == 0, \
        f"Stress test failed: {failed_cycles}/{num_cycles} cycles failed"
    
    # Vérifier que le panier est vide à la fin
    final_cart_count = home.get_cart_count()
    assert final_cart_count == 0, \
        f"Final cart should be empty after all cycles, but has {final_cart_count} items"
    
    # Statistiques
    avg_cycle_time = sum(cycle_times) / len(cycle_times) if cycle_times else 0
    min_cycle_time = min(cycle_times) if cycle_times else 0
    max_cycle_time = max(cycle_times) if cycle_times else 0
    
    print(f"\n✓ All {num_cycles} add/remove cycles completed successfully")
    print(f"  Average cycle time: {avg_cycle_time:.0f}ms")
    print(f"  Min cycle time: {min_cycle_time:.0f}ms")
    print(f"  Max cycle time: {max_cycle_time:.0f}ms")
    print(f"  Total time: {sum(cycle_times):.0f}ms ({sum(cycle_times)/1000:.2f}s)")
    
    # Cleanup
    home.logout()


@pytest.mark.stress
def TC45_stress_login_logout_cycles(driver):
    """Stress Test : 20 cycles login/logout
    
    Technique : Stress testing (répétition sessions)
    Objectif : Vérifier stabilité des sessions et gestion mémoire
    
    Étapes :
    1. Répéter 20 fois : login → vérifier produits → logout
    2. Chaque cycle doit réussir (login → PRODUCTS page → logout)
    3. Vérifier qu'il n'y a pas de crash ou fuite mémoire
    
    Résultat attendu : Tous les 20 cycles réussis
    """
    login = LoginPage(driver)
    home = HomePage(driver)
    
    num_cycles = 20
    failed_cycles = 0
    times = []
    
    for cycle in range(1, num_cycles + 1):
        try:
            cycle_start = time.perf_counter()
            
            # === Login ===
            login.send_keys(*login.USERNAME, "standard_user")
            time.sleep(0.1)
            login.send_keys(*login.PASSWORD, "secret_sauce")
            time.sleep(0.1)
            login.click(*login.LOGIN_BTN)
            time.sleep(0.5)
            
            # === Vérifier affichage PRODUCTS ===
            products_elem = driver.find_element("accessibility id", "test-PRODUCTS")
            assert products_elem is not None, f"Cycle {cycle}: PRODUCTS page not found"
            
            # === Logout ===
            home.logout()
            time.sleep(0.1)
            
            # === Vérifier retour page login ===
            login_elem = driver.find_element(*login.USERNAME)
            assert login_elem is not None, f"Cycle {cycle}: Not returned to login page"
            
            cycle_time = (time.perf_counter() - cycle_start) * 1000
            times.append(cycle_time)
            
            print(f"  Cycle {cycle}/{num_cycles}: ✓ Pass ({cycle_time:.0f}ms)")
            
        except Exception as e:
            failed_cycles += 1
            print(f"  Cycle {cycle}/{num_cycles}: ✗ FAIL - {str(e)}")
    
    # === Assertions finales ===
    assert failed_cycles == 0, \
        f"Login/logout stress test failed: {failed_cycles}/{num_cycles} cycles failed"
    
    # Statistiques de performance
    avg_time = sum(times) / len(times) if times else 0
    min_time = min(times) if times else 0
    max_time = max(times) if times else 0
    
    print(f"\n✓ All {num_cycles} login/logout cycles completed")
    print(f"  Average cycle time: {avg_time:.0f}ms")
    print(f"  Min cycle time: {min_time:.0f}ms")
    print(f"  Max cycle time: {max_time:.0f}ms")


# ==================== Load Tests ====================

@pytest.mark.stress
def TC46_load_scroll_products_list_to_bottom(driver):
    """Test de Charge : 50 scrolls rapides (haut/bas alternés) sur la liste produits
    
    Technique : Load testing basique (répétition d'action UI)
    Objectif : Scroller 50 fois rapidement (alternant haut et bas) et mesurer temps de réponse
    
    Étapes :
    1. Se connecter
    2. Scroller 50 fois vers le bas ET vers le haut (alternativement)
    3. Mesurer temps total et temps par scroll (min/max/avg)
    4. Vérifier qu'il n'y a pas de crash ou lag excessif
    
    Résultat attendu : 50 scrolls complétés (25 down + 25 up), temps moyen < 1.5s par scroll
    """
    login = LoginPage(driver)
    home = HomePage(driver)
    
    # === Connexion ===
    login.send_keys(*login.USERNAME, "standard_user")
    login.send_keys(*login.PASSWORD, "secret_sauce")
    login.click(*login.LOGIN_BTN)
    time.sleep(1)
    
    # === Load test : Exactement 50 scrolls rapides (alternant haut/bas) ===
    num_scrolls = 50
    scroll_times = []
    failed_scrolls = 0
    
    # Obtenir dimensions de la fenêtre pour le scroll
    window_size = driver.get_window_size()
    start_x = window_size['width'] // 2
    start_y = window_size['height'] // 2
    scroll_distance = 1000  # Distance de scroll
    
    print(f"\n📱 Scrolling product list {num_scrolls} times (alternating up/down)...")
    print(f"  Window size: {window_size['width']}x{window_size['height']}")
    print(f"  Scroll distance: {scroll_distance}px")
    
    # Mesurer le temps total
    test_start_time = time.perf_counter()
    
    for scroll_num in range(1, num_scrolls + 1):
        try:
            scroll_start = time.perf_counter()
            
            # Alterner : scroll down (impair) et scroll up (pair)
            if scroll_num % 2 == 1:
                # Scroll DOWN
                driver.swipe(start_x, start_y, start_x, start_y - scroll_distance, duration=300)
            else:
                # Scroll UP
                driver.swipe(start_x, start_y, start_x, start_y + scroll_distance, duration=300)
            
            time.sleep(0.1)  # Minimal wait for render
            
            scroll_time = (time.perf_counter() - scroll_start) * 1000
            scroll_times.append(scroll_time)
            
            # Afficher progression tous les 10 scrolls
            if scroll_num % 10 == 0:
                direction = "↓" if scroll_num % 2 == 1 else "↑"
                print(f"  Scroll {scroll_num}/{num_scrolls} {direction}: ✓ ({scroll_time:.0f}ms)")
        
        except Exception as e:
            failed_scrolls += 1
            print(f"  Scroll {scroll_num}: ✗ FAIL - {str(e)}")
    
    test_total_time = (time.perf_counter() - test_start_time) * 1000
    
    # === Assertions finales ===
    assert failed_scrolls < num_scrolls * 0.1, \
        f"Too many scroll failures: {failed_scrolls}/{num_scrolls}"
    
    # Statistiques de performance
    avg_scroll = sum(scroll_times) / len(scroll_times) if scroll_times else 0
    min_scroll = min(scroll_times) if scroll_times else 0
    max_scroll = max(scroll_times) if scroll_times else 0
    
    threshold_avg_ms = 1500  # Chaque scroll en moyenne < 1.5s
    assert avg_scroll < threshold_avg_ms, \
        f"Average scroll time {avg_scroll:.0f}ms exceeds threshold {threshold_avg_ms}ms"
    
    # Afficher résumé détaillé
    print(f"\n✓ Successfully completed {num_scrolls} rapid scrolls (alternating up/down)")
    print(f"  Total time: {test_total_time:.0f}ms ({test_total_time/1000:.2f}s)")
    print(f"  Average scroll time: {avg_scroll:.0f}ms (threshold: {threshold_avg_ms}ms)")
    print(f"  Min scroll time: {min_scroll:.0f}ms")
    print(f"  Max scroll time: {max_scroll:.0f}ms")
    print(f"  Failed scrolls: {failed_scrolls}/{num_scrolls}")
    print(f"  Success rate: {((num_scrolls - failed_scrolls) / num_scrolls * 100):.1f}%")
    print(f"  Scrolls down: {(num_scrolls + 1) // 2}, Scrolls up: {num_scrolls // 2}")
    
    # Cleanup
    home.logout()