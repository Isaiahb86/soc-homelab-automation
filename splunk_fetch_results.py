import requests
import time
import base64
import urllib3
import os

# Suppress insecure HTTPS warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Splunk credentials and connection settings
username = 'admin'
password = 'isaiah123'  # Replace with your actual Splunk password
auth_str = f"{username}:{password}"
b64_auth = base64.b64encode(auth_str.encode()).decode()

headers = {
    'Authorization': f'Basic {b64_auth}'
}

# Define the search query
search_query = 'search index=* host=192.168.1.101 sudo'
data = {
    'search': search_query,
    'exec_mode': 'normal'
}

# Step 1: Submit the search job to Splunk with JSON response format
response = requests.post(
    'https://localhost:8089/services/search/jobs?output_mode=json',
    headers=headers,
    data=data,
    verify=False
)

print("Search job created.")
print(f"Status Code: {response.status_code}")
print(f"Raw Response: {response.text}")

# Step 2: Extract SID (Search ID) from JSON response
sid = response.json()['sid']
print(f"SID: {sid}")

# Step 3: Poll for job completion
status_url = f'https://localhost:8089/services/search/jobs/{sid}?output_mode=json'
is_done = False

print("Checking search job status...")
while not is_done:
    status_response = requests.get(status_url, headers=headers, verify=False)
    content = status_response.json()
    is_done = content['entry'][0]['content']['isDone']
    if not is_done:
        time.sleep(2)  # Wait 2 seconds before checking again

# Step 4: Fetch the results
results_url = f'https://localhost:8089/services/search/jobs/{sid}/results?output_mode=json'
results_response = requests.get(results_url, headers=headers, verify=False)

# Step 5: Print the results
print("Search Results:")
results = results_response.json().get('results', [])
print(results)

# Step 6: Extract IPs and write to file if not already listed
blocked_ip_file = '/home/isaiah/blocked_ip/blocked_ips.txt'

# Ensure the file exists
os.makedirs(os.path.dirname(blocked_ip_file), exist_ok=True)
if not os.path.exists(blocked_ip_file):
    open(blocked_ip_file, 'w').close()

for result in results:
    ip = result.get("host")
    if ip:
        with open(blocked_ip_file, "r") as file:
            existing_ips = file.read().splitlines()

        if ip not in existing_ips:
            with open(blocked_ip_file, "a") as file:
                file.write(f"{ip}\n")
                print(f"[+] Added new blocked IP: {ip}")


