import requests

url = "http://127.0.0.1:8000/api/v1/personnel/corrections/"
print("Testing GET:", requests.get(url).status_code)
