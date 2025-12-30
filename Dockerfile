# ---- builder ----
FROM python:3.10-slim AS builder
WORKDIR /w

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/*

COPY requirements/api.txt requirements.txt
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ---- runtime ----
FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src
WORKDIR /app

COPY --from=builder /wheels /wheels
COPY requirements/api.txt requirements.txt
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt \
  && rm -rf /wheels

COPY serving/api/ /app/api
COPY src/ /app/src/
COPY serving/models/ /app/models/

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
