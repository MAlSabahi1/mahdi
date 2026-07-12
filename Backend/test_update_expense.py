import requests

url = "http://127.0.0.1:8000/api/v1/personnel/6099999/"
payload = {"expense_status": "has_expenses"}
res = requests.patch(url, json=payload, headers={"Authorization": "Token 7edb569cd4e6b72a4f475a89dfba9dae3d0972b2"})
print(res.status_code)
print(res.json())
