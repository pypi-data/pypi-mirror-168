# -*- coding: utf-8 -*-
# __author__ : Ricky
# __createTime__ : 2022/7/7 17:53
# __fileName__ : XueshuSpider console_scripts.py
# __devIDE__ : PyCharm
import fire
from CrawlSpider.Utils.SpiderRequest import spiderRequest
from CrawlSpider.Utils.SplashHandler import webSplash
from CrawlSpider.spiders.BaseNewsSpider import BaseNewsSpider
try:
    from CrawlSpider.Utils.twineUtils import build as projectBuild
except:
    pass

class Command:

    @staticmethod
    async def get(*args, url="https://httpbin.org/get", **kwargs):
        """
        isUsingProxy 是否使用代理
        proxy        使用哪个代理
        isSplash     是否动态渲染，这里使用的是 selenium
        form         数据返回的形式，json(字典), text(文本), content(二进制流), origin(即表示原请求对象)
        """
        chromedriverPath = 'chromedriverPath' in kwargs and kwargs.pop('chromedriverPath')
        version = 'version' in kwargs and kwargs.pop('version')
        webSplash.initDriver(chromedriverPath=chromedriverPath, version=version, **kwargs)
        res = await spiderRequest.get(
            url,
            *args,
            **kwargs
        )
        print(f"res:{res}")

    @staticmethod
    async def post(*args, url="https://httpbin.org/post", **kwargs):
        """
       isUsingProxy 是否使用代理
       proxy        使用哪个代理
       form         数据返回的形式，json(字典), text(文本), content(二进制流), origin(即表示原请求对象)
       """

        res = await spiderRequest.get(
            url,
            *args,
            **kwargs
        )
        print(f"res:{res}")

    @staticmethod
    async def spider(*args, url="https://httpbin.org/get",**kwargs):
        """
       isUsingProxy 是否使用代理
       proxy        使用哪个代理
       form         数据返回的形式，json(字典), text(文本), content(二进制流), origin(即表示原请求对象)
       """
        chromedriverPath = 'chromedriverPath' in kwargs and kwargs.pop('chromedriverPath')
        version = 'version' in kwargs and kwargs.pop('version')
        method = 'method' in kwargs and kwargs.pop("method") or 'getList'
        webSplash.initDriver(chromedriverPath=chromedriverPath, version=version, **kwargs)

        spider = BaseNewsSpider(*args, seed=url, *kwargs)
        res = await getattr(spider, method)(**kwargs)
        print(f"res:{res}")
    @staticmethod
    async def build(*args, **kwargs):
        """
        打包项目,基于twine库的使用
        is_publish 是否发布，默认false只打包不上传到pypi
        version    版本号，不填默认为原项目下__version__.py文件中的__version__
        distDir    构建包所在目录，不填则为运行此命令的项目根路径下的dist目录
        **kwargs   即为 twine 所需参数，比如 username, password等
        """
        projectBuild(*args, **kwargs)



def main():
    fire.Fire({
        'build': Command.build,
        'get': Command.get,
        'post': Command.post,
        'spider': Command.spider
    })
