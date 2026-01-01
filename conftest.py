# Filename: conftest.py
# Description: Ensures environment variables are loaded for secure config management and provides logging setup.

import os
import logging

def pytest_configure(config):
    # Set up logging for diagnostics
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s %(message)s"
    )
