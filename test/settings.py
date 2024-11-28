from typing import List, Dict, Any

import os

from django.core.management.utils import get_random_secret_key

BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY: str = get_random_secret_key()

DEBUG: bool = True

INSTALLED_APPS: List[str] = [
    "django.contrib.contenttypes",
    "payme",
    "test",
    "pytest_django",
]

DATABASES: Dict[str, Dict[str, Any]] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        "TEST": {
            "NAME": os.path.join(BASE_DIR, "test_db.sqlite3"),  # Configure test database
        },
    }
}

PAYME_ACCOUNT_MODEL: str = "test.models.Order"

DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"