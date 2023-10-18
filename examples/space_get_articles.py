import asyncio
from news_api.platforms.space.client import SpaceClient
from rich import print


async def main():
    url = "https://www.space.com/news/archive/2023/09"
    client = SpaceClient()
    data = await client.get_archive_articles_one_page(url)
    print(data)

if __name__ == '__main__':
    asyncio.run(main())
