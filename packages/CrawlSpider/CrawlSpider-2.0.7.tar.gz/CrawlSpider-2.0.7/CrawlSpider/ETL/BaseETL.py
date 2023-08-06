
from CrawlSpider.Utils.ResHandler import ImgSrcReplace

class BaseETL:

    @classmethod
    async def bodyTransfer(cls, data):
        """
        测试body的图片和链接的置换
        """
        body = data.get('new_content')
        imgHint = "未做转换"
        if body:
            imgFileScope = data.get('imgFileScope')
            if not imgFileScope:
                url = data.get('url')
                print(url)
                if url:
                    imgFileScope = url.rstrip(url.split('/')[-1])
            body, imgHint = await ImgSrcReplace.common(body, imgFileScope=imgFileScope)
        return {
            'status': 0,
            'new_content': body,
            'imgHint': imgHint
        }

    @classmethod
    async def delTagsExceptImg(cls, htmlStr: str = None, soup=None, imgAttr='src'):
        # 这里不需要，因为已经做过前置处理了 preProcess
        # htmlStr = cls.cleanWebChars(htmlStr)
        res = await ImgSrcReplace.delTagsExceptImg(htmlStr, soup, imgAttr)
        return res

    @classmethod
    async def cleanWebChars(cls, htmlStr):
        charList = ['&nbsp;', '&amp;', '&lt;', '&gt;', '&quot;', '&qpos;']
        for charStr in charList:
            if charStr == '&amp;':
                htmlStr = htmlStr.replace(charStr, '&')
            else:
                htmlStr = htmlStr.replace(charStr, '')

        return htmlStr



baseETL = BaseETL()






