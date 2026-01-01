# Filename: tests/test_69694096_dashboard_base_page_links_no_printers.py
# Description: Refactored test to use Page Object Model, centralized locator utility, and secure config management. No hardcoded URLs or credentials.

import pytest
from selenium import webdriver
from config.config_provider import ConfigProvider
from pages.dashboard_page import DashboardPage

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    if os.environ.get("HEADLESS", "1") == "1":
        options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_69694096_dashboard_base_page_links_no_printers(driver):
    config = ConfigProvider()
    dashboard = DashboardPage(driver)

    # Step 1: Navigate to Consolidated Portal and login (login logic abstracted if needed)
    driver.get(config.get_base_url())
    dashboard.wait_for_welcome_banner()

    # Step 2: Click 'Install HP Smart App' button and assert redirect
    dashboard.click_install_hp_smart_app()
    WebDriverWait(driver, 10).until(
        lambda d: "apps.apple.com" in d.current_url or "play.google.com" in d.current_url
    )
    assert "apps.apple.com" in driver.current_url or "play.google.com" in driver.current_url

    # Step 3: Click 'Download now' link and assert redirect
    driver.get(config.get_base_url())
    dashboard.click_download_now_link()
    WebDriverWait(driver, 10).until(
        lambda d: "apps.apple.com" in d.current_url or "play.google.com" in d.current_url
    )
    assert "apps.apple.com" in driver.current_url or "play.google.com" in driver.current_url

    # Step 4: Click 'Learn more' link and assert navigation
    driver.get(config.get_base_url())
    dashboard.click_learn_more_link()
    WebDriverWait(driver, 10).until(
        lambda d: "/sustainability" in d.current_url
    )
    assert "/sustainability" in driver.current_url
