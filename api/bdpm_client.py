import requests

from config import API_URL


def search_medicine(name, timeout=10):

    try:
        response = requests.get(
            f"{API_URL}/medicaments/search",
            params={"q": name},
            timeout=timeout
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        return {"error": str(exc)}

    try:
        return response.json()
    except ValueError:
        return {"error": "Réponse invalide de l'API BDPM (JSON attendu)"}


def check_api_status(timeout=5):

    try:
        response = requests.get(API_URL, timeout=timeout)
        return response.status_code < 500
    except requests.exceptions.RequestException:
        return False