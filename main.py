import requests
import asyncio
import os
import re
import json
from telethon import TelegramClient
from config import BOT_TOKEN, CHAT_ID, API_ID, API_HASH, CHANNELS, APPS

FILE_VERSIONS = "versions.json"

# ===== INVIO MESSAGGIO =====
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

# ===== VERSIONE DA NOME FILE =====
def extract_version(filename):
    match = re.search(r'v?(\d+\.\d+(\.\d+)?)', filename.lower())
    return match.group(1) if match else None

# ===== CONFRONTO VERSIONI =====
def version_to_tuple(v):
    return tuple(map(int, v.split(".")))

# ===== LINK TELEGRAM DIRETTO =====
def build_telegram_link(msg):
    chat_id = str(msg.chat_id).replace("-100", "")
    return f"https://t.me/c/{chat_id}/{msg.id}"

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
        print("✅ Monitor APK (versione veloce con link)")

        stored_versions = load_versions()
        best_files = {}

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

        # ✅ INVIO SOLO NUOVE VERSIONI
        for name, (version, msg) in best_files.items():
            last = stored_versions.get(name)

            if last != version:
                link = build_telegram_link(msg)

                print(f"🔔 Nuova versione: {name} {version}")

                send_message(
                    f"📱 {name}\n\n"
                    f"✅ Ultima versione: {version}\n"
                    f"📥 Scarica APK:\n{link}"
                )

                stored_versions[name] = version

        save_versions(stored_versions)

if __name__ == "__main__":
    asyncio.run(main())