import os

# ===== TELEGRAM BOT =====
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

# ===== TELEGRAM API =====
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

# ===== CANALI (ID FINALMENTE STABILI ✅)
CHANNELS = [
    -1001731133661,
    -1001818148294,
]

# ===== APP DA MONITORARE
APPS = {
    "3bmeteo": "3B Meteo",
    "prezzi benzina": "Prezzi Benzina",
}
