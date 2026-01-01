# Filename: utils/element_finder.py
# Description: Centralized locator utility implementing a layered fallback strategy with explicit waits, configurable timeouts, and robust error handling. Integrates with Page Object Model and avoids brittle XPaths.

import logging
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)

class ElementFinder:
    """
    Centralized utility for robust element location with layered fallback strategy.
    Priority: accessibility selectors > data-testid > semantic selectors > visible text.
    """

    def __init__(self, driver, timeout=None, poll_frequency=None):
        self.driver = driver
        # Configurable timeout and polling interval with environment variable fallback
        self.timeout = int(timeout or os.environ.get("SELENIUM_WAIT_TIMEOUT", 10))
        self.poll_frequency = float(poll_frequency or os.environ.get("SELENIUM_WAIT_POLL", 0.5))

    def find(self, element_name, page_name, locator_dict):
        """
        Attempts to find an element using a prioritized locator dictionary.
        Args:
            element_name (str): Logical name for the element (for diagnostics).
            page_name (str): Page/component context.
            locator_dict (dict): Ordered mapping of locator strategies.
                Example:
                {
                    'accessibility': (By.CSS_SELECTOR, "[aria-label='Install HP Smart App']"),
                    'data-testid': (By.CSS_SELECTOR, "[data-testid='install-hp-smart-app']"),
                    'semantic': (By.CSS_SELECTOR, "button.install-hp-smart-app"),
                    'text': (By.XPATH, "//button[normalize-space()='Install HP Smart App']")
                }
        Returns:
            WebElement if found, else raises NoSuchElementException.
        """
        current_url = self.driver.current_url
        for strategy, locator in locator_dict.items():
            if not locator:
                continue
            try:
                logger.info(f"Trying {strategy} locator for '{element_name}' on page '{page_name}' ({current_url}): {locator}")
                wait = WebDriverWait(self.driver, self.timeout, self.poll_frequency)
                element = wait.until(EC.presence_of_element_located(locator))
                logger.info(f"Located '{element_name}' using {strategy} strategy.")
                return element
            except (TimeoutException, NoSuchElementException):
                logger.debug(f"Failed to locate '{element_name}' using {strategy} on '{page_name}' ({current_url}). Trying next fallback.")
                continue
        error_msg = (
            f"ERROR: Could not locate element '{element_name}' on page '{page_name}' ({current_url}) "
            f"using any locator strategy. Locators tried: {locator_dict}"
        )
        logger.error(error_msg)
        raise NoSuchElementException(error_msg)

    def click(self, element_name, page_name, locator_dict):
        """
        Clicks an element found by the fallback strategy, with error handling and logging.
        """
        try:
            element = self.find(element_name, page_name, locator_dict)
            wait = WebDriverWait(self.driver, self.timeout, self.poll_frequency)
            wait.until(EC.element_to_be_clickable(locator_dict[next(iter(locator_dict))]))
            element.click()
            logger.info(f"Clicked '{element_name}' on page '{page_name}' ({self.driver.current_url})")
        except Exception as e:
            error_msg = (
                f"ERROR: Failed to click '{element_name}' on page '{page_name}' ({self.driver.current_url}). "
                f"Action: click. Exception: {str(e)}"
            )
            logger.error(error_msg)
            raise

    def assert_visible(self, element_name, page_name, locator_dict):
        """
        Asserts that an element is visible, with diagnostics.
        """
        try:
            element = self.find(element_name, page_name, locator_dict)
            wait = WebDriverWait(self.driver, self.timeout, self.poll_frequency)
            wait.until(EC.visibility_of(element))
            logger.info(f"Verified visibility of '{element_name}' on page '{page_name}' ({self.driver.current_url})")
            assert element.is_displayed(), f"Element '{element_name}' not visible on '{page_name}'"
        except Exception as e:
            error_msg = (
                f"ERROR: Visibility assertion failed for '{element_name}' on '{page_name}' ({self.driver.current_url}). "
                f"Action: assert_visible. Exception: {str(e)}"
            )
            logger.error(error_msg)
            raise

# Usage in Page Objects:
# from utils.element_finder import ElementFinder
# self.element_finder = ElementFinder(self.driver)
