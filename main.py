from asyncio import tasks
import sys
import requests
import asyncio
import aiohttp
from urllib.parse import urlparse
from crawl import extract_page_data, get_urls_from_html, normalize_url

class AsyncCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).hostname
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = 10
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url in self.page_data:
                return False
            else:
                self.page_data[normalized_url] = {}
                return True

    async def get_html(self, url):
        try:
            async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as response:
                if str(response.status).startswith("4"):
                    raise Exception(f"Client error: {response.status}")
                elif "text/html" not in response.headers.get("Content-Type", ""):
                    raise Exception(f"Content type is not text/html: {response.headers.get('Content-Type', '')}")
                return await response.text()
        except requests.RequestException as e:
            raise Exception(f"Error fetching URL: {e}")

    async def crawl_page(self, current_url):
        if await self.add_page_visit(normalize_url(current_url)) != True:
            return self.page_data
        async with self.semaphore:
            if current_url is None:
                current_url = self.base_url
            #print("base_url:", self.base_url, "current_url:", current_url, "page_data:", self.page_data)
            if urlparse(self.base_url).hostname != urlparse(current_url).hostname:
                return self.page_data
            normalized_url = normalize_url(current_url)
            html = await self.get_html(current_url)
            print(f"Successfully fetched: {current_url}")
        async with self.lock:
            self.page_data[normalized_url] = extract_page_data(html, current_url)
        get_urls = get_urls_from_html(html, current_url)
        tasks = []
        for url in get_urls:
            tasks.append(asyncio.create_task(self.crawl_page(url)))
        await asyncio.gather(*tasks)
        print(f"Crawled {len(self.page_data)} pages from {self.base_url}")
        return self.page_data

    async def crawl(self):
        page_data = await self.crawl_page(self.base_url)
        return page_data
        
async def crawl_site_async(base_url):
    async with AsyncCrawler(base_url) as crawler:
        page_data = await crawler.crawl()
        return page_data

async def main():
    print("Hello from web-scraper!")

    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    else:
        print(f"starting crawl of: {sys.argv[1]}")

    print(await crawl_site_async(sys.argv[1]))

if __name__ == "__main__":
    asyncio.run(main())
