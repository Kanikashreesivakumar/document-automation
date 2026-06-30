import requests

url = "http://localhost:8000/api/shipments/3398b4f2-98ac-4bb1-aa2f-d306d9fa1fd5/animal-annexure"
payload = {
    "producer_name": "TEST PRODUCER",
    "certificate_number": "001"
}
headers = {'Content-Type': 'application/json'}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
