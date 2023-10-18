from utils.xpath import *
from utils.BaseClient import BaseClient
from rich import print


class SingleTopicParser(XPathParser):

    fields = [
        XpathField(
            "name",
            './/h4/a/text()',
            single=True,
        ),
        XpathField(
            "url",
            './/h4/a/@href',
            single=True,
        ),
        XpathField(
            "description",
            './/p[1]/text()',
            single=True
        )
    ]


class RootTopicParser(XPathParser):

    fields = [
        XpathField(
            "topics",
            "//h2[contains(text(), 'category')]/../div/div/div",
            func=lambda x: [SingleTopicParser().parse(e)
                            for e in x]
        )
    ]


class SubTopicParser(XPathParser):

    fields = [
        XpathField(
            "topics",
            "//h2[contains(text(), 'Topics')]/../div/div/div/div",
            func=lambda x: [SingleTopicParser().parse(e)
                            for e in x]
        )
    ]


class ArticleParser(XPathParser):

    fields = [
        XpathField(
            "title",
            './div/h3/a/text()',
            single=True
        ),
        XpathField(
            "types",
            './div/div/div/a/text()'
        ),
        XpathField(
            "url",
            './a[1]/@href',
            single=True
        ),
        XpathField(
            "img",
            './a[1]/img/@src',
            single=True
        )
    ]


class AstronomyClient(BaseClient):

    BASE_URL = "https://www.astronomy.com"

    async def get_topics(self):
        url = self.BASE_URL + "/news/"
        res = await self.get(url)
        topics = RootTopicParser().parseHtml(res.text)['topics']
        print(topics)
        print([t['url'] for t in topics])
        topics_requests = [self.build_request('GET', topic["url"])
                           for topic in topics]
        topics_res = await self.batch_send(topics_requests)
        sub_topics = [SubTopicParser().parseHtml(res.text)['topics']
                      for res in topics_res]
        for i in range(len(topics)):
            topics[i]["sub_topics"] = sub_topics[i]
        return topics

    async def get_topic_articles(self, url: str):
        return await self.get_articles_with_pagination(
            url,
            XpathField(
                "articles",
                '//*[@id="main"]/article/div/div[2]/div//article',
                func=lambda x: [ArticleParser().parse(e)
                                for e in x]
            ),
            XpathField(
                "total_page",
                '//a[@class="page-numbers"][last()]/text()',
                func=lambda x: int(x[0]) if x else 0,
                single=True
            ),
            lambda i: url + f"page/{i}/"
        )
