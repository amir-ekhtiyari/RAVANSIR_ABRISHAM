"""gunicorn settings for the Docker image (override with env vars)."""
import multiprocessing
import os

bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
workers = int(os.environ.get('GUNICORN_WORKERS', min(4, multiprocessing.cpu_count() * 2 + 1)))
threads = int(os.environ.get('GUNICORN_THREADS', '2'))
worker_class = 'gthread'
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '60'))
graceful_timeout = 30
keepalive = 5
max_requests = 1000          # recycle workers now and then to keep memory flat
max_requests_jitter = 100
worker_tmp_dir = '/dev/shm'
forwarded_allow_ips = '*'    # only the reverse proxy can reach this port (internal Docker network)
accesslog = '-'
errorlog = '-'
loglevel = os.environ.get('GUNICORN_LOGLEVEL', 'info')
access_log_format = '%({x-real-ip}i)s "%(r)s" %(s)s %(b)s %(M)sms "%(a)s"'
