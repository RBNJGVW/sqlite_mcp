# ---- Etapa 1: build (opcional si no necesitas compilar deps nativas) ----
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Etapa 2: runtime ----
FROM python:3.12-slim

WORKDIR /app
# Copiamos deps de builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copiamos código fuente y la base de datos
COPY . .

EXPOSE 8000

CMD ["python", "-u", "server.py"]
