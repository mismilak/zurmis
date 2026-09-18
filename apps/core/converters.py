"""کانورتر URL برای پشتیبانی از اسلاگ‌های فارسی."""


class UnicodeSlugConverter:
    """مانند slug اما حروف فارسی/عربی را هم می‌پذیرد."""

    regex = r"[^/]+"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
