# Build

FROM python:3.11-slim AS build

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Production
# Final image only contains required runtime components
FROM python:3.11-slim

WORKDIR /app

RUN useradd -m -u 1000 appuser

COPY --from=build /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

EXPOSE 443

CMD if [ "$USE_SSL" = "true" ]; then \
      gunicorn --bind 0.0.0.0:443 --workers 4 --timeout 120 --certfile /etc/ssl/certs/ssl-cert-snakeoil.pem --keyfile /etc/ssl/private/ssl-cert-snakeoil.key app:app; \
    else \
      gunicorn --bind 0.0.0.0:443 --workers 4 --timeout 120 app:app; \
    fi