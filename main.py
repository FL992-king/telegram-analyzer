import requests
import asyncio
import os
from telethon import TelegramClient
from config import BOT_TOKEN, CHAT_ID, API_ID, API_HASH, CHANNEL

KEYWORDS = ["nuo va versione", "aggiornamento"]
APPS = ["3bmeteo", "prezzi benzina"]

FILE = "last_id.txt"

def check_message(text):
    if not text:
        return False
    text = text.lower()
    keyword_ok = any(k in text for k in KEYWORDS)
    app_ok = any(app in text for app in APPS)
    return keyword_ok and app_ok

def send_alert(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": f"📱 Nuovi aggiornamenti app:\n\n{text}"
    })

def load_last_id():
    if not os.path.exists(FILE):
        return 0
    with open(FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        return int(content) if content.isdigit() else 0

def save_last_id(msg_id):
    with open(FILE, "w", encoding="utf-8") as f:
        f.write(str(msg_id))

async def main():
    async with TelegramClient("session", API_ID, API_HASH) as client:
        print("✅ Controllo giornaliero...")

        last_id = load_last_id()
        messages = await client.get_messages(CHANNEL, limit=50)

        nuovi = []

        for msg in messages:
            if msg.id > last_id and getattr(msg, "text", None):
                if check_message(msg.text):
                    nuovi.append(msg)

        if nuovi:
            nuovi.sort(key=lambda x: x.id)

            testi = [m.text for m in nuovi]
            send_alert("\n\n".join(testi))

            save_last_id(nuovi[-1].id)
        else:
            print("❗ Nessun aggiornamento trovato")

if __name__ == "__main__":
    asyncio.run(main())
