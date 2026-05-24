import requests
import asyncio
import os
import re
import json
from telethon import TelegramClient
from config import BOT_TOKEN, CHAT_ID, API_ID, API_HASH, CHANNELS, APPS

FILE_VERSIONS = "versions.json"

def send_alert(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })

def load_versions():
    if not os.path.exists(FILE_VERSIONS):
        return {}
    with open(FILE_VERSIONS, "r") as f:
        return json.load(f)

def save_versions(data):
    with open(FILE_VERSIONS, "w") as f:
        json.dump(data, f)

def extract_version(text):
    match = re.search(r'\d+\.\d+(\.\d+)?', text)
    return match.group(0) if match else None

def extract_link(text):
    match = re.search(r'(https?://\S+)', text)
    return match.group(0) if match else None

def analyze_message(text):
    text_lower = text.lower()

    for key, name in APPS.items():
        if key in text_lower:
            version = extract_version(text)
            link = extract_link(text)

            if version and link:
                return name, version, link

    return None, None, None

async def main():
    async with TelegramClient("session", API_ID, API_HASH) as client:
        print("✅ Controllo avanzato app...")

        stored_versions = load_versions()

        for channel in CHANNELS:
            messages = await client.get_messages(channel, limit=50)

            for msg in messages:
                if not msg.text:
                    continue

                name, version, link = analyze_message(msg.text)

                if name:
                    last_version = stored_versions.get(name)

                    if last_version != version:
                        print(f"🔔 Nuova versione trovata: {name} {version}")

                        send_alert(
                            f"📱 {name}\n\n"
                            f"✅ Ultima versione: {version}\n"
                            f"🔗 Scarica qui: {link}"
                        )

                        stored_versions[name] = version

        save_versions(stored_versions)

if __name__ == "__main__":
    asyncio.run(main())
