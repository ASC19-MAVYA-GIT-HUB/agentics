# Filename: pages/dashboard_page.py
# Description: Dashboard Page Object using centralized ElementFinder utility for robust locator strategy.

from selenium.webdriver.common.by import By
from utils.element_finder import ElementFinder

class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.ef = ElementFinder(driver)

    def wait_for_welcome_banner(self):
        self.ef.assert_visible(
            "Welcome Banner",
            "Dashboard",
            {
                "accessibility": (By.CSS_SELECTOR, "[aria-label='Welcome Banner']"),
                "data-testid": (By.CSS_SELECTOR, "[data-testid='welcome-banner']"),
                "semantic": (By.CSS_SELECTOR, "div.welcome-banner"),
                "text": None  # Avoid XPaths unless absolutely necessary
            }
        )

    def click_install_hp_smart_app(self):
        self.ef.click(
            "Install HP Smart App Button",
            "Dashboard",
            {
                "accessibility": (By.CSS_SELECTOR, "[aria-label='Install HP Smart App']"),
                "data-testid": (By.CSS_SELECTOR, "[data-testid='install-hp-smart-app']"),
                "semantic": (By.CSS_SELECTOR, "button.install-hp-smart-app"),
                "text": (By.XPATH, "//button[normalize-space()='Install HP Smart App']")
            }
        )

    def click_download_now_link(self):
        self.ef.click(
            "Download Now Link",
            "Dashboard",
            {
                "accessibility": (By.CSS_SELECTOR, "[aria-label='Download now']"),
                "data-testid": (By.CSS_SELECTOR, "[data-testid='download-now']"),
                "semantic": (By.CSS_SELECTOR, "a.download-now"),
                "text": (By.XPATH, "//a[normalize-space()='Download now']")
            }
        )

    def click_learn_more_link(self):
        self.ef.click(
            "Learn More Link",
            "Dashboard",
            {
                "accessibility": (By.CSS_SELECTOR, "[aria-label='Learn more']"),
                "data-testid": (By.CSS_SELECTOR, "[data-testid='learn-more']"),
                "semantic": (By.CSS_SELECTOR, "a.learn-more"),
                "text": (By.XPATH, "//a[normalize-space()='Learn more']")
            }
        )

    # Add similar methods for other critical elements as needed
