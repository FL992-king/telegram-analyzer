import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

# ✅ SOLO canale privato
CHANNELS = [
    -1001818148294
]

# ✅ app da monitorare (match su nome file)
APPS = {
    "3bmeteo": "3B Meteo",
    "prezzi": "Prezzi Benzina",

    "spotify": "Spotify Mod",
    "spotif": "Spotify Mod",

    "flightradar": "Flightradar24 Mod",
}