import os

def get_env(name):
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Variabile {name} non trovata nei secrets GitHub")
    return value

BOT_TOKEN = get_env("BOT_TOKEN")
CHAT_ID = get_env("CHAT_ID")

API_ID = int(get_env("API_ID"))
API_HASH = get_env("API_HASH")

CHANNEL = "ApplicazioniCR"