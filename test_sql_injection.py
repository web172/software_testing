import requests
def test_sql_injection():
    url ="http://127.0.0.1:5000/login"
    payload = {"username": "' OR 1=1 --","password": "xxx"}
    res = requests.post(url, json=payload)
    assert res.status_code == 400 or "error" in res.text.lower()