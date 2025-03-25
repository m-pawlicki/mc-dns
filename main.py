import requests, os, json

def main():

    API_KEY=os.getenv('CF_API_KEY')

    ip_request = requests.get("https://ifconfig.me/ip")
    current_ip = ip_request.text

    if ip_request.status_code != 200:
        print(f"ERROR: {ip_request.status_code}\nREASON: {ip_request.content}\n Error retrieving IP, quitting.")
        return

    if API_KEY is None:
        print("Environment variable CF_API_KEY is not set, quitting.")
        return

    print("Checking if server IP needs to be updated...")

    head = {'Authorization':f'Bearer {API_KEY}'}

    list_zones_url = f'https://api.cloudflare.com/client/v4/zones'
    list_zones_request = requests.get(url= list_zones_url, headers= head)
    list_zones_content = json.loads(list_zones_request.content)
    ZONE_ID = next(x for x in list_zones_content['result'] if x['name'] == 'jdkendall.com')['id']

    list_records_url = f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records'
    list_records_request = requests.get(url= list_records_url, headers= head)
    list_records_content = json.loads(list_records_request.content)
    DNS_RECORD_ID = next(x for x in list_records_content['result'] if x['name'] == 'minecraft.jdkendall.com' and x['type'] == 'A')['id']

    
    url = f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{DNS_RECORD_ID}'
    get_ip_request = requests.get(url = url, headers= head)
    server_content = json.loads(get_ip_request.content)

    if get_ip_request.status_code == 200:
        print(f"SUCCESS: {get_ip_request.status_code}")
    else:
        print(f"ERROR: {get_ip_request.status_code}\nREASON: {server_content['errors']}")
        return

    server_ip = server_content['result']['content']
    print(f"Local IP: {current_ip} | Server IP: {server_ip}")


    if current_ip == server_ip:
        print("IPs are the same. No change needed, quitting.")
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