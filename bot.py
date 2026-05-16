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
def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 720})

        chart_url = "https://www.tradingview.com/chart/zYV8pbip/"

        symbols = [
            "XAUUSD",
            "XAGUSD",
            "ETHUSDT"
        ]

        for symbol in symbols:
            page.goto(chart_url)
            time.sleep(10)

            page.keyboard.press("s")
            time.sleep(2)

            page.keyboard.type(symbol)
            time.sleep(2)

            page.keyboard.press("Enter")
            time.sleep(10)

            file_name = symbol + ".png"
            page.screenshot(path=file_name)

            send_telegram(file_name, symbol + " - 5M Chart")

        browser.close()

# =========================
# RUN
# =========================
if __name__ == "__main__":
    run()
