FROM python:3.11-slim
# Prevent Python from writing .pyc files and buffer logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
WORKDIR /app
# Install system dependencies
RUN apt-get update && \
apt-get install -y --no-install-recommends build-essential poppler-utils && \
rm -rf /var/lib/apt/lists/*
# Copy requirements first (better layer caching)
COPY backend/requirements.txt .
# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
pip install --no-cache-dir -r requirements.txt
# Install spaCy model
RUN python -m spacy download en_core_web_sm
# Copy project files
COPY backend/ ./backend/
COPY frontend/ ./frontend/
# Expose Flask port
EXPOSE 5000
# Start application with Gunicorn
CMD ["gunicorn", "backend.app:app", "--bind", "0.0.0.0:5000", "--workers", "3"]