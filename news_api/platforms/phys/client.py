from utils.BaseClient import BaseClient
from utils.xpath import *


class ArticleParser(XPathParser):

    fields = [
        XpathField(
            'title',
            './/h3/a/text()',
            single=True
        ),
        XpathField(
            'url',
            './/h3/a/@href',
            single=True
        ),
        XpathField(
            'description',
            './/p/text()',
            func=lambda x: x[0].strip(),
            single=True
        ),
        XpathField(
            'img',
            './/figure/a/img/@src',
            single=True
        ),
        XpathField(
            "release_time",
            './div[2]/div[2]/p/text()',
            func=lambda x: x[0].strip(),
            single=True
        )
    ]


class PhysClient(BaseClient):

    BASE_URL = "https://phys.org"

    # async def get_topics(self):
    #     url = self.BASE_URL + "/news/"
    #     res = await self.get(url)
    #     topics = RootTopicParser().parseHtml(res.text)['topics']
    #     print(topics)
    #     print([t['url'] for t in topics])
    #     topics_requests = [self.build_request('GET', topic["url"])
    #                        for topic in topics]
    #     topics_res = await self.batch_send(topics_requests)
    #     sub_topics = [SubTopicParser().parseHtml(res.text)['topics']
    #                   for res in topics_res]
    #     for i in range(len(topics)):
    #         topics[i]["sub_topics"] = sub_topics[i]
    #     return topics

    async def get_topic_articles(self, url: str):
        return await self.get_articles_with_pagination(
            url,
            XpathField(
                "articles",
                '/html/body/main/div/div[1]/div/div[2]/div/div/article',
                func=lambda x: [ArticleParser().parse(e)
                                for e in x]
            ),
            XpathField(
                "total_page",
                '/html/body/main/div/div[2]/div/div/div/span/text()',
                func=lambda x: int(x[0]) if x else 0,
                single=True
            ),
            lambda i: url + f"page{i}.html"
        )
