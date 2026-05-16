import time
import requests
from playwright.sync_api import sync_playwright

BOT_TOKEN = "8806170853:AAG00AtfG8sxzOjhwaRa2VMExW6lDLzUzN0"
CHAT_ID = "1547104263"

# =========================
# SYMBOLS (REAL EXCHANGE FORMAT)
# =========================
symbols = [
    "OANDA:XAUUSD",
    "OANDA:XAGUSD",
    "BINANCE:ETHUSDT"
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
        page.set_viewport_size({"width": 1400, "height": 800})

        for symbol in symbols:

            # SIMPLE CLEAN TRADINGVIEW CHART (NO LAYOUT)
            url = f"https://www.tradingview.com/chart/?symbol={symbol}&interval=5"

            page.goto(url, wait_until="networkidle")
            time.sleep(12)  # allow chart to load

            file_name = symbol.replace(":", "_") + "_5m.png"

            # screenshot ONLY visible chart area
            page.screenshot(path=file_name)

            send_telegram(file_name, f"{symbol} - 5M Chart")

        browser.close()

if __name__ == "__main__":
    run()
