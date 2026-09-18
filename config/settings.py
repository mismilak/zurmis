"""تنظیمات پروژه وب‌سایت وکیل پایه یک دادگستری."""
from pathlib import Path

from config import env

BASE_DIR = Path(__file__).resolve().parent.parent
env.load_env(BASE_DIR / ".env")

SECRET_KEY = env.get("SECRET_KEY", "django-insecure-dev-key-change-me-in-production")
DEBUG = env.get_bool("DEBUG", True)
ALLOWED_HOSTS = env.get_list("ALLOWED_HOSTS", ["*"])
CSRF_TRUSTED_ORIGINS = env.get_list("CSRF_TRUSTED_ORIGINS", [])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
    "apps.core",
    "apps.blog",
    "apps.videos",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DATABASE_URL = env.get("DATABASE_URL", "")
if DATABASE_URL:
    # پشتیبانی ساده از PostgreSQL بدون وابستگی اضافه
    from urllib.parse import urlparse

    url = urlparse(DATABASE_URL)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": url.path.lstrip("/"),
            "USER": url.username or "",
            "PASSWORD": url.password or "",
            "HOST": url.hostname or "",
            "PORT": str(url.port or ""),
            "CONN_MAX_AGE": 60,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "fa-ir"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# اگر whitenoise نصب باشد، فایل‌های استاتیک مستقیماً توسط جنگو سرو می‌شوند
try:  # pragma: no cover
    import whitenoise  # noqa: F401

    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
    }
    WHITENOISE_MAX_AGE = 60 * 60 * 24 * 30
except ImportError:  # pragma: no cover
    pass

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

# --- ایمیل ---
EMAIL_HOST = env.get("EMAIL_HOST", "")
if EMAIL_HOST:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_PORT = env.get_int("EMAIL_PORT", 587)
    EMAIL_HOST_USER = env.get("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = env.get("EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_TLS = env.get_bool("EMAIL_USE_TLS", True)
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = env.get("DEFAULT_FROM_EMAIL", "no-reply@localhost")
NOTIFY_EMAIL = env.get("NOTIFY_EMAIL", "")

# --- امنیت ---
SECURE_SSL_REDIRECT = env.get_bool("SECURE_SSL_REDIRECT", False)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
if not DEBUG:
    SESSION_COOKIE_SECURE = SECURE_SSL_REDIRECT
    CSRF_COOKIE_SECURE = SECURE_SSL_REDIRECT
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

LOGIN_URL = "/admin/login/"

# --- شخصی‌سازی پنل مدیریت ---
ADMIN_SITE_HEADER = "پنل مدیریت وب‌سایت وکالت"
ADMIN_SITE_TITLE = "مدیریت سایت"
ADMIN_INDEX_TITLE = "خوش آمدید"
