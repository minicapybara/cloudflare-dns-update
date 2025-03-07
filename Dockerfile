FROM python:3.10-slim

WORKDIR /app

# install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy the application code
COPY . .

# create logs directory
RUN mkdir -p logs

# set up cron job to run every 5 minutes
RUN echo "*/5 * * * * cd /app && /usr/local/bin/python3 cloudflare.py 2>&1 > /proc/1/fd/1" > /etc/cron.d/cloudflare-cron
RUN chmod 0644 /etc/cron.d/cloudflare-cron
RUN crontab /etc/cron.d/cloudflare-cron

# set environment variables
ENV PYTHONUNBUFFERED=1

# create a script to handle startup
RUN echo '#!/bin/sh\n\
touch /app/logs/log.out\n\
tail -f /app/logs/log.out & \n\
exec cron -f' > /app/start.sh && \
chmod +x /app/start.sh

# run the startup script
CMD ["/app/start.sh"] 