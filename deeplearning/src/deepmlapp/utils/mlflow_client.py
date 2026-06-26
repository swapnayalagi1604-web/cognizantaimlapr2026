import requests

payload = {
    "inputs": [
        [0.25, -0.42, 1.31]
    ]
}

response = requests.post(
    "http://127.0.0.1:5001/invocations",
    json=payload
)

print(response.json())