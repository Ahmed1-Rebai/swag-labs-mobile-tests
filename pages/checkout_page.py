from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class CheckoutPage(BasePage):
    """
    Page Object Model pour les étapes du processus de paiement (Checkout).
    """
    
    # Étape 1: Vos informations (Your Information)
    FIRST_NAME = (AppiumBy.ACCESSIBILITY_ID, "test-First Name")
    LAST_NAME = (AppiumBy.ACCESSIBILITY_ID, "test-Last Name")
    POSTAL_CODE = (AppiumBy.ACCESSIBILITY_ID, "test-Zip/Postal Code")
    CONTINUE_BTN = (AppiumBy.ACCESSIBILITY_ID, "test-CONTINUE")
    CANCEL_BTN = (AppiumBy.ACCESSIBILITY_ID, "test-cancel")
    
    # Étape 2: Aperçu (Overview)
    FINISH_BTN = (AppiumBy.ACCESSIBILITY_ID, "test-FINISH")
    
    # Étape 3: Confirmation (Complete)
    BACK_HOME_BTN = (AppiumBy.ACCESSIBILITY_ID, "test-Back Home")
    
    def __init__(self, driver):
        super().__init__(driver)
        
    # Valeurs par défaut utilisables dans les tests
    DEFAULT_FIRST_NAME = "John"
    DEFAULT_LAST_NAME = "Doe"
    DEFAULT_POSTAL_CODE = "12345"

    def enter_user_info(self, first_name, last_name, postal_code):
        """Remplir les champs d'information du client."""
        if first_name is None:
            first_name = self.DEFAULT_FIRST_NAME
        if last_name is None:
            last_name = self.DEFAULT_LAST_NAME
        if postal_code is None:
            postal_code = self.DEFAULT_POSTAL_CODE
        self.send_keys(*self.FIRST_NAME, first_name)
        self.send_keys(*self.LAST_NAME, last_name)
        self.send_keys(*self.POSTAL_CODE, postal_code)
        
    def click_continue_button(self):
        """Clique sur le bouton Continuer."""
        self.click(*self.CONTINUE_BTN)

    def click_cancel_button(self):
        """Clique sur le bouton Annuler."""
        try:
            self.click(*self.CANCEL_BTN)
        except Exception:
            # fallbacks for different app variants
            try:
                self.driver.find_element("accessibility id", "test-CANCEL").click()
                return
            except Exception:
                pass
            try:
                el = self.driver.find_element("xpath", "//android.widget.Button[contains(@text, 'CANCEL') or contains(@text, 'Cancel')]")
                el.click()
                return
            except Exception:
                raise

    def click_finish_button(self):
        """Clique sur le bouton Finaliser (étape Aperçu)."""
        try:
            # try normal click
            self.click(*self.FINISH_BTN)
        except Exception:
            # try to find with scroll and click
            try:
                el = self.find_with_scroll(self.FINISH_BTN[0], self.FINISH_BTN[1], max_swipes=6)
                el.click()
            except Exception:
                # fallback to xpath search
                el = self.driver.find_element("xpath", "//android.widget.Button[contains(@text, 'FINISH') or contains(@text, 'Finish')]")
                el.click()
        
    def click_back_home(self):
        """Clique sur le bouton Retour à l'accueil (après confirmation)."""
        try:
            self.click(*self.BACK_HOME_BTN)
        except Exception:
            try:
                el = self.find_with_scroll(self.BACK_HOME_BTN[0], self.BACK_HOME_BTN[1], max_swipes=6)
                el.click()
                return
            except Exception:
                # fallback to xpath/button text
                el = self.driver.find_element("xpath", "//android.widget.Button[contains(@text, 'Back Home') or contains(@text, 'BACK HOME') or contains(@text, 'Back to Home')]")
                el.click()

    def enter_user_info_default(self):
        """Convenience helper to fill default test user info."""
        self.enter_user_info(None, None, None)