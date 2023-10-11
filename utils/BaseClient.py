import httpx
import asyncio
from news_api.config import BASE_HEADERS


class BaseClient(httpx.AsyncClient):

    MAX_CONCURRENT_REQUESTS: int = 10
    BASE_URL: str = ""
    BASE_HEADERS = BASE_HEADERS

    def __init__(self, cookies: str = "", **kwargs):
        super().__init__(**kwargs)
        self.headers = self.BASE_HEADERS
        if cookies:
            self.headers["Cookie"] = cookies

    async def batch_send(self, requests: httpx.Request):
        semaphore = asyncio.Semaphore(self.MAX_CONCURRENT_REQUESTS)

        async def task(request):
            async with semaphore:
                return await self.send(request)

        return await asyncio.gather(*map(task, requests))
