from appium.webdriver.common.appiumby import AppiumBy


class BasePage:
    def __init__(self, driver):
        self.driver = driver


    def find(self, by, value, timeout=10):
        return self.driver.find_element(by, value)

    def click(self, by, value):
        el = self.find(by, value)
        el.click()

    def send_keys(self, by, value, text):
        el = self.find(by, value)
        el.clear()
        el.send_keys(text)

    def drag_and_drop(self, source_el, target_el, duration=800):
        """Drag element `source_el` and drop it onto `target_el`.

        Uses Appium mobile: dragGesture command via execute_script.
        Both args can be WebElement objects or tuples (by, value).
        """
        import time

        # Resolve if selectors were passed
        if isinstance(source_el, tuple) and len(source_el) >= 2:
            source_el = self.find(source_el[0], source_el[1])
        if isinstance(target_el, tuple) and len(target_el) >= 2:
            target_el = self.find(target_el[0], target_el[1])

        # Get element locations
        s_loc = source_el.location
        t_loc = target_el.location

        # Use mobile: dragGesture (Appium 2.0+)
        try:
            self.driver.execute_script('mobile: dragGesture', {
                'startX': int(s_loc['x']),
                'startY': int(s_loc['y']),
                'endX': int(t_loc['x']),
                'endY': int(t_loc['y']),
                'duration': duration
            })
            time.sleep(0.5)
        except Exception as e:
            print(f"Drag gesture failed: {e}")

    def find_with_scroll(self, by, value, max_swipes=6, direction='up', swipe_duration=600):
        """Try to find an element; if not present, perform swipes to bring it into view.

        Returns the WebElement if found, otherwise raises NoSuchElementException.
        """
        import time
        from selenium.common.exceptions import NoSuchElementException

        # Try immediate find first
        try:
            el = self.driver.find_element(by, value)
            return el
        except Exception:
            pass

        # Otherwise attempt swiping to reveal the element
        size = self.driver.get_window_size()
        width = size['width']
        height = size['height']

        for i in range(max_swipes):
            # perform swipe depending on direction
            try:
                if direction == 'up':
                    start_x = width // 2
                    start_y = int(height * 0.7)
                    end_x = start_x
                    end_y = int(height * 0.25)
                elif direction == 'down':
                    start_x = width // 2
                    start_y = int(height * 0.3)
                    end_x = start_x
                    end_y = int(height * 0.8)
                else:
                    # default to up
                    start_x = width // 2
                    start_y = int(height * 0.7)
                    end_x = start_x
                    end_y = int(height * 0.25)

                try:
                    # Try legacy swipe
                    self.driver.swipe(start_x, start_y, end_x, end_y, swipe_duration)
                except Exception:
                    # Fallback to mobile: swipe (some Appium servers)
                    try:
                        self.driver.execute_script('mobile: swipe', {'direction': 'up'})
                    except Exception:
                        # Last resort: W3C actions could be used, but skip for brevity
                        pass

                time.sleep(0.6)

                # try finding after swipe
                els = self.driver.find_elements(by, value)
                if els:
                    return els[0]
            except Exception:
                # ignore and continue swiping
                continue

        # After swipes, try one last time
        try:
            el = self.driver.find_element(by, value)
            return el
        except Exception as e:
            raise NoSuchElementException(f"Could not find element ({by}, {value}) after {max_swipes} swipes: {e}")