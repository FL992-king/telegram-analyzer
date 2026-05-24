import requests
import asyncio
import os
import re
from telethon import TelegramClient
from config import BOT_TOKEN, CHAT_ID, API_ID, API_HASH, CHANNELS, APPS

FILE = "last_id.txt"

def send_alert(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })

def load_last_id():
    if not os.path.exists(FILE):
        return 0
    with open(FILE, "r") as f:
        return int(f.read())

def save_last_id(msg_id):
    with open(FILE, "w") as f:
        f.write(str(msg_id))

def extract_version(text):
    match = re.search(r'\d+\.\d+(\.\d+)?', text)
    return match.group(0) if match else "Non trovata"

def extract_link(text):
    match = re.search(r'(https?://\S+)', text)
    return match.group(0) if match else "Link non disponibile"

def analyze_message(text):
    text_lower = text.lower()

    for key, name in APPS.items():
        if key in text_lower:
            version = extract_version(text)
            link = extract_link(text)

            return f"📱 {name}\n\n✅ Ultima versione: {version}\n🔗 Scarica qui: {link}"

    return None

async def main():
    async with TelegramClient("session", API_ID, API_HASH) as client:
        print("✅ Controllo multi-canale...")

        last_id = load_last_id()
        nuovi = []

        for channel in CHANNELS:
            entity = await client.get_entity(channel)
            messages = await client.get_messages(entity, limit=50)

            for msg in messages:
            if msg.id > last_id and msg.text:
                result = analyze_message(msg.text)
            if result:
                nuovi.append((msg.id, result))

        if nuovi:
            nuovi.sort(key=lambda x: x[0])

            testi = [item[1] for item in nuovi]
            send_alert("\n\n".join(testi))

            save_last_id(nuovi[-1][0])
        else:
            print("❗ Nessun aggiornamento trovato")

if __name__ == "__main__":
    asyncio.run(main())
