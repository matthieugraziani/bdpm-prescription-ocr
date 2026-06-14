from rapidfuzz import process
KNOWN=["doliprane","amoxicilline","spasfon"]
def normalize(text):
    return process.extractOne(text.lower(),KNOWN)[0]
