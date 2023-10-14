import httpx
import asyncio
from news_api.config import BASE_HEADERS
from utils.xpath import *
from timeit import default_timer as timer


async def log_request(request: httpx.Request):
    print(f"[{request.method}] {request.url}")


class BaseClient(httpx.AsyncClient):

    MAX_CONCURRENT_REQUESTS: int = 10
    BASE_URL: str = ""
    BASE_HEADERS = BASE_HEADERS

    def __init__(self, cookies: str = "", **kwargs):
        super().__init__(**{
            "event_hooks": {
                "request": [log_request]
            },
            "timeout": 60,
            **kwargs})
        self.headers = self.BASE_HEADERS
        if cookies:
            self.headers["Cookie"] = cookies

    async def batch_send(self, requests: httpx.Request):
        semaphore = asyncio.Semaphore(self.MAX_CONCURRENT_REQUESTS)

        async def task(request):
            async with semaphore:
                return await self.send(request)

        return await asyncio.gather(*map(task, requests))

    async def get_articles_with_pagination(self, initial_url: str, article_parser: XpathField, total_page_parser: XpathField, url_generator: Callable[[int], str]):
        res = await self.get(initial_url)
        articles = article_parser.extract_from_html(res.text)
        total_page = total_page_parser.extract_from_html(res.text)
        start = timer()
        if not total_page:
            return articles
        rest = await self.batch_send([self.build_request('GET', url_generator(i))
                                      for i in range(2, total_page+1)])
        duration = timer() - start
        print(f"Got {len(rest)} pages in {duration:.4f} seconds")
        for r in rest:
            articles += article_parser.extract_from_html(r.text)
        return articles
