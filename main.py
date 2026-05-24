import requests
import asyncio
import os
import re
import json
from telethon import TelegramClient
from config import BOT_TOKEN, CHAT_ID, API_ID, API_HASH, CHANNELS, APPS

FILE_VERSIONS = "versions.json"

# ===== INVIO TELEGRAM =====
def send_alert(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })

# ===== STORAGE VERSIONI =====
def load_versions():
    if not os.path.exists(FILE_VERSIONS):
        return {}
    with open(FILE_VERSIONS, "r") as f:
        return json.load(f)

def save_versions(data):
    with open(FILE_VERSIONS, "w") as f:
        json.dump(data, f)

# ===== ESTRAZIONE VERSIONE =====
def extract_version(text):
    match = re.search(r'\d+\.\d+(\.\d+)?', text)
    return match.group(0) if match else None

# ===== ESTRAZIONE LINK (NO PLAYSTORE) =====
def extract_valid_link(text):
    links = re.findall(r'(https?://\S+)', text)

    for link in links:
        if "play.google.com" not in link:
            return link

    return None

# ===== CONFRONTO VERSIONI =====
def version_to_tuple(v):
    return tuple(map(int, v.split(".")))

# ===== ANALISI MESSAGGIO =====
def analyze_message(msg):
    if not msg.text:
        return None

    text_lower = msg.text.lower()

    for key, name in APPS.items():
        if key in text_lower:

            version = extract_version(msg.text)
            link = extract_valid_link(msg.text)

            # ✅ se c'è file telegram → priorità
            if msg.file:
                link = "📎 File disponibile nel canale"

            if version:
                return name, version, link

    return None

# ===== MAIN =====
async def main():
    async with TelegramClient("session", API_ID, API_HASH) as client:
        print("✅ Controllo avanzato app...")

        stored_versions = load_versions()
        best_versions = {}

        # 🔄 legge tutti i canali
        for channel in CHANNELS:
            messages = await client.get_messages(channel, limit=50)

            for msg in messages:
                result = analyze_message(msg)

                if result:
                    name, version, link = result

                    # ✅ salva solo la versione più alta per ogni app
                    if name not in best_versions:
                        best_versions[name] = (version, link)
                    else:
                        current_version = best_versions[name][0]

                        if version_to_tuple(version) > version_to_tuple(current_version):
                            best_versions[name] = (version, link)

        # ✅ INVIO SOLO SE CAMBIA
        for name, (version, link) in best_versions.items():
            last = stored_versions.get(name)

            if last != version:
                print(f"🔔 Nuova versione: {name} {version}")

                message = (
                    f"📱 {name}\n\n"
                    f"✅ Ultima versione: {version}\n"
                )

                if link:
                    message += f"🔗 Scarica qui: {link}"
                else:
                    message += "❗ Nessun link trovato"

                send_alert(message)

                stored_versions[name] = version

        save_versions(stored_versions)

if __name__ == "__main__":
    asyncio.run(main())