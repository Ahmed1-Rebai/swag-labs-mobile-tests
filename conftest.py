import pytest
import os
import base64
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config import BASE_CAPS, AVD_CONFIGS, APPIUM_SERVER
from datetime import datetime


# --- Paramètre CLI pour choisir l'AVD ---
def pytest_addoption(parser):
    """Ajoute l'option --avd pour choisir l'émulateur cible"""
    parser.addoption(
        "--avd",
        action="store",
        default=None,
        help="Target AVD (emulator ID, e.g., emulator-5556, emulator-5554)"
    )


@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture Appium Driver avec support multi-AVD
    
    Usage:
    - Sans paramètre: pytest tests/test_responsive.py  (utilise le 1er AVD)
    - Avec AVD spécifique: pytest tests/test_responsive.py --avd emulator-5556
    """
    # Récupérer l'AVD cible depuis les options CLI
    avd_id = request.config.getoption("--avd")
    
    # Construire les capabilities
    caps = {**BASE_CAPS}
    
    if avd_id and avd_id in AVD_CONFIGS:
        # Cibler un AVD spécifique
        caps.update(AVD_CONFIGS[avd_id])
        print(f"\n🎯 Targeting AVD: {avd_id} ({AVD_CONFIGS[avd_id]['deviceName']})")
    else:
        # Utiliser le device name générique (Appium choisira le premier)
        if not avd_id:
            print(f"\n📱 Using default device (first available). Use --avd <emulator-id> to target specific AVD")
    
    # Création des options Appium
    options = UiAutomator2Options()
    options.platform_name = caps["platformName"]
    options.automation_name = caps["automationName"]
    
    if "deviceName" in caps:
        options.device_name = caps["deviceName"]
    if "udid" in caps:
        options.udid = caps["udid"]
    
    options.app = caps["app"]
    options.app_package = caps["appPackage"]
    options.app_activity = caps["appActivity"]
    options.new_command_timeout = caps.get("newCommandTimeout", 300)

    driver = webdriver.Remote(APPIUM_SERVER, options=options)
    
    # Store the used config for metadata
    request.config._used_caps = caps
    
    yield driver
    driver.quit()


# --- pytest-html integrations: screenshots and metadata ---
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Add useful metadata to the HTML report and ensure reports folder exists."""
    try:
        # Add app / device metadata from config caps
        config._metadata = getattr(config, '_metadata', {})
        config._metadata['App Package'] = BASE_CAPS.get('appPackage', 'unknown')
        config._metadata['App Activity'] = BASE_CAPS.get('appActivity', 'unknown')
        config._metadata['Platform'] = BASE_CAPS.get('platformName', 'Android')
        config._metadata['AVD Target'] = config.getoption("--avd") or "Auto (first available)"
    except Exception:
        pass

    # Ensure reports/screenshots directory exists
    try:
        reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
        screenshots_dir = os.path.join(reports_dir, 'screenshots')
        os.makedirs(screenshots_dir, exist_ok=True)
    except Exception:
        pass


def pytest_html_report_title(report):
    report.title = "Rapport de tests – Swag Labs Mobile"
    

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure and attach to pytest-html report.

    Saves files under `reports/screenshots/<testname>_<when>_<timestamp>.png`
    and embeds the image in the HTML report for easy inspection.
    """
    outcome = yield
    report = outcome.get_result()

    # Only act for the actual test call or setup phase when it fails
    if report.when not in ("call", "setup"):
        return

    # Consider failures (including xfail that was expected)
    if not (report.failed or (report.skipped and getattr(report, 'wasxfail', False))):
        return

    driver = None
    try:
        driver = item.funcargs.get('driver')
    except Exception:
        driver = None

    if not driver:
        return

    try:
        # Get screenshot as base64
        screenshot_base64 = driver.get_screenshot_as_base64()

        # Save organized file for archive
        reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
        screenshots_dir = os.path.join(reports_dir, 'screenshots')
        os.makedirs(screenshots_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_test_name = item.name.replace('/', '_').replace(' ', '_')
        filename = f"{safe_test_name}_{report.when}_{timestamp}.png"
        fpath = os.path.join(screenshots_dir, filename)
        with open(fpath, 'wb') as fh:
            fh.write(base64.b64decode(screenshot_base64))

        # Attach to html report (inline image)
        extra = getattr(report, 'extra', [])
        try:
            from pytest_html import extras
            # Try adding image as base64 string first (most compatible)
            try:
                extra.append(extras.image(screenshot_base64, mime_type='image/png'))
            except Exception:
                # Fallback: create an HTML img tag with data URI
                try:
                    img_tag = f'<img src="data:image/png;base64,{screenshot_base64}" alt="screenshot" style="max-width:100%; height:auto;"/>'
                    extra.append(extras.html(img_tag))
                except Exception:
                    # Last-resort: attach raw bytes (older/newer pytest-html sometimes accepts bytes)
                    try:
                        img_bytes = base64.b64decode(screenshot_base64)
                        extra.append(extras.image(img_bytes, mime_type='image/png'))
                    except Exception:
                        pass

            # also add a file link for easy download from report directory
            relpath = os.path.relpath(fpath, os.path.abspath(os.getcwd()))
            relpath = relpath.replace('\\', '/')
            extra.append(extras.url(relpath, name='Saved screenshot'))
        except Exception:
            pass
        report.extra = extra
    except Exception:
        # don't let screenshot capture break the test flow
        return

