# Filename: config/config_provider.py
# Description: Secure configuration provider abstraction. Loads environment-specific data from environment variables with backward compatibility.

import os

class ConfigProvider:
    """
    Loads configuration from environment variables.
    Fallbacks to defaults for backward compatibility.
    """
    def __init__(self):
        self.env = os.environ.get("TEST_ENV", "PIE").upper()
        self.base_urls = {
            "PIE": os.environ.get("BASE_URL_PIE", "https://smb.pie.portalshell.int.hp.com"),
            "STAGE": os.environ.get("BASE_URL_STAGE", "https://smb.stage.portalshell.int.hp.com")
        }
        self.credentials = {
            "PIE": {
                "username": os.environ.get("PIE_USERNAME", ""),
                "password": os.environ.get("PIE_PASSWORD", "")
            },
            "STAGE": {
                "username": os.environ.get("STAGE_USERNAME", ""),
                "password": os.environ.get("STAGE_PASSWORD", "")
            }
        }

    def get_base_url(self):
        return self.base_urls.get(self.env, self.base_urls["PIE"])

    def get_credentials(self):
        return self.credentials.get(self.env, self.credentials["PIE"])

# Usage:
# from config.config_provider import ConfigProvider
# config = ConfigProvider()
# driver.get(config.get_base_url())
# username, password = config.get_credentials().values()
