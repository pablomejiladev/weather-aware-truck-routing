# Stage 1: build the React frontend
FROM node:20-slim AS frontend
WORKDIR /fe
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
# Same-origin API calls in production (served by Django below).
ENV VITE_API_URL=""
RUN npm run build

# Stage 2: Django backend serving the API + the built frontend
FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBUG=false

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./
COPY --from=frontend /fe/dist ./frontend_dist

RUN SECRET_KEY=build python manage.py collectstatic --noinput

# Bind to the host's $PORT when provided (Koyeb/Railway/etc.), else 7860.
EXPOSE 7860
CMD gunicorn routing.wsgi --bind 0.0.0.0:${PORT:-7860} --workers 2 --timeout 120
