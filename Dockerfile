FROM python:3.10-slim

WORKDIR /app

# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Set up cron job to run every 5 minutes
RUN echo "*/5 * * * * cd /app && /usr/local/bin/python3 cloudflare.py >> /app/logs/cron.log 2>&1" > /etc/cron.d/cloudflare-cron
RUN chmod 0644 /etc/cron.d/cloudflare-cron
RUN crontab /etc/cron.d/cloudflare-cron

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run cron in foreground
CMD ["cron", "-f"] 