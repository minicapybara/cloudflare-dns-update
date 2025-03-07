# Cloudflare DNS Updater

This script updates Cloudflare DNS records with the current public IP address. It checks the existing records and updates them only if the IP has changed unless the `--force` option is provided.


## Setup

```bash
# create venv (optional)
python3 -m venv venv

# activate venv 
source ./venv/bin/activate

# install dependencies
pip install -r requirements.txt
```


## Configuration

#### Environment Variables
```sh
# cloudflare zone id
ZONE_ID=
# cloudflare api token
# permission: zone, dns, edit
API_TOKEN=
# DNS Records Update Configuration:

# ALLOW_LIST: Specify the DNS records that are allowed to be updated
# Example: allow updates only for api.example.com and www.example.com
ALLOW_LIST=api.example.com,www.example.com

# DENY_LIST: Specify the DNS records that should not be updated
# Example: prevent updates for test.example.com and dev.example.com
DENY_LIST=test.example.com,dev.example.com

# Update Rules:
# 1. If both ALLOW_LIST and DENY_LIST are empty: All DNS records will be updated
# 2. If ALLOW_LIST has entries: Only records in this list will be updated (unless they are in DENY_LIST)
# 3. If only DENY_LIST has entries: All records except those in DENY_LIST will be updated
# 4. Records in DENY_LIST will never be updated, even if they appear in ALLOW_LIST
```

## Usage

#### Manual run

```sh
usage: cloudflare.py [-h] [--force]

options:
  -h, --help   show this help message and exit
  --force, -f  Force dns record update
```

#### Cron

```sh
# runs every 5 minutes
*/5 * * * * /path/to/venv/python3 /path/to/script/cloudflare.py
```


## Logrotate

Setup logrotate for the program (Optional). Create file with below contents named cloudflare under /etc/logrotate.d/

```sh
/path/to/cloudflare/logs {
    daily               # Rotate the logs daily
    missingok           # Ignore errors if the log file is missing
    rotate 7            # Keep 7 days worth of backlogs
    compress            # Compress rotated files
    delaycompress       # Delay compression of the previous log file until the next rotation
    notifempty          # Don't rotate empty log files
}
```

## Docker



## Cloudflare API Reference

[Cloudflare API Docs](https://developers.cloudflare.com/api-next/resources/dns/subresources/records/)