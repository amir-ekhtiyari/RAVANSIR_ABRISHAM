# Ravan Seir Abrisham website – production image (Django + gunicorn).
#
# On servers that cannot reach Docker Hub / PyPI directly (e.g. in Iran), pass mirrors:
#   docker compose build --build-arg PYTHON_IMAGE=docker.arvancloud.ir/python:3.13-slim \
#                        --build-arg PIP_INDEX_URL=https://mirror-pypi.runflare.com/simple
ARG PYTHON_IMAGE=python:3.13-slim

# ---------- build stage: compile wheels once ----------
FROM ${PYTHON_IMAGE} AS build
ARG PIP_INDEX_URL=https://pypi.org/simple
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_NO_CACHE_DIR=1 PIP_INDEX_URL=${PIP_INDEX_URL}
WORKDIR /build
COPY requirements.txt requirements-docker.txt ./
RUN pip wheel --wheel-dir /wheels -r requirements-docker.txt

# ---------- runtime stage ----------
FROM ${PYTHON_IMAGE}
LABEL org.opencontainers.image.title="ravansir-abrisham-web" \
      org.opencontainers.image.description="Ravan Seir Abrisham International Transportation website"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_DEBUG=0 \
    DJANGO_CACHE_DIR=/tmp/django-cache \
    PORT=8000

# libpq is bundled in psycopg[binary]; curl-less healthcheck uses Python.
RUN groupadd --system --gid 1000 app && useradd --system --uid 1000 --gid app --home /app --shell /usr/sbin/nologin app

WORKDIR /app
COPY --from=build /wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* && rm -rf /wheels

COPY --chown=app:app . .
RUN chmod +x docker/entrypoint.sh \
 && mkdir -p /app/staticfiles /app/media /tmp/django-cache \
 && chown -R app:app /app/staticfiles /app/media /tmp/django-cache

USER app
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
  CMD ["python", "docker/healthcheck.py"]

ENTRYPOINT ["docker/entrypoint.sh"]
CMD ["gunicorn", "ravansir_abrisham.wsgi:application", "--config", "docker/gunicorn.conf.py"]
