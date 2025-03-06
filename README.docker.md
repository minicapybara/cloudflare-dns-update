# Running Cloudflare DNS Updater with Docker

This guide explains how to run the Cloudflare DNS Updater using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system (optional, but recommended)

## Configuration

There are two ways to configure the application when running with Docker:

### Option 1: Using docker-compose (Recommended)

1. Make sure you set the environment variable contains the required variables:
   ```
   ZONE_ID=your_cloudflare_zone_id
   API_TOKEN=your_cloudflare_api_token
   DNS_RECORDS_TO_UPDATE=record1.example.com,record2.example.com
   ```

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
  -e DNS_RECORDS_TO_UPDATE=record1.example.com,record2.example.com \
  -v $(pwd)/logs:/app/logs \
  --restart unless-stopped \
  cloudflare-dns-updater
```

## Viewing Logs

To view the logs from the container:

```bash
# Using docker-compose
docker-compose logs -f

# Using docker directly
docker logs -f cloudflare-dns-updater
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
