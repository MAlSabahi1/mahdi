import requests

url = "http://127.0.0.1:8000/api/v1/personnel/6099999/"
payload = {"expense_status": "no_expenses", "qualification": None}
res = requests.patch(url, json=payload)
print(res.status_code)
print(res.json())
