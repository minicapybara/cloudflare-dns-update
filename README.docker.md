# Running Cloudflare DNS Updater with Docker

This guide explains how to run the Cloudflare DNS Updater using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system (optional, but recommended)

## Configuration

There are two ways to configure the application when running with Docker:

### Option 1: Using docker-compose (Recommended)

1. Make sure you set the environment variables in your `.env` file:
   ```
   ZONE_ID=your_cloudflare_zone_id
   API_TOKEN=your_cloudflare_api_token
   ALLOW_LIST=record1.example.com,record2.example.com
   DENY_LIST=test.example.com,dev.example.com
   ```

   Configuration Options:
   - `ZONE_ID`: Your Cloudflare zone ID
   - `API_TOKEN`: Your Cloudflare API token
   - `ALLOW_LIST`: (Optional) Comma-separated list of DNS records that are allowed to be updated
   - `DENY_LIST`: (Optional) Comma-separated list of DNS records that should not be updated

   DNS Update Rules:
   - If both `ALLOW_LIST` and `DENY_LIST` are empty: All DNS records will be updated
   - If `ALLOW_LIST` has entries: Only records in this list will be updated (unless they are in `DENY_LIST`)
   - If only `DENY_LIST` has entries: All records except those in `DENY_LIST` will be updated
   - Records in `DENY_LIST` will never be updated, even if they appear in `ALLOW_LIST`

2. Run the container using docker-compose:
   ```bash
   docker-compose up -d
   ```

### Option 2: Using Docker directly

Run the container with environment variables:

```bash
docker build -t cloudflare-dns-updater .

docker run -d \
  --name cloudflare-dns-updater \
  -e ZONE_ID=your_cloudflare_zone_id \
  -e API_TOKEN=your_cloudflare_api_token \
  -e ALLOW_LIST=record1.example.com,record2.example.com \
  -e DENY_LIST=test.example.com,dev.example.com \
  -v $(pwd)/logs:/app/logs \
  --restart unless-stopped \
  cloudflare-dns-updater
```

## Logging System

The application uses a dual logging system:

1. File Logging:
   - All logs are written to `/app/logs/log.out` inside the container
   - Logs are persisted on the host machine through volume mounting at `./logs/log.out`
   - Useful for historical log review and debugging

2. Docker Logging:
   - All logs are also available through Docker's logging system
   - Can be viewed using `docker logs` command
   - Configured with log rotation (max 10MB per file, max 3 files)
   - Ideal for real-time monitoring and integration with container orchestration systems

## Viewing Logs

To view the logs from the container:

```bash
# Using docker-compose
docker-compose logs -f

# Using docker directly
docker logs -f cloudflare-dns-updater

# Viewing log file directly
cat ./logs/log.out
```

## Updating the Container

When you make changes to the code or want to update the container:

```bash
# Using docker-compose
docker-compose down
docker-compose build
docker-compose up -d

# Using docker directly
docker stop cloudflare-dns-updater
docker rm cloudflare-dns-updater
docker build -t cloudflare-dns-updater .
# Then run the container again with the command from the setup section
```
