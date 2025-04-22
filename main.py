import requests, os, json, argparse, re, shelve, time

def main():

    parser = argparse.ArgumentParser(prog='DNS-IP Helper',
                    description='Sets the DNS to an IP address (if specified), otherwise defaults to the outgoing IP of the current machine.')

    parser.add_argument("-I", "--ipaddress", help = "IP address to apply, optional.")
    parser.add_argument("-H", "--hostname", help = "Target hostname, required.")
    parser.add_argument("-S", "--subdomain", help = "Target subdomain, optional.")
    args = parser.parse_args()

    shelve_file = shelve.open("dns.txt")
    CHECK_TIMEOUT = 600 # (600 seconds = 10 min)

    API_KEY=os.getenv('CF_API_KEY')
    if API_KEY is None:
        print("Environment variable CF_API_KEY is not set.")
        return

    if args.hostname:
        hostname = args.hostname
    else:
        print("Invalid hostname.")
        return
    
    if args.subdomain:
        subdomain = args.subdomain+"."+args.hostname
    else:
        subdomain = hostname

    if args.ipaddress:
        match = re.search(r"\b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))\b", args.ipaddress)
        if match:
            current_ip = args.ipaddress
        else:
            print("Invalid IP address.")
            return
    else:
        ip_request = requests.get("https://ifconfig.me/ip")
        current_ip = ip_request.text

        if ip_request.status_code != 200:
            print(f"ERROR: {ip_request.status_code}\nREASON: {ip_request.content}\n Error retrieving IP.")
            return

    print("Checking if server IP needs to be updated...")

    print("Searching for cache...")

    if 'ip' in shelve_file:
        print("Cache exists! Checking IP...")
        cached_ip = shelve_file['ip']
        print(f"Local IP: {current_ip} | Cached Server IP: {shelve_file['ip']}")
        if current_ip == cached_ip:
            print("IPs are the same, checking time since last cache update...")
            current_time = int(time.time())
            print(f"Time since last update (in minutes): {(int)((current_time - shelve_file['timestamp'])/60)}")
            if(current_time-shelve_file['timestamp'] < CHECK_TIMEOUT):
                print("Too soon to generate new cache. Nothing to do here.")
                return
            else:
                print("Cache oudated, fetching server IP via API.")
    else:
        print("Cache not found, generating new cache file and fetching server IP via API.")

    head = {'Authorization':f'Bearer {API_KEY}'}

    list_zones_url = f'https://api.cloudflare.com/client/v4/zones'
    list_zones_request = requests.get(url= list_zones_url, headers= head)
    if list_zones_request.status_code != 200:
            print(f"ERROR: {list_zones_request.status_code}\nREASON: {list_zones_request.content}\n Error retrieving zone ID.")
            return
    list_zones_content = json.loads(list_zones_request.content)
    ZONE_ID = next(x for x in list_zones_content['result'] if x['name'] == f'{hostname}')['id']


    list_records_url = f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records'
    list_records_request = requests.get(url= list_records_url, headers= head)
    if list_records_request.status_code != 200:
            print(f"ERROR: {list_records_request.status_code}\nREASON: {list_records_request.content}\n Error retrieving record.")
            return
    list_records_content = json.loads(list_records_request.content)
    try:
        DNS_RECORD_ID = next(x for x in list_records_content['result'] if x['name'] == f'{subdomain}' and x['type'] == 'A')['id']
    except StopIteration:
        print("No matching record found. Did you use the right hostname (or subdomain)?")
        return

        
    url = f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{DNS_RECORD_ID}'
    get_ip_request = requests.get(url = url, headers= head)
    server_content = json.loads(get_ip_request.content)

    if get_ip_request.status_code != 200:
        print(f"ERROR: {get_ip_request.status_code}\nREASON: {server_content['errors']}")
        return

    server_ip = server_content['result']['content']
    print(f"Local IP: {current_ip} | Server IP: {server_ip}")

    shelve_file['timestamp'] = int(time.time())
    shelve_file['ip'] = server_ip
    shelve_file.sync()
    shelve_file.close()



    if current_ip == server_ip:
        print("IPs are the same. No change needed.")
        return
        
    print("Different IPs found. Attempting update...")

    patch_head = {'Authorization':f'Bearer {API_KEY}', 'Content-Type':'application/json'}
    patch_payload = json.dumps({"content": f"{current_ip}"})
    patch_request = requests.patch(url = url, data = patch_payload, headers = patch_head)
    patch_content = json.loads(patch_request.content)

    if patch_request.status_code == 200:
        print(f"SUCCESS: {patch_request.status_code}")
        print("IP updated.")
    else:
        print(f"ERROR: {patch_request.status_code}\nREASON: {patch_content["errors"]}")
        return
    
if __name__ == "__main__":
    main()