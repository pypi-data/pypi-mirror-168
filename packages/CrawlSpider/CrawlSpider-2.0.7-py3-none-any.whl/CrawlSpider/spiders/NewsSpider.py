
from CrawlSpider.spiders.BaseNewsSpider import BaseNewsSpider
from CrawlSpider.ETL.BaseETL import baseETL


class NewsSpider(BaseNewsSpider):
    async def saveTo(self, resultItem:dict):
        raise NotImplemented('`saveTo` for NewSpider is not implemented')

    def keyMap(self):
        ks = "url,title,publish_time,author,content,source,originalContent".split(',')
        kMap = self.getKMap()
        return ks, kMap

    async def transfer(self,fieldDic: dict, **kwargs):
        new_content = fieldDic.get('content') or fieldDic.get('body')
        data = {
            'new_content': new_content,
            'url': fieldDic.get('url')
        }
        result = await baseETL.bodyTransfer(data)
        content = result.get('new_content')
        originalContent = content
        if self.isDelTagsExceptImg():
            content = await baseETL.delTagsExceptImg(content)
        fieldDic.update({
            'content': content,
            'originalContent': originalContent
        })
        return await super().transfer(fieldDic, **kwargs)


    def isDelTagsExceptImg(self):
        return True
















