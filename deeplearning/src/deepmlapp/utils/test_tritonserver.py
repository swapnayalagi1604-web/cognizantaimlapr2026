import requests
import json

url = "http://51.20.84.134:8000/v2/models/loan_model/infer"

payload = {
    "inputs": [
        {
            "name": "loan_raw_input",
            "shape": [1, 3],
            "datatype": "FP32",
            "data": [[36513, 121, 23]]
        }
    ],
    "outputs": [
        {
            "name": "loan_output"
        }
    ]
}

response = requests.post(url, json=payload)

print(response.status_code)
print(json.dumps(response.json(), indent=4))

score = response.json()["outputs"][0]["data"][0]

print("Score:", score)
print("Prediction:", "Loan Approved" if score > 0.5 else "Loan Rejected")