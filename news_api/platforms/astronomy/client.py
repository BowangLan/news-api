import httpx
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
