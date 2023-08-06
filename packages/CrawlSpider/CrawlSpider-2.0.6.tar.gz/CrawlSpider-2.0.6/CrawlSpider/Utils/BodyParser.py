from CrawlSpider.Utils.SpiderRequest import spiderRequest
from bs4 import BeautifulSoup,Tag
def getPlainContent(tag):
    return tag.has_attr('id') and tag['id'] == 'js_content'
def getVideoContent(tag):
    return tag.has_attr('id') and tag['id'] == 'js_content'
class WxGzh:
    @classmethod
    async def plainText(cls, soup:Tag):
        contents = soup.find_all(getPlainContent)
        return contents

    @classmethod
    async def videoText(cls, soup:Tag):
        contents = soup.find_all(getVideoContent)
        return contents



async def test(url):
    res = await spiderRequest.get(url)
    soup = BeautifulSoup(res.decode(), 'lxml')
    contents = await WxGzh.videoText(soup)
    print(contents)






if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    url = "https://mp.weixin.qq.com/s?__biz=MzA5ODgxNDAyMQ==&mid=2654690723&idx=2&sn=3451b209eab2200c534f37fe32820895&chksm=8b442c89bc33a59fd0c58201a9114e7e282d5a08ecbf12d06e64780833b2058ee44de0c214f7&&&sessionid=0&scene=126&clicktime=1627463401&enterid=1627463401"
    s = loop.create_task(test(url))
    loop.run_until_complete(s)






