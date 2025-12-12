from pages.home_page import HomePage

def TC1_open_app(driver):
    home = HomePage(driver)
    login_button = home.find("accessibility id", "test-LOGIN")
    assert login_button is not None, "Login button is not visible"
