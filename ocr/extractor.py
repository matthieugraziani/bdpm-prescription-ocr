import cv2
import easyocr

_reader = None


def get_reader(lang_list=None, gpu=False):
    """
    Retourne une instance partagée du lecteur EasyOCR, en la créant au
    premier appel uniquement.

    Le chargement des modèles EasyOCR est coûteux (plusieurs secondes,
    téléchargement au premier lancement) : il ne doit pas se produire à
    l'import du module, mais seulement lorsque l'OCR est réellement utilisé.
    """
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(lang_list or ["fr"], gpu=gpu)
    return _reader


def preprocess(image):
    """
    Prétraite une image (tableau numpy) pour améliorer la qualité de l'OCR :
    conversion en niveaux de gris, débruitage léger, puis seuillage adaptatif.

    Accepte une image en couleur (RGB, 3 canaux) ou déjà en niveaux de gris.
    """
    if image.ndim == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    else:
        gray = image

    denoised = cv2.fastNlMeansDenoising(gray, h=10)

    return cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11,
    )


def extract(image, preprocess_image=True, gpu=False):
    """
    Extrait le texte d'une image (tableau numpy RGB ou niveaux de gris).

    Args:
        image: tableau numpy représentant l'image.
        preprocess_image: si True (par défaut), applique `preprocess()`
            avant l'OCR pour améliorer la reconnaissance.
        gpu: passé à EasyOCR pour activer/désactiver l'accélération GPU.

    Returns:
        Le texte détecté, une ligne par zone de texte reconnue.
    """
    if preprocess_image:
        image = preprocess(image)

    reader = get_reader(gpu=gpu)
    return "\n".join(reader.readtext(image, detail=0))