# splunk_search.py - Queries Splunk for a saved search and checks if it's complete

import requests
import base64
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# === CONFIGURATION ===
SPLUNK_HOST = "https://localhost:8089"
USERNAME = "admin"
PASSWORD = "isaiah123"  # Replace with your actual Splunk password

# Prepare HTTP Basic Auth header
credentials = f"{USERNAME}:{PASSWORD}"
b64_auth = base64.b64encode(credentials.encode()).decode()
headers = {
    'Authorization': f'Basic {b64_auth}'
}

# === STEP 1: Create Search Job ===
search_query = "search index=* host=192.168.1.101 sudo"

search_url = f"{SPLUNK_HOST}/services/search/jobs?output_mode=json"
response = requests.post(search_url, headers=headers, data={
    'search': search_query,
    'exec_mode': 'normal'
}, verify=False)

print("Status code:", response.status_code)
print("Response:", response.text)

# Parse SID
sid = response.json()['sid']
print("SID:", sid)

# === STEP 2: Wait for Search to Complete ===
job_status_url = f"{SPLUNK_HOST}/services/search/jobs/{sid}?output_mode=json"

while True:
    status_response = requests.get(job_status_url, headers=headers, verify=False)
    print("Status Check Response Code:", status_response.status_code)
    print("Status Check Raw Content:", status_response.text)

    if status_response.status_code != 200:
        print("Failed to get status. Exiting.")
        break

    content = status_response.json()

    if content['entry'][0]['content']['isDone']:
        print("Search job is done.")
        break

    time.sleep(1)

# === STEP 3: Fetch Results ===
results_url = f"{SPLUNK_HOST}/services/search/jobs/{sid}/results?output_mode=json"
results_response = requests.get(results_url, headers=headers, verify=False)
print("Results:", results_response.text)



