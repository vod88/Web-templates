import os
import asyncio
from playwright.async_api import async_playwright
import urllib.parse

BASE_URL = "https://web-templates-f0x.pages.dev/349套HTML5+CSS3免费网站模板下载/"
OUTPUT_DIR = "thumbs"
MAX_CONCURRENT = 5 # 同时截5个，CF Pages 免费版足够了

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def screenshot_one(browser, i):
    num = str(i).zfill(3)
    output_path = f"{OUTPUT_DIR}/{num}.jpg"

    if os.path.exists(output_path):
        print(f"{num} 已存在，跳过")
        return

    folder_encoded = urllib.parse.quote("349套HTML5+CSS3免费网站模板下载")
    url = f"https://web.vod88.top/{folder_encoded}/{num}/"

    page = await browser.new_page(viewport={'width': 1280, 'height': 800})
    try:
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(1500) # 等动画加载
        await page.screenshot(path=output_path, type='jpeg', quality=80)
        print(f"✅ {num} 完成")
    except Exception as e:
        print(f"❌ {num} 失败: {e}")
    finally:
        await page.close()

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        tasks = []
        for i in range(1, 350):
            if len(tasks) >= MAX_CONCURRENT:
                await asyncio.gather(*tasks)
                tasks = []
            tasks.append(screenshot_one(browser, i))
        if tasks:
            await asyncio.gather(*tasks)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
