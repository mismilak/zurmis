"""ورودی Passenger برای هاست‌های cPanel / DirectAdmin (Setup Python App).

در تنظیمات «Setup Python App» مقدار Application startup file را روی
passenger_wsgi.py و Application Entry point را روی application بگذارید.
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
