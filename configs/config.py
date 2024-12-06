import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Cloudflare
cf_zone_id = os.getenv('ZONE_ID')  
cf_api_token = os.getenv('API_TOKEN')  
cf_api_baseurl = f"https://api.cloudflare.com/client/v4/zones/{cf_zone_id}/dns_records"

# Logs
log_path = "./logs/log.out"
log_level = logging.DEBUG
