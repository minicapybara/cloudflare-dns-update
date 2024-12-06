import os 
import requests
import json
import logging 
import argparse
from datetime import datetime 
from configs import config

# surpress logs
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

def setup_logger(log_file, log_level=logging.INFO):
    if log_file and not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))
    
    logging.basicConfig(
        filename=log_file, 
        level=log_level, 
        format=f'%(asctime)-15s - %(name)s - %(levelname)s - %(filename)s/%(funcName)s/%(lineno)d - %(message)s'
    )

def get_public_ip():
    try:
        response = requests.get('http://checkip.amazonaws.com')
        return response.text.strip()
    except Exception as e:
        logging.error(f"get_public_ip(): {e}")
        return None 

def get_dns_records():
    try:
        headers = {
            "Authorization": f"Bearer {config.cf_api_token}",
            "Content-Type": "application/json"
        }

        response = requests.get(config.cf_api_baseurl, headers=headers)
        
        records = []
        if response.status_code == 200:
            for result in response.json()['result']:
                records.append({
                    "id": result.get("id"),
                    "content": result.get("content").strip(),
                    "name": result.get("name")
                })
        
        return records
        
    except Exception as e:
        logging.error(f"get_dns_records(): {e}") 
        return None 
    
def update_dns_record(record, ip):
    id = record.get("id")
    content = record.get("content")
    name = record.get("name")

    logging.info(
        f"Updating record: {name} :"
        f"Id: {id}. "
        f"Original Content: {content}. "
        f"New Content: {ip}. "
    )
    
    url = f"{config.cf_api_baseurl}/{id}"

    payload = json.dumps({
        "comment": f"Updated by autoscript @ {datetime.now()}",
        "content": ip
        })
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Email": "",
        "Authorization": f"Bearer {config.cf_api_token}",
    }

    try:
        response = requests.patch(url, headers=headers, data=payload)
        if response.status_code == 200:
            logging.info(f"Successfully updated {name} to {ip}")
            logging.debug(f"response: {response.json()}")
        else:
            logging.error(
                f"Fail to update dns record: "
                f"code: {response.status_code} "
                f"message: {response.json()}"
            )
    except Exception as e:
        logging.error(f"update_dns_record(): {e}")

if __name__ == '__main__':
    # args  
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", "-f", help="Force dns record update", action="store_true")
    args = parser.parse_args()

    # logger 
    setup_logger(config.log_path, config.log_level)

    # get ip 
    ip = get_public_ip()
    logging.info(f"current ip: {ip}")

    # get records
    records = get_dns_records()
    logging.debug(f"get_dns_records: {records}")

    for record in records:
        # skip if ip is not changed
        if ip == record.get("content") and not args.force:
            logging.info(f"ip is not changed, skipping {record['name']}")
            continue 
        
        update_dns_record(record, ip)


