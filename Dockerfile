# Step 1: Base image
FROM python:3.12.3-slim

# Step 2: Prevent Python from writing pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Step 3: Set working directory
WORKDIR /app

# Step 4: Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Step 5: Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the rest of the code
COPY . /app

# Step 7: Expose FastAPI port
EXPOSE 8000

# Run Alembic migrations and then start the app
CMD ["bash", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"]
