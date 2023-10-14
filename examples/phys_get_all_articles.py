import asyncio
from news_api.platforms.phys.client import PhysClient
from rich import print


async def main():
    url = "https://phys.org/space-news/astronomy/sort/date/all/"
    client = PhysClient()
    articles = await client.get_topic_articles(url)
    print(len(articles))

if __name__ == '__main__':
    asyncio.run(main())
