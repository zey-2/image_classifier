# Use official Python slim image for smaller image size
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install OS packages required to build and run Python packages such as Pillow
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libgl1 \
       libglib2.0-0 \
       libjpeg-dev \
       zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application files
COPY . /app

# The bot will load a model from HuggingFace the first time it runs. Optionally
# you can provide a local cache via a volume on /root/.cache/huggingface

# The TELEGRAM_API_KEY should be provided at runtime (docker run -e TELEGRAM_API_KEY=...)
ENV PYTHONUNBUFFERED=1

# Run the bot
CMD ["python", "app.py"]
