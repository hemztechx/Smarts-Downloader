import os
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

def save_mhtml(url, output_name):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(url)
        time.sleep(5)

        result = driver.execute_cdp_cmd("Page.captureSnapshot", {})
        mhtml = result["data"]

        filename = output_name if output_name else "page"
        path = f"downloads/{filename}.mhtml"

        os.makedirs("downloads", exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(mhtml)

        print("Saved:", path)

    finally:
        driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", required=False)

    args = parser.parse_args()
    save_mhtml(args.url, args.output)
