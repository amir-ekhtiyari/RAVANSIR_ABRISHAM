# راهنمای انتشار روی سرور با Docker

این پروژه با سه کانتینر اجرا می‌شود:

| سرویس | کار |
|---|---|
| `db` | پایگاه داده PostgreSQL 16 (داده‌ها در volume دائمی `postgres_data`) |
| `web` | Django + gunicorn (هنگام شروع: صبر برای دیتابیس، migrate، collectstatic) |
| `caddy` | وب‌سرور جلویی: **HTTPS خودکار** با Let's Encrypt، فشرده‌سازی، سرو مستقیم `/static/` و `/media/` |

## راه سریع (سرور تازه‌ی Ubuntu، داخل یا خارج ایران)

```bash
git clone https://github.com/amir-ekhtiyari/RAVANSIR_ABRISHAM.git /opt/ravansir
cd /opt/ravansir && sudo bash scripts/server_setup.sh
```

این اسکریپت swap، Docker (از مخزن خود اوبونتو)، آینه‌های ایرانی Docker و pip، فایروال و فایل `.env` با رمزهای تصادفی را خودش می‌سازد و سایت را بالا می‌آورد. اگر دامنه هنوز به IP سرور وصل نشده باشد، سایت روی `http://IP-سرور` برای تست بالا می‌آید؛ بعد از تنظیم DNS همان دستور دوم را دوباره بزنید تا HTTPS فعال شود. بقیه‌ی این راهنما همان مراحل را دستی توضیح می‌دهد.

## پیش‌نیازها

- یک سرور لینوکس (Ubuntu 22.04/24.04 پیشنهاد می‌شود) با حداقل ۱ گیگ رم و ۱۰ گیگ دیسک.
- Docker و Docker Compose:
  ```bash
  curl -fsSL https://get.docker.com | sh
  ```
- دامنه‌ی `ravanseirabrisham.ir` با این رکوردهای DNS (در پنل ایرنیک/نمایندگی یا هر سرویس DNS که دامنه به آن وصل است):

  | نوع | نام | مقدار |
  |---|---|---|
  | `A` | `@` | IP سرور |
  | `A` | `www` | IP سرور |

  نشانی `www.ravanseirabrisham.ir` خودکار به `ravanseirabrisham.ir` ریدایرکت می‌شود. اگر از CDN ابری (مثل آروان) استفاده می‌کنید، تا گرفتن اولین گواهی HTTPS پروکسی ابری را خاموش بگذارید.
- پورت‌های 80 و 443 سرور باز باشند.

## ۱. کپی پروژه روی سرور

```bash
sudo mkdir -p /opt/ravansir && sudo chown $USER /opt/ravansir
git clone https://github.com/amir-ekhtiyari/RAVANSIR_ABRISHAM.git /opt/ravansir
cd /opt/ravansir
```

## ۲. تنظیم `.env`

```bash
cp .env.example .env
python3 -c "import secrets; print(secrets.token_urlsafe(50))"   # خروجی را در DJANGO_SECRET_KEY بگذارید
nano .env
```

حتماً این‌ها را پر کنید:

| متغیر | نمونه |
|---|---|
| `SITE_ADDRESS` | `ravanseirabrisham.ir, www.ravanseirabrisham.ir` |
| `ACME_EMAIL` | ایمیل شما برای گواهی SSL |
| `DJANGO_SECRET_KEY` | کلید تصادفی بالا |
| `DJANGO_ALLOWED_HOSTS` | `ravanseirabrisham.ir,www.ravanseirabrisham.ir` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://ravanseirabrisham.ir,https://www.ravanseirabrisham.ir` |
| `SITE_URL` | `https://ravanseirabrisham.ir` (برای سئو و کارت QR) |
| `DJANGO_ADMIN_URL` | یک مسیر غیرقابل حدس، مثلاً `rsa-panel-8k2/` |
| `POSTGRES_PASSWORD` | یک رمز قوی جدید |

> اگر بعد از اولین اجرا `POSTGRES_PASSWORD` را عوض کنید، دیتابیس رمز قبلی را نگه می‌دارد. یا رمز را برگردانید یا (فقط وقتی داده‌ای ندارید) `docker compose down -v` بزنید.

> تست اولیه بدون دامنه (با IP سرور): `SITE_ADDRESS=:80`، `DJANGO_HTTPS=0`، و IP سرور را در `DJANGO_ALLOWED_HOSTS` بگذارید. بعد از وصل شدن دامنه این دو را به حالت HTTPS برگردانید.

## ۳. ساخت و اجرا

```bash
docker compose up -d --build
docker compose ps            # هر سه سرویس باید healthy / running باشند
docker compose logs -f web   # دیدن لاگ‌ها (Ctrl+C برای خروج)
```

Caddy در اولین درخواست، گواهی HTTPS را خودکار می‌گیرد و تمدید می‌کند.

### سرور داخل ایران (Docker Hub یا PyPI در دسترس نیست)

در `.env` آینه‌ها را فعال کنید (خطوط `PYTHON_IMAGE`، `POSTGRES_IMAGE`، `CADDY_IMAGE` و `PIP_INDEX_URL` را از حالت توضیح خارج کنید، یا آینه‌ی دیگری که سرورتان به آن دسترسی دارد بنویسید) و دوباره `docker compose up -d --build` بزنید.

## ۴. کاربر مدیر و انتقال اطلاعات

ساخت کاربر مدیر جدید:
```bash
docker compose exec web python manage.py createsuperuser
```

یا انتقال همه‌ی اطلاعات فعلی (اطلاعات شرکت، خدمات، مسیرها، ناوگان، کاربر مدیر و درخواست‌ها) از فایل `db.sqlite3` کامپیوترتان: فایل را با `scp` به پوشه‌ی پروژه روی سرور بفرستید و:
```bash
sh scripts/import_sqlite.sh db.sqlite3
```

عکس‌هایی که در پنل مدیریت بارگذاری کرده‌اید (پوشه‌ی `media` را هم کنار پروژه روی سرور کپی کنید):
```bash
sh scripts/import_media.sh media
```

پنل مدیریت: `https://دامنه/مسیر-DJANGO_ADMIN_URL/`

## ۵. به‌روزرسانی سایت

```bash
cd /opt/ravansir
git pull
docker compose up -d --build
```
مهاجرت دیتابیس و فایل‌های استاتیک خودکار انجام می‌شوند.

## ۶. پشتیبان‌گیری

```bash
sh scripts/backup.sh                                   # دیتابیس + فایل‌های آپلودی در backups/
sh scripts/restore.sh backups/db-YYYYMMDD-HHMMSS.dump  # بازگردانی
```
پشتیبان خودکار هر شب ساعت ۳ (با `crontab -e`):
```
0 3 * * * cd /opt/ravansir && sh scripts/backup.sh >> backups/cron.log 2>&1
```
نسخه‌ای از پوشه‌ی `backups` را هم گاهی بیرون از سرور نگه دارید.

## دستورهای مفید

| کار | دستور |
|---|---|
| وضعیت سرویس‌ها | `docker compose ps` |
| لاگ‌ها | `docker compose logs -f web caddy` |
| ری‌استارت | `docker compose restart web` |
| توقف همه | `docker compose down` (داده‌ها حذف نمی‌شوند) |
| شل جنگو | `docker compose exec web python manage.py shell` |
| سلامت سایت | `curl -H "Host: دامنه" http://127.0.0.1/healthz` |

## امنیت (پیش‌فرض‌ها)

- `DEBUG=0`، کوکی‌های امن، HSTS، ریدایرکت خودکار به HTTPS.
- کانتینر وب با کاربر غیر root اجرا می‌شود؛ پورت 8000 و دیتابیس فقط در شبکه‌ی داخلی Docker در دسترس‌اند و فقط پورت‌های 80/443 باز هستند.
- فایل `.env` هرگز در گیت یا داخل image قرار نمی‌گیرد.
