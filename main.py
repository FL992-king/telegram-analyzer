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

# ===== STORAGE =====
def load_versions():
    if not os.path.exists(FILE_VERSIONS):
        return {}
    with open(FILE_VERSIONS, "r") as f:
        return json.load(f)

def save_versions(data):
    with open(FILE_VERSIONS, "w") as f:
        json.dump(data, f)

# ===== ESTRAI VERSIONE DA FILE =====
def extract_version(filename):
    match = re.search(r'v?(\d+\.\d+(\.\d+)?)', filename.lower())
    return match.group(1) if match else None

# ===== VERSION COMPARE =====
def version_to_tuple(v):
    return tuple(map(int, v.split(".")))

# ===== ANALISI FILE APK =====
def analyze_file(msg):
    if not msg.file:
        return None

    filename = msg.file.name.lower()

    if not filename.endswith(".apk"):
        return None

    for key, name in APPS.items():
        if key in filename:
            version = extract_version(filename)

            if version:
                return name, version, msg

    return None

# ===== MAIN =====
async def main():
    async with TelegramClient("session", API_ID, API_HASH) as client:
        print("✅ Controllo APK diretto (file)")

        stored_versions = load_versions()
        best_files = {}

        entity = "me"

        for channel in CHANNELS:
            messages = await client.get_messages(channel, limit=50)

            for msg in messages:
                result = analyze_file(msg)

                if result:
                    name, version, real_msg = result

                    if name not in best_files:
                        best_files[name] = (version, real_msg)
                    else:
                        current_version = best_files[name][0]

                        if version_to_tuple(version) > version_to_tuple(current_version):
                            best_files[name] = (version, real_msg)

        for name, (version, msg) in best_files.items():
            last = stored_versions.get(name)

            if last != version:
                print(f"🔔 Nuova versione: {name} {version}")

                send_message(
                    f"📱 {name}\n\n"
                    f"✅ Ultima versione: {version}\n"
                    f"📎 APK incluso"
)

            # ✅ inoltra direttamente il messaggio originale
                await client.send_file(
                    "me",
                    msg)



                stored_versions[name] = version

        save_versions(stored_versions)

if __name__ == "__main__":
    asyncio.run(main())