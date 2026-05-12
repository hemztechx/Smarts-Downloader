import asyncio
import os
import re
import argparse
from urllib.parse import urlparse
from pyppeteer import launch


def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]+', "_", name).strip("_") or "downloaded_page"


async def save_mhtml(url: str, output_file: str):
    browser = None
    try:
        browser = await launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
            ],
        )
        page = await browser.newPage()
        await page.goto(url, {"waitUntil": "networkidle2", "timeout": 120000})
        mhtml = await page._client.send("Page.captureSnapshot", {})
        with open(output_file, "wb") as f:
            f.write(mhtml["data"].encode("utf-8", errors="ignore"))
    finally:
        if browser is not None:
            await browser.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()

    parsed = urlparse(args.url)
    base = sanitize_filename(parsed.netloc + parsed.path.replace("/", "_"))

    os.makedirs("download", exist_ok=True)
    out_path = os.path.join("download", f"{base}.mhtml")

    # راه مطمئن برای CI
    asyncio.get_event_loop().run_until_complete(save_mhtml(args.url, out_path))

    print(f"✅ Saved: {out_path}")


if __name__ == "__main__":
    main()
