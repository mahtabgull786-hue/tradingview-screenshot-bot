import os
import time
import requests
from playwright.sync_api import sync_playwright

# =========================
# TELEGRAM CONFIG
# =========================
BOT_TOKEN = "8806170853:AAG00AtfG8sxzOjhwaRa2VMExW6lDLzUzN0"
CHAT_ID = "1547104263"

symbols = [
    "XAUUSD",
    "XAGUSD",
    "ETHUSDT.P"
]

def send_telegram(image_path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as img:
        requests.post(url, data={"chat_id": CHAT_ID, "caption": caption}, files={"photo": img})

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )
        page = browser.new_page()

        for symbol in symbols:
            url = f"https://www.tradingview.com/chart/?symbol=OANDA:{symbol}"
            page.goto(url)
            time.sleep(15)  # IMPORTANT: allow full load

            page.set_viewport_size({"width": 1280, "height": 720})

            file_name = f"{symbol}.png"
            page.screenshot(path=file_name)

            send_telegram(file_name, f"{symbol} - 1H Chart")

        browser.close()

if __name__ == "__main__":
    run()
