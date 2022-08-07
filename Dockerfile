# syntax=docker/dockerfile:1

# Сборочный образ
FROM python:3.9-slim-bullseye as compile-image
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Итоговый образ для бота
FROM python:3.9-slim-bullseye
COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app
COPY tg_bot /app/tg_bot
CMD ["python", "-m", "tg_bot"]