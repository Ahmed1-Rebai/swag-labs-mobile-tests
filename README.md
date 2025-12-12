# Test Automation Project Structure

## Overview
This project contains automated tests for a mobile application using Appium and pytest. The tests are organized by type and functionality to ensure comprehensive coverage.

## Test Organization

### 1. Functionality Tests (tests/functionality/)
These tests verify the core functionality of the application.

- **TestSuite1_Basic.py**: Basic application functionality
  - TC1: test_open_app - App launch and initial state verification

- **TestSuite2_Login.py**: Login functionality tests
  - TC2: test_login_with_accepted_users - User authentication with different user types
  - TC3: test_login_with_empty_fields - Login validation for empty fields
  - TC4: test_login_with_wrong_password - Login validation for wrong password
  - TC5: test_login_with_wrong_username - Login validation for wrong username
  - TC6: test_login_tc03_empty_password - Boundary testing for empty password
  - TC7: test_login_tc04_empty_username - Boundary testing for empty username
  - TC8: test_login_tc07_fields_exceeding_limit - Boundary testing for oversized fields

- **TestSuite3_Navigation.py**: Navigation and state management
  - TC9: test_nav01_open_side_menu - Opening side menu (hamburger)
  - TC10: test_nav02_navigate_to_sections - Navigation to different sections
  - TC11: test_nav03_android_back_button - Android back button functionality
  - TC12: test_nav04_portrait_landscape_rotation - Orientation changes
  - TC13: test_nav05_app_restart_session_state - App restart and session state

- **TestSuite4_Products.py**: Product page functionality
  - TC14: test_products_page_displayed - Products page display verification
  - TC15: test_products_list_not_empty - Products list validation
  - TC16: test_add_to_cart_buttons_available - Add to cart buttons availability
  - TC17: test_add_product_to_cart - Add product to cart functionality
  - TC18: test_remove_product_from_cart - Remove product from cart
  - TC19: test_add_multiple_products_to_cart - Multiple products addition
  - TC20: test_drag_product_to_cart - Drag and drop to cart
  - TC21: test_cart_navigation - Cart page navigation
  - TC22: test_menu_navigation - Menu navigation
  - TC23: test_product_details_navigation - Product details navigation
  - TC24: test_logout_functionality - Logout functionality
  - TC25: test_toggle_sort_menu - Sort menu functionality
  - TC26: test_scroll_products_list - Products list scrolling

- **TestSuite5_Checkout.py**: Checkout and purchase flow
  - TC27: test_sort_products_by_price_low_to_high - Price sorting (low to high)
  - TC28: test_sort_products_by_name_z_to_a - Name sorting (Z to A)
  - TC29: test_sort_products_by_name_a_to_z - Name sorting (A to Z)
  - TC30: test_sort_products_by_price_high_to_low - Price sorting (high to low)
  - TC31: test_cancel_sort_modal - Cancel sort modal
  - TC32: test_empty_cart - Empty cart functionality
  - TC33: test_checkout_without_products - Checkout validation
  - TC34: test_successful_end_to_end_purchase - Complete purchase flow
  - TC35: test_purchase_process_cancellation - Purchase cancellation
  - TC36: test_checkout_info_validation_missing_fields - Form validation
  - TC37: test_visual_glitch_with_problem_user - Visual testing with problem user

### 2. Responsive Tests (tests/responsive/)
Tests for different screen sizes and device compatibility.

- **TestSuite6_Responsive.py**: Multi-device responsive testing
  - TC38: test_resp01_login_display_small_phone - Login on small phone (4.7")
  - TC39: test_resp02_products_visibility_medium_phone - Products on medium phone (6.4")
  - TC40: test_resp03_buttons_clickable_large_tablet - Buttons on large tablet (10")
  - TC41: test_resp_summary - Responsive test summary

### 3. Performance Tests (tests/performance/)
Performance and response time validation.

- **TestSuite7_Performance.py**: Performance metrics
  - TC42: test_performance_products_page_load_time - Products page load time
  - TC43: test_performance_full_checkout_process - End to end purchase load time

### 4. Stress Tests (tests/stress/)
Stability testing under load and repeated operations.

- **TestSuite8_Stress.py**: Stress and load testing
  - TC44: test_stress_add_remove_product_cycles - Add/remove cycles (20 iterations)
  - TC45: test_stress_login_logout_cycles - Login/logout cycles (20 iterations)
  - TC46: test_load_scroll_products_list_to_bottom - Rapid scrolling load test

## Test Execution

### Running All Tests
```bash
pytest
```

### Running by Category
```bash
# Functionality tests
pytest tests/functionality/

# Responsive tests
pytest tests/responsive/ -m responsive

# Performance tests
pytest tests/performance/ -m performance

# Stress tests
pytest tests/stress/ -m stress
```

### Running Specific Test Cases
```bash
# Run specific test case
pytest tests/functionality/TestSuite1_Login.py::TC1_login_with_accepted_users

# Run with HTML report
pytest --html=reports/test_report.html
```

## Test Configuration

### pytest.ini
- HTML reporting enabled
- Test markers defined for categorization
- Quiet output for clean reports

### conftest.py
- Shared fixtures for driver setup
- Test data and configuration

## Project Structure
```
tests/
├── functionality/
│   ├── TestSuite1_Login.py
│   ├── TestSuite2_Basic.py
│   ├── TestSuite3_Navigation.py
│   ├── TestSuite4_Products.py
│   └── TestSuite5_Checkout.py
├── responsive/
│   └── TestSuite6_Responsive.py
├── performance/
│   └── TestSuite7_Performance.py
├── stress/
│   └── TestSuite8_Stress.py
├── __pycache__/
├── conftest.py
└── pytest.ini

pages/
├── base_page.py
├── home_page.py
├── login_page.py
└── checkout_page.py

reports/
├── test_report.html
└── screenshots/

config.py
requirements.txt
RAPPORT_STRUCTURE.md
```

## Test Coverage Summary

- **Functionality**: 5 test cases covering login, navigation, products, and checkout
- **Responsive**: 1 test case covering 3 device sizes
- **Performance**: 1 test case with load time measurements
- **Stress**: 1 test case with repeated operations testing

Total: 8 test cases providing comprehensive coverage of the application.