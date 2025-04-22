FROM python:3.11-slim 

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    python3-venv \
    # git \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv /opt/venv

# Activate the virtual environment by default
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip and install requirements
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# #Entry Point
# COPY entrypoint.sh /app/
# RUN chmod +x /app/entrypoint.sh

# Copy project files
COPY . /app/

# ENTRYPOINT ["/app/entrypoint.sh"]
# Default command
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

RUN python manage.py collectstatic --noinput
