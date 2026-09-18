# وب‌سایت وکیل پایه یک دادگستری

وب‌سایت کامل و آمادهٔ انتشار برای وکیل پایه یک دادگستری (کانون وکلا) — با بک‌اند **جنگو**،
طراحی **راست‌به‌چپ و موبایل‌محور**، ناوبار شناور شیشه‌ای پایین صفحه (مشابه تلگرام)،
انیمیشن‌های ورود، بخش مقالات، ویدیوهای آپارات و فرم درخواست مشاوره.

---

## فهرست بخش‌های سایت

| بخش | توضیح |
|---|---|
| معرفی (Hero) | تیتر اصلی، شماره پروانه، دکمه مشاوره و تماس |
| آمار و دستاوردها | شمارنده متحرک سال سابقه، پرونده‌ها و … |
| درباره وکیل | معرفی کامل + تب‌های سوابق شغلی، تحصیلات و افتخارات |
| زمینه‌های تخصصی | خدمات حقوقی (حقوقی، کیفری، خانواده، ملکی، تجاری، قراردادها، ارث، دیوان عدالت اداری) با صفحه اختصاصی |
| مراحل همکاری | فرآیند چهارمرحله‌ای از ثبت درخواست تا اجرای حکم |
| ویدیوها | نمایش ویدیوهای آپارات (فقط لینک را وارد کنید) + صفحه اختصاصی هر ویدیو |
| مقالات | وبلاگ کامل با دسته‌بندی، برچسب، جست‌وجو، دیدگاه و صفحه‌بندی |
| نظرات موکلان | اسلایدر نظرات با امتیاز ستاره |
| پرسش‌های متداول | آکاردئون + صفحه مستقل |
| تماس و مشاوره | فرم درخواست مشاوره (AJAX)، اطلاعات تماس، نقشه، واتساپ/تلگرام/ایتا |
| صفحات ثابت | درباره دفتر، قوانین، حریم خصوصی (قابل مدیریت از پنل) |
| سئو | sitemap.xml، robots.txt، Open Graph، داده ساختاریافته Attorney/Article |

**ویژگی‌های موبایل:** ناوبار شناور پایین با بک‌گراند شیشه‌ای (blur) که با اسکرول به پایین مخفی و با
اسکرول به بالا ظاهر می‌شود، رعایت `safe-area` آیفون، دکمه شناور بازگشت به بالا و چیدمان تک‌ستونی.

---

## پیش‌نیازها

- پایتون ۳.۱۰ یا بالاتر
- فقط دو پکیج الزامی: `Django` و `Pillow`
  (پکیج‌های `whitenoise` و `gunicorn` توصیه‌شده ولی اختیاری‌اند)

---

## راه‌اندازی روی سیستم خودتان

```bash
python3 -m venv .venv
source .venv/bin/activate          # ویندوز: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # سپس مقادیر را ویرایش کنید

python manage.py migrate
python manage.py seed_demo         # داده‌های نمونه فارسی (اختیاری ولی توصیه‌شده)
python manage.py createsuperuser   # ساخت کاربر مدیر
python manage.py runserver
```

- سایت: <http://127.0.0.1:8000>
- پنل مدیریت: <http://127.0.0.1:8000/admin>

> `seed_demo` سایت را با محتوای نمونه (خدمات، مقالات، ویدیوها، نظرات و پرسش‌ها) پر می‌کند تا از همان
> ابتدا سایت «بالا بیاید». برای پاک کردن داده‌های نمونه و ساخت مجدد: `python manage.py seed_demo --fresh`

---

## کار با پنل مدیریت (ترتیب پیشنهادی)

۱. **تنظیمات سایت** — نام وکیل، شماره پروانه، کانون، عکس، شماره تماس، واتساپ، آدرس، کد نقشه، متن‌های سئو و نماد اعتماد.
۲. **زمینه‌های تخصصی و خدمات** — هر خدمت یک صفحه اختصاصی و آیکون دارد.
   آیکون‌های موجود: `scale, gavel, family, home, briefcase, contract, shield, bank, doc, check, phone, clock, star, users, message, video, book, map, mail, award`
۳. **سوابق و افتخارات / آمار / مراحل همکاری** — محتوای بخش «درباره وکیل».
۴. **مقالات** — نوشتن مطلب (متن با HTML)، دسته‌بندی، برچسب و تصویر شاخص.
۵. **ویدیوها** — فقط لینک آپارات را جای‌گذاری کنید؛ کد ویدیو خودکار استخراج و پخش‌کننده امبد می‌شود.
۶. **درخواست‌های مشاوره** — پیام‌های ثبت‌شده از فرم سایت با وضعیت (جدید / در حال پیگیری / انجام شد).
۷. **دیدگاه‌ها** — دیدگاه‌های مقالات پس از تایید شما نمایش داده می‌شوند.

### افزودن ویدیوی آپارات

در بخش «ویدیوها» → افزودن ویدیو → در فیلد «لینک ویدیو در آپارات» یکی از این‌ها را وارد کنید:

```
https://www.aparat.com/v/abc123
https://www.aparat.com/video/video/embed/videohash/abc123/vt/frame
abc123
```

سیستم خودش کد ویدیو را استخراج و پخش‌کننده را در سایت نمایش می‌دهد.
برای تصویر بندانگشتی بهتر، فایل کاور را هم آپلود کنید.

---

## انتشار روی هاست

### گزینه ۱: هاست اشتراکی cPanel / DirectAdmin (Setup Python App)

۱. فایل‌های پروژه را در مسیر مثلاً `/home/USER/lawyer-site` آپلود کنید (پوشه‌های `.venv` و `media` را آپلود نکنید).
۲. در cPanel وارد **Setup Python App** شوید و یک اپ بسازید:
   - Python version: ۳.۱۰ یا بالاتر
   - Application root: `lawyer-site`
   - Application URL: دامنه یا ساب‌دامنه شما
   - Application startup file: `passenger_wsgi.py`
   - Application Entry point: `application`
۳. در همان صفحه، دستور «Enter to the virtual environment» را کپی و در ترمینال اجرا کنید، سپس:

```bash
pip install -r requirements.txt
cp .env.example .env      # و مقادیر را ویرایش کنید (DEBUG=False و ALLOWED_HOSTS دامنه شما)
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py seed_demo      # اختیاری
```

۴. در تنظیمات اپ، روی **Restart** بزنید.
۵. اگر فایل‌های استاتیک نمایش داده نشد: مطمئن شوید `whitenoise` نصب است (در این پروژه به‌صورت خودکار
   فعال می‌شود) یا در فایل `.htaccess` مسیر `/static` را به پوشه `staticfiles` و `/media` را به پوشه `media` بدهید.

### گزینه ۲: سرور مجازی (Ubuntu + Gunicorn + Nginx)

```bash
sudo apt update && sudo apt install -y python3-venv nginx
sudo mkdir -p /var/www/lawyer-site && cd /var/www/lawyer-site
# آپلود یا clone پروژه در این مسیر
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env && nano .env
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

sudo cp deploy/gunicorn.service /etc/systemd/system/lawyer-site.service
sudo systemctl daemon-reload && sudo systemctl enable --now lawyer-site

sudo cp deploy/nginx.conf /etc/nginx/sites-available/lawyer-site
sudo ln -s /etc/nginx/sites-available/lawyer-site /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# گواهی SSL رایگان
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com
```

سپس در `.env` مقدار `SECURE_SSL_REDIRECT=True` را فعال کنید و سرویس را ری‌استارت کنید.

### گزینه ۳: داکر

```bash
cp .env.example .env
docker compose up -d --build
```

---

## تنظیمات مهم `.env`

| متغیر | توضیح |
|---|---|
| `SECRET_KEY` | یک رشته تصادفی طولانی (حتماً عوض شود) |
| `DEBUG` | روی هاست حتماً `False` |
| `ALLOWED_HOSTS` | دامنه‌ها با کاما: `example.com,www.example.com` |
| `CSRF_TRUSTED_ORIGINS` | با `https://` مثال: `https://example.com` |
| `DATABASE_URL` | خالی = SQLite. برای PostgreSQL: `postgres://user:pass@host:5432/db` |
| `EMAIL_HOST` و … | در صورت تنظیم، هر درخواست مشاوره به `NOTIFY_EMAIL` ایمیل می‌شود |
| `SECURE_SSL_REDIRECT` | پس از نصب SSL روی `True` |

ساخت کلید امن:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

## ساختار پروژه

```
config/            تنظیمات جنگو، مسیرها، WSGI/ASGI و خواننده .env
apps/core/         تنظیمات سایت، خدمات، سوابق، آمار، نظرات، پرسش‌ها، فرم مشاوره، صفحات ثابت
apps/blog/         مقالات، دسته‌بندی، برچسب و دیدگاه‌ها
apps/videos/       ویدیوهای آپارات
templates/         قالب‌های HTML (پایه، صفحه نخست، وبلاگ، ویدیو، خطاها)
static/css|js|img  استایل، اسکریپت و آیکون
static/fonts/      فونت وزیرمتن (میزبانی محلی، بدون CDN)
media/             فایل‌های آپلودی مدیر (عکس‌ها)
deploy/            نمونه تنظیمات Nginx و systemd
```

## دستورات مفید

```bash
python manage.py test               # اجرای تست‌ها
python manage.py seed_demo --fresh  # بازسازی داده‌های نمونه
python manage.py collectstatic      # جمع‌آوری فایل‌های استاتیک
python manage.py changepassword USER
```

## نکات تکمیلی

- فونت **وزیرمتن** داخل خود پروژه میزبانی می‌شود (`static/fonts/`) و هیچ درخواستی به CDN خارجی زده نمی‌شود؛
  همین فونت روی پنل مدیریت هم اعمال شده است. مجوز فونت: `static/fonts/LICENSE-Vazirmatn.txt`
- تاریخ‌ها به‌صورت **شمسی** و اعداد **فارسی** نمایش داده می‌شوند (بدون نیاز به پکیج اضافه).
- آدرس صفحات از عنوان فارسی ساخته می‌شود (مثلاً `/services/دعاوی-حقوقی/`) که برای سئوی فارسی مناسب است.
- فرم مشاوره دارای فیلد تله ضدربات و اعتبارسنجی شماره موبایل ایرانی است.
- پشتیبان‌گیری: فایل `db.sqlite3` (یا دامپ PostgreSQL) به‌همراه پوشه `media/`.
