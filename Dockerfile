# Fase di build
FROM python:3.11-slim as builder

ARG VERSION=latest
ENV VERSION=${VERSION}

COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Fase finale
FROM python:3.11-slim

ARG VERSION=latest
LABEL org.opencontainers.image.version="${VERSION}" \
    org.opencontainers.image.source="https://github.com/gfsolone/amamilano" \
    org.opencontainers.image.created="${BUILD_DATE}" \
    org.opencontainers.image.licenses="MIT"

COPY --from=builder /root/.local /root/.local
COPY amamilano.py .
COPY verbs.txt .

ENV PATH=/root/.local/bin:$PATH \
    VERSION=${VERSION}
    
CMD ["python", "amamilano.py"]
