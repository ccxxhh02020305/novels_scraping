import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import random
import os


async def playwright_open_chromium():
    p = await async_playwright().start()
    browser = await p.chromium.launch(
        headless=True,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-web-security',
            '--disable-dev-shm-usage'
        ]
    )

    context = await browser.new_context(
        viewport= {'width':2560, 'height':1440},  # type: ignore
        user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    )

    await context.set_extra_http_headers({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })


    return p,browser,context

async def push_url(context, url):
    page = await context.new_page()


    try:
        print("正在打开页面")
        await page.goto(url, wait_until='networkidle', timeout=60000)

        if await page.query_selector('text="Just a moment..."'):
            print("Cloudflare出现")

            await page.wait_for_selector('text="Just a moment..."', state='hidden', timeout=30000)
            print("Cloudflare已解决")

        await page.wait_for_load_state('networkidle')

        for _ in range(3):
            scroll_height = await page.evaluate("document.body.scrollHeight")
            scroll_to = random.randint(100, scroll_height // 2)
            await page.evaluate(f"window.scrollTo(0, {scroll_to})")
            await asyncio.sleep(random.uniform(0.5, 2))

        content = await page.content()


    except Exception as e:
        print(f"发生错误: {e}")
        await page.screenshot(path='cloudflare_error.png')
        return None

    finally:
        await page.close()

    return content


def parse_novel_content(html_content):
    if not html_content:
        return None

    soup = BeautifulSoup(html_content, 'html.parser')

    if soup.find('title') and 'Just a moment' in soup.find('title').text:
        print("仍然在Cloudflare页面")
        return None

    title = soup.find('h1')
    if title:
        title = title.get_text().strip()
        print(f"小说标题: {title}")
    else:
        print("未找到标题")
        title = "未知标题"

    alist = soup.find_all('a', href=True)
    number = []
    for a in alist:
        href = a.get('href')
        parts = href.rsplit("/", 2)
        if len(parts) > 2:
            number.append(parts[2])
    return number

def novel_text_content(novel_content):
    if not novel_content:
        return None

    soup = BeautifulSoup(novel_content, 'html.parser')

    if soup.find('title') and 'Just a moment' in soup.find('title').text:
        print("仍然在Cloudflare页面")
        return None

    title = soup.find('h1')
    if title:
        title = title.get_text().strip()
        print(f"小说标题: {title}")
    else:
        print("未找到标题")
        title = "未知标题"

    div_text = soup.find('div', id='content')
    text = []
    for p_tag in div_text.find_all('p'):
        p_text = p_tag.get_text().strip()
        text.append(p_text)

    full_text = "\n\n".join(text)
    return full_text, title


async def main():
    novel_url = "https://www.beqege.cc/65200/"

    print("正在创建浏览器实例")
    p,browser,context = await playwright_open_chromium()

    father_page = await push_url(context, novel_url)
    if father_page:
        print("页面内容获取成功")
        chapters_number = parse_novel_content(father_page)
        chapters_url = []
        for i in chapters_number:
            if '.html' not in i:
                continue
            chapters_url.append(novel_url + i)
    else:
        print("获取页面内容失败")

    for url in chapters_url:
        print("正在创建浏览器页面")
        novel_content = await push_url(context, url)
        if novel_content:
            print("页面内容获取成功")
            novel_text, novel_title = novel_text_content(novel_content)
        else:
            print(f"{url}提取失败")
        await asyncio.sleep(random.randint(1,5))
        save_path = os.path.join(r"E:\小说", f"{novel_title}.txt")
        with open(save_path, mode="w", encoding="utf-8") as f:
            f.write(novel_text)
            print(f"{novel_title}下载完成")

    await browser.close()
    await p.stop()
    return novel_content


if __name__ == "__main__":
    success = asyncio.run(main())
    if success:
        print("爬取成功")
    else:
        print("爬取失败")
