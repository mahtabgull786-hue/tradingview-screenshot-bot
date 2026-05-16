import os
import time
import requests
from playwright.sync_api import sync_playwright

# =========================
# SEND TO TELEGRAM
# =========================
def send_telegram(image_path, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    with open(image_path, "rb") as img:
        requests.post(
            url,
            data={"chat_id": CHAT_ID, "caption": caption},
            files={"photo": img}
        )

# =========================
# MAIN BOT
# =========================
def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox"]
        )

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

            # search symbol in TradingView
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
