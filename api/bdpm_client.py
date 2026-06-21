import requests

from config import API_URL


def search_medicine(name, timeout=10):
    """
    Recherche un medicament par nom auprès de l'API BDPM.

    Retourne le JSON de la réponse en cas de succès, ou un dict
    {"error": "..."} en cas d'échec (réseau, timeout, statut HTTP
    non-2xx, ou réponse non-JSON).
    """
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
    """
    Vérifie si l'API BDPM est accessible.

    Utilisé pour afficher un indicateur de statut dans l'interface.
    Retourne True si l'API répond (même avec un statut d'erreur côté
    application, tant que ce n'est pas une erreur serveur 5xx ou un
    problème réseau), False sinon.
    """
    try:
        response = requests.get(API_URL, timeout=timeout)
        return response.status_code < 500
    except requests.exceptions.RequestException:
        return False