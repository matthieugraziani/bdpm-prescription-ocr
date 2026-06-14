import requests
from config import API_URL
def search_medicine(name):
    try:
        r=requests.get(f"{API_URL}/search",params={"name":name},timeout=10)
        return r.json()
    except Exception as e:
        return {"error":str(e)}
