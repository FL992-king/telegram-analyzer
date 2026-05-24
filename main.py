import requests
import asyncio
import os
import re
import json
from telethon import TelegramClient
from config import BOT_TOKEN, CHAT_ID, API_ID, API_HASH, CHANNELS, APPS

FILE_VERSIONS = "versions.json"

# ===== INVIO TESTO =====
def send_message(text):
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

# ===== VERSIONE =====
def extract_version(text):
    match = re.search(r'\d+\.\d+(\.\d+)?', text)
    return match.group(0) if match else None

def version_to_tuple(v):
    return tuple(map(int, v.split(".")))

# ===== ANALISI =====
def analyze_message(msg):
    if not msg.text or not msg.file:
        return None

    text_lower = msg.text.lower()

    for key, name in APPS.items():
        if key in text_lower:
            version = extract_version(msg.text)

            if version:
                return name, version

    return None

# ===== MAIN =====
async def main():
    async with TelegramClient("session", API_ID, API_HASH) as client:
        print("✅ Controllo APK diretto...")

        entity = "me"

        stored_versions = load_versions()
        best_messages = {}

        for channel in CHANNELS:
            messages = await client.get_messages(channel, limit=50)

            for msg in messages:
                result = analyze_message(msg)

                if result:
                    name, version = result

                    if name not in best_messages:
                        best_messages[name] = (version, msg)
                    else:
                        current_version = best_messages[name][0]

                        if version_to_tuple(version) > version_to_tuple(current_version):
                            best_messages[name] = (version, msg)

        for name, (version, msg) in best_messages.items():
            last = stored_versions.get(name)

            if last != version:
                send_message(
                    f"📱 {name}\n\n"
                    f"✅ Ultima versione: {version}\n"
                    f"📎 APK incluso:"
                )

                await client.send_file(entity, msg.media)

                stored_versions[name] = version

        save_versions(stored_versions)


if __name__ == "__main__":
    asyncio.run(main())
