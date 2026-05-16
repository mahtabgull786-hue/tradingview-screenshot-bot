import os
import time
import requests
from playwright.sync_api import sync_playwright

# =========================
# TELEGRAM CONFIG
# =========================
BOT_TOKEN = "8806170853:AAG00AtfG8sxzOjhwaRa2VMExW6lDLzUzN0"
CHAT_ID = "1547104263"

# =========================
# SYMBOLS (CORRECT FORMAT)
# =========================
symbols = [
    "OANDA:XAUUSD",
    "OANDA:XAGUSD",
    "BINANCE:ETHUSDT"
]

# =========================
# SEND TO TELEGRAM
# =========================
def send_telegram(image_path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    with open(image_path, "rb") as img:
        response = requests.post(
            url,
            data={"chat_id": CHAT_ID, "caption": caption},
            files={"photo": img}
        )

    if response.status_code != 200:
        print("Telegram Error:", response.text)

# =========================
# MAIN BOT FUNCTION
# =========================
def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )

        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 720})

        for symbol in symbols:

            # FORCE 5 MIN CHART
            url = f"https://www.tradingview.com/chart/?symbol={symbol}&interval=5"

            print("Opening:", url)
            page.goto(url)

            # wait for chart to fully load
            time.sleep(15)

            # screenshot file name safe format
            file_name = symbol.replace(":", "_") + ".png"

            page.screenshot(path=file_name)

            send_telegram(file_name, f"{symbol} - 5M Chart")

        browser.close()

# =========================
# RUN
# =========================
if __name__ == "__main__":
    run()
