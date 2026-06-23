from rapidfuzz import fuzz, process

# Référentiel de secours utilisé pour corriger les erreurs OCR courantes
# avant interrogation de l'API BDPM.
#
# TODO: remplacer/compléter cette liste par les dénominations réelles des
# spécialités BDPM (ex. via un endpoint de l'API qui exposerait la liste des
# noms connus), afin de couvrir bien plus que ces quelques médicaments
# courants.
DEFAULT_KNOWN = [
    "doliprane",
    "amoxicilline",
    "spasfon",
    "ibuprofene",
    "paracetamol",
    "augmentin",
    "levothyrox",
    "kardegic",
    "ventoline",
    "smecta",
    "dafalgan",
    "efferalgan",
    "advil",
    "xanax",
    "amlodipine",
    "metformine",
    "atorvastatine",
    "omeprazole",
    "lansoprazole",
    "esomeprazole",
    "tramadol",
    "codeine",
    "azithromycine",
    "clamoxyl",
]

# Score minimal (0-100) à partir duquel on considère qu'une ligne OCR
# correspond à un nom de médicament de référence.
DEFAULT_THRESHOLD = 80


def normalize(text, known=None, threshold=DEFAULT_THRESHOLD):

    cleaned = text.strip().lower()
    if not cleaned:
        return cleaned, 0, False

    candidates = known or DEFAULT_KNOWN
    result = process.extractOne(cleaned, candidates, scorer=fuzz.WRatio)

    if result is None:
        return cleaned, 0, False

    match, score, _ = result
    if score >= threshold:
        return match, score, True

    return cleaned, score, False