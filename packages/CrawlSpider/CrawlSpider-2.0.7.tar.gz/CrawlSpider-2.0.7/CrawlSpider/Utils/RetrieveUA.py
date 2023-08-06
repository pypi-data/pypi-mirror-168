
from fake_useragent import UserAgent

from CrawlSpider.Utils.Helper import initUaCache


class RetrieveUA:

    ua = None

    @classmethod
    def getRandomUa(cls, **kwargs):
        if not cls.ua:
            cls.init(**kwargs)
        return cls.ua.random

    @classmethod
    def init(cls, **kwargs):
        """
        可以自定义 uaFile文件的路径
        """
        initUaCache(**kwargs)
        cls.ua = UserAgent()



