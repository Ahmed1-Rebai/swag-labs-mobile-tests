from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage






class HomePage(BasePage):
    # Les sélecteurs pour l'app Swag Labs
    USERNAME_INPUT = (AppiumBy.ACCESSIBILITY_ID, "test-Username")
    PASSWORD_INPUT = (AppiumBy.ACCESSIBILITY_ID, "test-Password")
    LOGIN_BTN = (AppiumBy.ACCESSIBILITY_ID, "test-LOGIN")
    MENU_BTN = (AppiumBy.ACCESSIBILITY_ID, "test-Menu")
    LOGOUT_BTN = (AppiumBy.ACCESSIBILITY_ID, "test-LOGOUT")


    def go_to_login(self):
        # Cette app démarre directement sur la page de login
        # Donc aucune navigation n'est nécessaire
        pass


    def login(self, username, password):
        by, value = self.USERNAME_INPUT
        self.send_keys(by, value, username)
        by, value = self.PASSWORD_INPUT
        self.send_keys(by, value, password)
        self.click(*self.LOGIN_BTN)

    def logout(self):
        """Logout en cliquant sur Menu puis LOGOUT."""
        import time
        try:
            # Cliquer sur le bouton Menu
            self.click(*self.MENU_BTN)
            time.sleep(1)
            # Cliquer sur le bouton LOGOUT
            self.click(*self.LOGOUT_BTN)
            time.sleep(2)
        except Exception as e:
            print(f"Logout failed: {str(e)}")

    # --- Helpers pour la page des produits / panier ---
    def get_cart_count(self):
        """Retourne le nombre d'articles dans le panier.

        Implémentation simple : compte les boutons 'REMOVE' (élément visible quand un article est ajouté).
        Si aucun bouton 'REMOVE' n'est trouvé, retourne 0.
        """
        try:
            removes = self.driver.find_elements("accessibility id", "test-REMOVE")
            return len(removes)
        except Exception:
            return 0

    def add_to_cart(self, item_index=0):
        """Ajoute l'article à l'index `item_index` sur la page des produits."""
        try:
            # Try common accessibility id first
            # Wait briefly for buttons to appear (some devices need rendering time)
            import time
            timeout = 5
            interval = 0.5
            elapsed = 0.0
            add_buttons = []
            while elapsed < timeout:
                add_buttons = self.driver.find_elements("accessibility id", "test-ADD TO CART")
                if add_buttons:
                    break
                time.sleep(interval)
                elapsed += interval
            # Fallback: try case-insensitive text buttons
            if not add_buttons:
                add_buttons = self.driver.find_elements("xpath", "//android.widget.Button[contains(@text, 'ADD TO CART') or contains(@text, 'Add to Cart')]")
            if not add_buttons:
                # Another fallback: buttons inside product items
                add_buttons = self.driver.find_elements("xpath", "//android.view.ViewGroup//android.widget.Button")

            if len(add_buttons) > item_index:
                add_buttons[item_index].click()
            else:
                # Try to scroll the list to load more items and retry
                try:
                    # Try to find any other available add button (click last available)
                    if add_buttons:
                        add_buttons[-1].click()
                        return
                    for _ in range(4):
                        # simple swipe up to reveal more items
                        size = self.driver.get_window_size()
                        start_x = size['width'] // 2
                        start_y = int(size['height'] * 0.8)
                        end_y = int(size['height'] * 0.3)
                        try:
                            self.driver.swipe(start_x, start_y, start_x, end_y, 600)
                        except Exception:
                            # fallback to W3C action if swipe not supported
                            try:
                                self.driver.execute_script('mobile: swipe', {'direction': 'up'})
                            except Exception:
                                pass
                        time.sleep(0.8)
                        add_buttons = self.driver.find_elements("accessibility id", "test-ADD TO CART")
                        if add_buttons and len(add_buttons) > item_index:
                            add_buttons[item_index].click()
                            return
                    # final fallback: click any add button by xpath
                    add_buttons = self.driver.find_elements("xpath", "//android.widget.Button[contains(@text, 'ADD TO CART') or contains(@text, 'Add to Cart')]")
                    if add_buttons:
                        add_buttons[0].click()
                        return
                except Exception:
                    pass
                raise IndexError("Not enough add-to-cart buttons found")
        except Exception as e:
            raise

    def remove_from_cart(self, item_index=0):
        """Retire l'article à l'index `item_index` depuis la page des produits (bouton REMOVE)."""
        try:
            rem_buttons = self.driver.find_elements("accessibility id", "test-REMOVE")
            if not rem_buttons:
                rem_buttons = self.driver.find_elements("xpath", "//android.widget.Button[contains(@text, 'REMOVE') or contains(@text, 'Remove')]")

            if len(rem_buttons) > item_index:
                rem_buttons[item_index].click()
            else:
                raise IndexError("Not enough remove buttons found")
        except Exception as e:
            raise

    def click_cart_icon(self):
        """Clique sur l'icône du panier pour ouvrir la page du panier."""
        try:
            cart = self.driver.find_element("accessibility id", "test-Cart")
            cart.click()
        except Exception:
            # fallback: try finding by content-desc containing 'Cart'
            elems = self.driver.find_elements("xpath", "//*[contains(@content-desc, 'Cart') or contains(@content-desc, 'cart')]")
            if elems:
                elems[0].click()
            else:
                raise
        # Wait for cart page to load (checkout button appears)
        try:
            # Use scroll-aware finder to ensure checkout button is visible
            self.find_with_scroll("accessibility id", "test-CHECKOUT", max_swipes=6)
            return
        except Exception:
            # Try fallback ids/texts
            try:
                self.find_with_scroll("xpath", "//android.widget.Button[contains(@text, 'CHECKOUT') or contains(@text, 'Checkout') or contains(@content-desc, 'CHECKOUT') or contains(@content-desc, 'Checkout')]")
                return
            except Exception:
                # give up - caller will see missing element
                return

    def select_sort_option(self, option_label):
        """Ouvre le menu de tri et sélectionne l'option correspondant à `option_label` (texte visible)."""
        try:
            # Try multiple selectors that may open the sorting modal
            toggle_selectors = [
                ("xpath", "//android.view.ViewGroup[@content-desc=\"test-Modal Selector Button\"]/android.view.ViewGroup/android.view.ViewGroup/android.widget.ImageView"),
                ("accessibility id", "test-Modal Selector"),
                ("accessibility id", "test-Sort"),
                ("accessibility id", "test-Toggle"),
                ("accessibility id", "test-Options"),
                ("xpath", "//android.widget.ImageView[contains(@content-desc, 'sort') or contains(@content-desc, 'Sort')]")
            ]
            opened = False
            for by, val in toggle_selectors:
                try:
                    elems = self.driver.find_elements(by, val)
                    if elems:
                        elems[0].click()
                        opened = True
                        break
                except Exception:
                    continue
            if not opened:
                # last resort: find any element with text 'Sort' or 'SORT'
                try:
                    el = self.driver.find_element("xpath", "//*[contains(translate(@text, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sort') or contains(translate(@content-desc, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sort')]")
                    el.click()
                except Exception:
                    # give up and raise
                    raise
            # Chercher l'option par texte de façon robuste (ignore la casse)
            # Look for common option element types (CheckedTextView, TextView)
            candidates = self.driver.find_elements("xpath", "//android.widget.CheckedTextView | //android.widget.TextView")
            matched = False
            def normalize(s):
                import re
                return re.sub(r'[^a-z0-9]', '', (s or '').lower())

            target_norm = normalize(option_label)
            for opt in candidates:
                try:
                    text = opt.text or ""
                    if not text:
                        continue
                    if target_norm in normalize(text) or normalize(text) in target_norm:
                        opt.click()
                        matched = True
                        break
                except Exception:
                    continue
            if not matched:
                # Wait and re-fetch candidates (spinner implementations may render after a brief delay)
                import time
                time.sleep(0.5)
                candidates = self.driver.find_elements("xpath", "//android.widget.CheckedTextView | //android.widget.TextView")
                for opt in candidates:
                    try:
                        text = opt.text or ""
                        if target_norm in normalize(text) or normalize(text) in target_norm:
                            opt.click()
                            matched = True
                            break
                    except Exception:
                        continue
            if not matched:
                # Last resort: try exact text match
                opt = self.driver.find_element("xpath", f"//android.widget.TextView[@text='{option_label}']")
                opt.click()
        except Exception:
            # si échec, lever pour que le test le signale
            raise

    def get_all_product_prices(self):
        """Retourne la liste des prix affichés sur la page des produits, sous forme de strings (ex: '$29.99')."""
        prices = []
        try:
            elems = self.driver.find_elements("accessibility id", "test-Price")
            for e in elems:
                prices.append(e.text)
            if not prices:
                # fallback: xpath by resource-id or text pattern
                elems = self.driver.find_elements("xpath", "//android.widget.TextView[contains(@text, '$')]")
                for e in elems:
                    prices.append(e.text)
        except Exception:
            pass
        return prices

    def get_all_product_names(self):
        """Retourne la liste des noms de produits visibles."""
        names = []
        try:
            elems = self.driver.find_elements("accessibility id", "test-Item title")
            if not elems:
                # fallback: find product title TextViews by common resource id patterns
                elems = self.driver.find_elements("xpath", "//android.widget.TextView[contains(@resource-id, 'title') or contains(@resource-id, 'name') or contains(@content-desc, 'title')]")
            if not elems:
                # last resort: any TextView under product items (but filter out non-product labels)
                elems = self.driver.find_elements("xpath", "//android.view.ViewGroup//android.widget.TextView")
            for e in elems:
                txt = (e.text or '').strip()
                # filter out empty, price-like, button labels, and generic navigation labels
                if not txt:
                    continue
                if '$' in txt:
                    continue
                up = txt.upper()
                if up in ("ADD TO CART", "REMOVE", "BACK TO PRODUCTS", "BACK TO HOME", "CHECKOUT", "CANCEL"):
                    continue
                # ignore pure digits or short single-letter labels
                if txt.isdigit() or len(txt) < 2:
                    continue
                names.append(txt)
        except Exception:
            pass
        return names

    def get_all_product_image_sources(self):
        """Retourne une liste de 'sources' des images; si aucune source disponible, retourne leurs bounds ou empty strings."""
        sources = []
        try:
            imgs = self.driver.find_elements("xpath", "//android.widget.ImageView")
            for img in imgs:
                src = img.get_attribute('content-desc') or img.get_attribute('resource-id') or img.get_attribute('src') or ''
                sources.append(src)
        except Exception:
            pass
        return sources