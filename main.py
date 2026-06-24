import sys
import asyncio
import aiohttp
from urllib.parse import urlparse
from crawl import extract_page_data, get_urls_from_html, normalize_url
from json_report import write_json_report

class AsyncCrawler:
    def __init__(self, base_url, max_concurrency, max_pages):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).hostname
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None
        self.max_pages = max_pages # Limit the number of pages to crawl
        self.should_stop = False  # Flag to indicate when to stop crawling
        self.all_tasks = set()  # Keep track of all tasks

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            counter = len(self.page_data)
            if self.should_stop:
                return False
            if counter == self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                #for task in self.all_tasks:
                #    task.cancel()
                return False
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
        except asyncio.CancelledError:
            raise
        except Exception as e:
            print(f"Error fetching URL: {e}")
            return None

    async def crawl_page(self, current_url):
        print(f"Carwling page: {current_url}")
        if self.should_stop:
            return
        if urlparse(self.base_url).hostname != urlparse(current_url).hostname:
                return self.page_data
        if await self.add_page_visit(normalize_url(current_url)) != True:
            return self.page_data
        
        async with self.semaphore:
            if current_url is None:
                current_url = self.base_url
            normalized_url = normalize_url(current_url)
            html = await self.get_html(current_url)
            if html is None:
                return
        print(f"Successfully fetched: {current_url}")
        async with self.lock:
            self.page_data[normalized_url] = extract_page_data(html, current_url)
        get_urls = get_urls_from_html(html, current_url)
        tasks = []
        for url in get_urls:
            task = asyncio.create_task(self.crawl_page(url))
            tasks.append(task)
            self.all_tasks.add(task)
        if tasks:
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            finally:
                for task in tasks:
                    self.all_tasks.discard(task)
        print(f"Crawled {len(self.page_data)} pages from {self.base_url}")
        #return self.page_data

    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data
        
async def crawl_site_async(base_url, max_concurrency, max_pages):
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        page_data = await crawler.crawl()
        return page_data

async def main():
    print("Hello from web-scraper!")

    if len(sys.argv) < 4:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)
    else:
        print(f"starting crawl of: {sys.argv[1]}")

    page_data = await crawl_site_async(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    #for page in page_data.values():
    #    print(f"Info about the {page}")
    write_json_report(page_data)

if __name__ == "__main__":
    asyncio.run(main())
