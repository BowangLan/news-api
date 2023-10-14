import lxml.html
from typing import *


class XpathField():
    def __init__(self, name, xpath, func=None, single: bool = False):
        self.name = name
        self.xpath = xpath
        self.func = func
        self.single = single

    def extract(self, element):
        t = element.xpath(self.xpath)
        if self.func:
            return self.func(t)
        elif self.single:
            if len(t) == 0:
                return None
            return t[0]
        return t

    def extract_from_html(self, html: str):
        root = lxml.html.fromstring(html)
        return self.extract(root)


class XPathParser(object):

    fields: List[XpathField]

    def parse(self, root: lxml.html.Element):
        result = {}
        for field in self.fields:
            result[field.name] = field.extract(root)
        return result

    def parseHtml(self, html: str):
        root = lxml.html.fromstring(html)
        return self.parse(root)
