import asyncio
from news_api.platforms.astronomy.client import AstronomyClient
from rich import print


async def main():
    url = "https://www.astronomy.com/science/stars/"
    astronomy_client = AstronomyClient()
    topics = await astronomy_client.get_topic_articles(url)
    print(topics)

if __name__ == '__main__':
    asyncio.run(main())
