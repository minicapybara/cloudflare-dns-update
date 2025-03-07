import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Cloudflare
cf_zone_id = os.getenv('ZONE_ID')  
cf_api_token = os.getenv('API_TOKEN')  
cf_api_baseurl = f"https://api.cloudflare.com/client/v4/zones/{cf_zone_id}/dns_records"

# DNS records configuration
# ALLOW_LIST: List of DNS records that are allowed to be updated
# DENY_LIST: List of DNS records that are not allowed to be updated
# If both lists are empty, all records will be updated
# If ALLOW_LIST has entries, only those records will be updated (unless they are in DENY_LIST)
# If only DENY_LIST has entries, all records except those will be updated

allow_list_raw = os.getenv('ALLOW_LIST', '')
deny_list_raw = os.getenv('DENY_LIST', '')

allow_list = []
deny_list = []

if allow_list_raw and allow_list_raw.strip():
    allow_list = [record.strip() for record in allow_list_raw.split(',') if record.strip()]

if deny_list_raw and deny_list_raw.strip():
    deny_list = [record.strip() for record in deny_list_raw.split(',') if record.strip()]
    
# Logs
log_path = "./logs/log.out"
log_level = logging.DEBUG
