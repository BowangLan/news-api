from __future__ import annotations
from utils.BaseClient import BaseClient
from utils.xpath import *


class ArchiveArticleParser(XPathParser):
    fields = []

    def parse(self, root):
        articles = {}
        for li in root.xpath("//*[@class='basic-list']/li[contains(@class, 'date-heading')]"):
            date = li.xpath("./text()")[0]
            aList = li.xpath("./following-sibling::li[1]/ul/li/a")
            temp = [LinkParser().parse(a) for a in aList]
            articles[date] = temp

        pages = [a for a in root.xpath("//*[@id='sidebar']/ul//li/ul/li/a/@href")]
        return {
            "articles": articles,
            "pages": pages
        }


class LinkParser(XPathParser):
    fields = [
        XpathField(
            "title",
            "./text()",
            single=True,
            func=lambda x: x[0].strip()
        ),
        XpathField(
            "url",
            "./@href",
            single=True
        )
    ]


class SpaceClient(BaseClient):

    BASE_URL = "https://www.space.com"

    async def get_topic_articles(self, url: str):
        res = await self.get(url)
        articles = ArchiveArticleParser().parseHtml(res.text)
        return articles

    async def get_archive_articles_one_page(self, url: str):
        res = await self.get(url)
        articles = ArchiveArticleParser().parseHtml(res.text)
        return articles
