import asyncio
import zipfile
import os
import re
import argparse
from pyppeteer import launch
from urllib.parse import urlparse

def sanitize_filename(name: str) -> str:
    """حذف کاراکترهای غیرمجاز برای نام فایل"""
    return re.sub(r'[\\/*?:"<>|]', "_", name)

async def save_mhtml(url: str, output_file: str):
    """ذخیره صفحه وب به صورت MHTML"""
    # تنظیمات مخصوص اجرا در محیط لینوکس گیت‌هاب
    browser = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle0'})
    mhtml_data = await page._client.send('Page.captureSnapshot', {})
    with open(output_file, 'wb') as f:
        f.write(mhtml_data['data'].encode())
    await browser.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()

    # استخراج نام برای فایل خروجی از روی آدرس سایت
    parsed = urlparse(args.url)
    base_name = sanitize_filename(parsed.netloc + parsed.path.replace('/', '_'))
    if not base_name or base_name == "_":
        base_name = "downloaded_page"

    # ایجاد پوشه دانلود
    os.makedirs("download", exist_ok=True)
    mhtml_path = os.path.join("download", f"{base_name}.mhtml")

    print(f"Starting download: {args.url}")
    asyncio.run(save_mhtml(args.url, mhtml_path))
    print(f"✅ Successfully saved to: {mhtml_path}")

if __name__ == "__main__":
    main()
