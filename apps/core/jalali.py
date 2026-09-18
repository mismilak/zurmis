"""تبدیل تاریخ میلادی به شمسی (بدون وابستگی خارجی)."""
import datetime

MONTH_NAMES = [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند",
]
WEEKDAY_NAMES = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "یکشنبه"]
PERSIAN_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def gregorian_to_jalali(gy: int, gm: int, gd: int):
    """تبدیل تاریخ میلادی به (سال، ماه، روز) شمسی."""
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    gy2 = gy - 1600
    gm2 = gm - 1
    gd2 = gd - 1

    g_day_no = 365 * gy2 + (gy2 + 3) // 4 - (gy2 + 99) // 100 + (gy2 + 399) // 400
    g_day_no += g_d_m[gm2] + gd2
    if gm > 2 and ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
        g_day_no += 1
    g_day_no -= 79

    j_np = g_day_no // 12053
    g_day_no %= 12053
    jy = 979 + 33 * j_np + 4 * (g_day_no // 1461)
    g_day_no %= 1461

    if g_day_no >= 366:
        jy += (g_day_no - 1) // 365
        g_day_no = (g_day_no - 1) % 365

    for i in range(11):
        month_len = 31 if i < 6 else 30
        if g_day_no < month_len:
            return jy, i + 1, g_day_no + 1
        g_day_no -= month_len
    return jy, 12, g_day_no + 1


def to_jalali_string(value, fmt="long", digits=True):
    """رشته تاریخ شمسی برای یک date/datetime."""
    if value is None:
        return ""
    if isinstance(value, datetime.datetime):
        value = datetime.date(value.year, value.month, value.day)
    if not isinstance(value, datetime.date):
        return str(value)

    jy, jm, jd = gregorian_to_jalali(value.year, value.month, value.day)
    if fmt == "numeric":
        result = f"{jy}/{jm:02d}/{jd:02d}"
    elif fmt == "short":
        result = f"{jd} {MONTH_NAMES[jm - 1]}"
    elif fmt == "weekday":
        result = f"{WEEKDAY_NAMES[value.weekday()]} {jd} {MONTH_NAMES[jm - 1]} {jy}"
    else:
        result = f"{jd} {MONTH_NAMES[jm - 1]} {jy}"
    return result.translate(PERSIAN_DIGITS) if digits else result


def to_persian_digits(value) -> str:
    return str(value).translate(PERSIAN_DIGITS)
