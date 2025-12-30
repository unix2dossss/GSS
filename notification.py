from dotenv import load_dotenv
import requests
import os

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("Missing Telegram env vars")

def notify(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=10)
        print(r.status_code, r.text)
        r.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"[WARN] Telegram notify failed: {e}")
        return False


def send_photo(image_path: str, caption: str = ""):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    try:
        with open(image_path, "rb") as f:
            r = requests.post(
                url,
                data={"chat_id": CHAT_ID, "caption": caption},
                files={"photo": f},
                timeout=30
            )
            r.raise_for_status()
        print("Telegram:", r.status_code, r.text)
        return True
    except requests.RequestException as e:
        print(f"[WARN] Telegram send photo failed: {e}")
        return False


if __name__ == "__main__":
    notify("notification.py test message")