import asyncio
import re

from lxml import etree
from functools import reduce
from CrawlSpider.Utils.SpiderRequest import spiderRequest,webSplash
from CrawlSpider.Utils.Helper import  getRealUrl
from CrawlSpider.Utils.DateUtils import  DateUtils

class BaseNewsSpider:

    def __init__(self, seed, listXPaths=None, detailXPaths=None, **kwargs):
        self.seed = seed
        self.listXPaths = listXPaths or {}
        self.detailXPaths = detailXPaths or {}
        self.kwargs = kwargs
        self.fieldRegExp = {}
        self.initData()


    def initData(self, **kwargs):
        self.listKw = kwargs.get('listKw') or self.kwargs.get('list') or {}
        self.detailKw = kwargs.get('detailKw') or self.kwargs.get('detail') or {}

    def updateListXPath(self, XPaths):
        self.listXPaths.update(XPaths)

    def updateDetailXPath(self, XPaths):
        self.detailXPaths.update(XPaths)

    #  修改  只允许请求为GET或POST
    async def getContent(self, url=None, **kwargs):
        url = url or self.seed
        res = None
        # isAllow302=True, isUsingProxy=False, isSplash=False
        method = ('method' in kwargs and kwargs.pop('method')) or 'GET'

        if method.upper() == 'GET':
            res = await spiderRequest.get(url, **kwargs)
        elif method.upper() == 'POST':
            res = await spiderRequest.post(url, **kwargs)
        # print("res:", res)

        return res['content']

    #  修改  只允许请求为GET或POST
    async def getTree(self, url=None, **kwargs) -> etree._Element:
        tree = None
        encoding = ('encoding' in kwargs and kwargs.pop('encoding')) or 'utf-8'
        res = await self.getContent(url, **kwargs)
        if res:
            result = await self.preProcess(res.decode(encoding=encoding, errors='ignore'))
            tree = etree.HTML(result)
        return tree

    @classmethod
    async def preProcess(cls, htmlStr):
        charList = ['&nbsp;', '&amp;', '&lt;', '&gt;', '&quot;', '&qpos;']
        for charStr in charList:
            if charStr == '&amp;':
                htmlStr = htmlStr.replace(charStr, '&')
            else:
                htmlStr = htmlStr.replace(charStr, '')

        return htmlStr


    async def getList(self, **kwargs):
        """
        [{'url': 'xxxx},{},{}....]
        :return:
        """
        items = []
        parentNodes, XPaths = await self.getParentNodesAndXPaths(self.seed, self.listXPaths, **self.listKw)
        # print("getList:", parentNodes, XPaths)
        if parentNodes:
            for parentNode in parentNodes:
                item = await self.getFields(parentNode, XPaths)
                items.append(item)

        return items

    async def getFields(self, parentNode, XPaths, isList=1):
        item = {}
        for fieldName in XPaths:
            value: dict = XPaths[fieldName]
            fieldMatchExp = value.get('fieldMatchExp')
            fieldValue = []
            vType = value.get('vType')
            typ = 'txtNoTag'
            v = None
            if vType:
                typ, v = vType
            if typ == 're':
                fieldValue = [await self.getFieldByRe(fieldName, fieldMatchExp,v, etree.tostring(parentNode, with_tail=False, encoding='utf-8',
                                                    method='html').decode())]
            else:
                fieldElems = parentNode.xpath(fieldMatchExp) if fieldMatchExp else [parentNode]
                if fieldElems:
                    isList = int(isList)
                    patch = []
                    if isList > len(fieldElems):
                        patch = [None] * (isList - len(fieldElems))
                        isList = -1

                    if isList == 1:
                        fieldElem = fieldElems[0]
                        fieldValue = [self.getFieldValue(fieldElem, typ, v)]
                    elif isList == -1:
                        fieldValue = []
                        for fieldElem in fieldElems:
                            fieldValue.append(self.getFieldValue(fieldElem, typ, v))
                    else:
                        fieldValue = []
                        for i in range(isList):
                            fieldElem = fieldElems[i]
                            fieldValue.append(self.getFieldValue(fieldElem, typ, v))
                    fieldValue.extend(patch)

            if isinstance(fieldValue, list) and len(fieldValue):
                if len(fieldValue) == 1:
                    item.setdefault(fieldName, fieldValue[0])
                else:
                    for i in range(len(fieldValue)):
                        item.setdefault(f"{fieldName}{i+1}", fieldValue[i])

        return item

    def getFieldValue(self, fieldElem, typ, v):
        fieldValue = None
        if typ == 'txtAndTag':
            fieldValue = etree.tostring(fieldElem, with_tail=False, encoding='utf-8',
                                        method='html').decode()
        elif typ == 'txtNoTag':
            fieldValue = fieldElem.xpath('string(.)')
            fieldValue = fieldValue and fieldValue.strip()
        elif typ == 'attr' and v:
            fieldValue = fieldElem.attrib.get(v)
        return fieldValue

    async def getFieldByRe(self, fieldName, regExp, groupNum, content):
        if content:
            try:
                groupNum = int(groupNum) if groupNum else 0
            except:
                groupNum = 0
            expInfo = self.fieldRegExp.get(fieldName)
            if expInfo and expInfo.get('exp') == regExp:
                _regExp = expInfo.get('regExp')
            else:
                _regExp = re.compile(regExp)
                self.fieldRegExp.update({
                    fieldName: {
                        'exp': regExp,
                        'regExp': _regExp
                    }
                })
            result = re.search(_regExp, content)
            return result.group(groupNum)

    async def getParentNodesAndXPaths(self,url, XPaths, **kwargs):
        tree = await self.getTree(url=url, **kwargs)
        if tree is None:
            return None, None
        prefix = XPaths.get('prefix')
        parentNodes = [tree]
        if prefix:
            XPaths = dict([(k, XPaths[k]) for k in XPaths if k != 'prefix'])
            parentNodes = tree.xpath(prefix)
        return parentNodes, XPaths

    async def getParentNodesAndXPathsByContent(self,content, XPaths, **kwargs):
        tree = await self.getTreeByContent(content)
        if tree is None:
            return None, None
        prefix = XPaths.get('prefix')
        parentNodes = [tree]
        if prefix:
            XPaths = dict([(k, XPaths[k]) for k in XPaths if k != 'prefix'])
            parentNodes = tree.xpath(prefix)
        return parentNodes, XPaths

    async def getTreeByContent(self, text:str):
        if text:
            return etree.HTML(text)

    async def getDetail(self, item:dict):
        fieldDic = {}
        print("item:", item)
        url = item.get('url')
        if url:
            detailUrl = await self.getDetailUrl(url)
            if detailUrl != url:
                item['url'] = detailUrl
            self.detailKw.update({'headers':{'Referer': self.seed}})
            parentNodes, XPaths = await self.getParentNodesAndXPaths(detailUrl, self.detailXPaths, **self.detailKw)
            # print("detailKw:", parentNodes, XPaths)
            if parentNodes:
                # isList = False if 'isList' not in self.detailKw else self.detailKw.pop('isList')
                fieldDic = await self.getFields(parentNodes[0], XPaths, isList=self.kwargs.get('isList', 1))
        return fieldDic

    async def getDetailUrl(self, url):
        return getRealUrl(url, self.seed)

    async def transfer(self,fieldDic: dict, **kwargs):
        dateTime = fieldDic.get('publish_time')
        dateTimeFormat = kwargs.get('dateTimeFormat')
        fieldDic.update({
            'publish_time': DateUtils.dateTimeToStr(DateUtils.strToDateTime(dateTime, dateTimeFormat))
        })
        return fieldDic

    async def startSpider(self):
        urlList = await self.getList()
        urlList = self.LinkDeduplication(urlList)
        isSplash = self.detailKw.get('isSplash')
        if isSplash:
            for urlItem in urlList:
                await self.getResult(urlItem)
        else:
            tasks = [asyncio.create_task(self.getResult(urlItem)) for urlItem in urlList]
            await asyncio.gather(*tasks)
        try:
            if webSplash.driver:
                # 关闭浏览器
                webSplash.driver.quit()
        except Exception as e:
            print("e:", e)


    async def startSpiderByThread(self):
        urlList = await self.getList()
        urlList = self.LinkDeduplication(urlList)
        for urlItem in urlList:
            await self.getResult(urlItem)
        try:
            if webSplash.driver:
                webSplash.driver.close()
        except Exception as e:
            print("e:", e)




    def LinkDeduplication(self, itemList):
        run_function = lambda x, y: x if y in x else x + [y]
        d = reduce(run_function, [[]] + itemList)
        return d

    async def getResult(self, urlItem):
        itemDic = await self.getDetail(urlItem)
        if itemDic:
            urlItem.update(itemDic)
            fieldDic = await self.transfer(urlItem)
            combineItem = await self.combineField(fieldDic)
        else:
            combineItem = itemDic
        await self.saveTo(combineItem)


    async def combineField(self,item:dict):
        combineItem = {}
        ks, kMap = self.keyMap()
        isBlank = self.kwargs.get('isBlank', False)
        for k in ks:
            mapKey = kMap.get(k)
            if item.get(k) or isBlank:
                combineItem.setdefault(mapKey or k, item.get(k))
        return combineItem


    def getKMap(self):
        return {
            'url': 'snapshotUrl',
            'content': 'new_content'
        }

    def keyMap(self):
        ks =  "url,title,publish_time,author,content,source".split(',')
        kMap = self.getKMap()
        return ks, kMap

    async def saveTo(self, resultItem):
        pass


