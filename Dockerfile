# Fase di build
FROM python:3.15.0a5-slim as builder

WORKDIR /app

# Installazione dipendenze build
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Fase finale
FROM python:3.15.0a5-slim

WORKDIR /app

ARG VERSION=latest
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    VERSION=${VERSION}

# Metadati OCI standard
LABEL org.opencontainers.image.version="${VERSION}" \
    org.opencontainers.image.source="https://github.com/gfsolone/amamilano" \
    org.opencontainers.image.title="AmaMilano Bot" \
    org.opencontainers.image.description="Bot Telegram per veri imbruttiti della City"

# Copia file necessari
COPY --from=builder /root/.local /root/.local
COPY amamilano.py verbs.txt ./

# Verifica esistenza file essenziali
RUN test -f verbs.txt || { echo "Errore: verbs.txt non trovato!"; exit 1; } && \
    chmod +x amamilano.py

ENV PATH=/root/.local/bin:$PATH

CMD ["python", "amamilano.py"]