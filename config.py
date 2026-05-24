import os

# ===== TELEGRAM BOT =====
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# ===== TELEGRAM API (Telethon) =====
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

# ===== CANALI DA MONITORARE =====
CHANNELS = [
    "https://t.me/+fHhFxAb1fEE3NmIx",   # CANALE PRIVATO
]

# ===== APP DA MONITORARE =====
# "chiave": "nome visualizzato"
APPS = {
    "3bmeteo": "3B Meteo",
    "prezzi benzina": "Prezzi Benzina",
}

