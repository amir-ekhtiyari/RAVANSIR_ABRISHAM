#!/usr/bin/env bash
# One-shot setup of a fresh Ubuntu 22.04/24.04 server (works on servers inside Iran).
#   git clone https://github.com/amir-ekhtiyari/RAVANSIR_ABRISHAM.git /opt/ravansir
#   cd /opt/ravansir && sudo bash scripts/server_setup.sh
# Safe to run again: it keeps an existing .env and only switches to HTTPS once the domain points here.
set -euo pipefail

DOMAIN="${DOMAIN:-ravanseirabrisham.ir}"
APP_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$APP_DIR"

say() { printf '\n\033[1;34m==> %s\033[0m\n' "$*"; }
[ "$(id -u)" -eq 0 ] || { echo "Run as root: sudo bash scripts/server_setup.sh"; exit 1; }

# 1) Swap (the image build needs memory on 1-2 GB servers)
if ! swapon --show | grep -q . ; then
  say "Creating 2 GB swap"
  fallocate -l 2G /swapfile || dd if=/dev/zero of=/swapfile bs=1M count=2048
  chmod 600 /swapfile && mkswap /swapfile >/dev/null && swapon /swapfile
  grep -q '^/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
fi

# 2) Docker from Ubuntu's own repository (download.docker.com is not reachable from Iran)
if ! docker compose version >/dev/null 2>&1; then
  say "Installing Docker"
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -y
  apt-get install -y docker.io git curl ufw dnsutils
  apt-get install -y docker-compose-v2 || apt-get install -y docker-compose-plugin
  systemctl enable --now docker
fi

# 3) Docker Hub mirror for pulls that are not covered by the image settings in .env
if [ ! -f /etc/docker/daemon.json ]; then
  say "Configuring Docker registry mirror"
  printf '{\n  "registry-mirrors": ["https://docker.arvancloud.ir"]\n}\n' > /etc/docker/daemon.json
  systemctl restart docker
fi

# 4) Firewall: SSH, HTTP, HTTPS only
say "Firewall"
ufw allow OpenSSH >/dev/null; ufw allow 80/tcp >/dev/null; ufw allow 443/tcp >/dev/null; ufw allow 443/udp >/dev/null
ufw --force enable >/dev/null

# 5) .env (created once, with fresh secrets)
SERVER_IP="$(curl -4fsS --max-time 8 https://api.ipify.org 2>/dev/null || hostname -I | awk '{print $1}')"
if [ ! -f .env ]; then
  say "Creating .env"
  rand() { tr -dc 'A-Za-z0-9' </dev/urandom | head -c "$1"; }
  cp .env.example .env
  sed -i "s|^DJANGO_SECRET_KEY=.*|DJANGO_SECRET_KEY=$(rand 60)|" .env
  sed -i "s|^POSTGRES_PASSWORD=.*|POSTGRES_PASSWORD=$(rand 32)|" .env
  sed -i "s|^DJANGO_ADMIN_URL=.*|DJANGO_ADMIN_URL=panel-$(rand 8 | tr 'A-Z' 'a-z')/|" .env
  # Iranian mirrors for images and pip
  sed -i -E 's|^# (PYTHON_IMAGE=.*)|\1|; s|^# (POSTGRES_IMAGE=.*)|\1|; s|^# (CADDY_IMAGE=.*)|\1|; s|^# (PIP_INDEX_URL=.*)|\1|' .env
  sed -i -E 's|^# (GUNICORN_WORKERS=).*|\12|' .env
fi

# 6) HTTPS only when the domain already points to this server; otherwise serve plain http://IP for testing
DNS_IP="$(dig +short A "$DOMAIN" @8.8.8.8 2>/dev/null | tail -1 || true)"
if [ -n "$SERVER_IP" ] && [ "$DNS_IP" = "$SERVER_IP" ]; then
  say "$DOMAIN points to $SERVER_IP -> HTTPS mode"
  sed -i "s|^SITE_ADDRESS=.*|SITE_ADDRESS=$DOMAIN, www.$DOMAIN|" .env
  sed -i "s|^DJANGO_HTTPS=.*|DJANGO_HTTPS=1|" .env
  sed -i "s|^DJANGO_ALLOWED_HOSTS=.*|DJANGO_ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN|" .env
  MODE=https
else
  say "$DOMAIN does not point here yet (DNS: ${DNS_IP:-none}, server: $SERVER_IP) -> test mode on http://$SERVER_IP"
  sed -i "s|^SITE_ADDRESS=.*|SITE_ADDRESS=:80|" .env
  sed -i "s|^DJANGO_HTTPS=.*|DJANGO_HTTPS=0|" .env
  sed -i "s|^DJANGO_ALLOWED_HOSTS=.*|DJANGO_ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN,$SERVER_IP|" .env
  MODE=http
fi

# 7) Build and start
say "Building and starting (first run takes a few minutes)"
docker compose up -d --build

say "Waiting for the site"
for _ in $(seq 1 60); do
  if curl -fsS -o /dev/null -H "Host: $DOMAIN" http://127.0.0.1/healthz 2>/dev/null \
     || curl -fsS -o /dev/null http://127.0.0.1/healthz 2>/dev/null \
     || curl -fsSk -o /dev/null --resolve "$DOMAIN:443:127.0.0.1" "https://$DOMAIN/healthz" 2>/dev/null; then
    OK=1; break; fi
  sleep 5
done
docker compose ps

echo
if [ "${OK:-0}" = 1 ]; then
  [ "$MODE" = https ] && echo "Site is up: https://$DOMAIN" || echo "Site is up (test mode): http://$SERVER_IP"
  echo "Admin panel path: /$(grep '^DJANGO_ADMIN_URL=' .env | cut -d= -f2)"
  echo "Create the admin user:  docker compose exec web python manage.py createsuperuser"
else
  echo "The site did not answer yet. Logs:  docker compose logs --tail=80 web caddy"
fi
