import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Cloudflare
cf_zone_id = os.getenv('ZONE_ID')  
cf_api_token = os.getenv('API_TOKEN')  
cf_api_baseurl = f"https://api.cloudflare.com/client/v4/zones/{cf_zone_id}/dns_records"

# specific DNS records to update, leave empty to update all records
# example: ['api.example.com', 'www.example.com']
# optimize the environment variable processing logic to ensure correct reading and processing of environment variable values
dns_records_raw = os.getenv('DNS_RECORDS_TO_UPDATE', '')
# Handling empty strings or only spaces
dns_records_to_update = []
if dns_records_raw and dns_records_raw.strip():
    # Split and remove leading and trailing spaces from each entry
    dns_records_to_update = [record.strip() for record in dns_records_raw.split(',') if record.strip()]
    
# Logs
log_path = "./logs/log.out"
log_level = logging.DEBUG
