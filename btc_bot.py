import requests
from datetime import datetime

TELEGRAM_TOKEN = "9268850431:AAExxS9BiH3CPpEaZLdO_5osmmqZty9-umM"
CHAT_ID = "7975050631"

def get_btc_price():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()["bitcoin"]
    return data["usd"], data.get("usd_24h_change")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload, timeout=10)

def main():
    try:
        price, change_24h = get_btc_price()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        change_str = f"{change_24h:+.2f}%" if change_24h is not None else "N/A"

        message = (
            f"₿ <b>Bitcoin Price</b>\n"
            f"💰 <b>${price:,.2f}</b>\n"
            f"📊 24h: {change_str}\n"
            f"🕒 {now}"
        )
        send_telegram(message)
        print(f"Sent: ${price:,.2f}")
    except Exception as e:
        send_telegram(f"⚠️ Error: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
