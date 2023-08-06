import asyncio
import copy
import json
import datetime
import requests 


from urllib.parse import urlparse
from CrawlSpider.Utils.SplashHandler import webSplash



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}



class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8', 'ignore')
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)



class SpiderRequestSync:
    def getSync(self,url, form="content", **kwargs):
        _headers: dict = (kwargs.get('headers') and kwargs.pop('headers')) or {}
        _headers.update(headers)
        kwargs.get('chrome_options') and kwargs.pop('chrome_options')
        proxyUrl = (kwargs.get('proxy') and kwargs.pop('proxy')) or ""
        if proxyUrl:
            res = urlparse(proxyUrl)
            proxies = {
                res.scheme: res.netloc
            }
            kwargs['proxies'] = proxies
        resp = requests.get(url, headers=_headers, **kwargs)
        r = None

        if resp and resp.ok:  # 注意这里是status，不是status_code
            if form == 'json':
                r = resp.json()
            elif form == 'text':
                r = resp.text
            elif form == 'content':
                r = resp.content
        return r


    def postSync(self, url, form="content", **kwargs):
        _headers: dict = (kwargs.get('headers') and kwargs.pop('headers')) or {}
        _headers.update(headers)
        kwargs.get('chrome_options') and kwargs.pop('chrome_options')
        proxyUrl = (kwargs.get('proxy') and kwargs.pop('proxy')) or ""
        if proxyUrl:
            res = urlparse(proxyUrl)
            proxies = {
                res.scheme: res.netloc
            }
            kwargs['proxies'] = proxies
        resp =  requests.post(url, headers=_headers, **kwargs)
        r = None
        if resp.ok:  # 注意这里是status，不是status_code
            if form == 'json':
                r = resp.json()
            elif form == 'text':
                r = resp.text
            elif form == 'content':
                r = resp.content
        return r

    def get(self, url, isAllow302=True, isUsingProxy=False, isSplash=False, **kwargs):
        if isUsingProxy:
            ret = self.proxy(self.get_, url, isAllow302=isAllow302, isSplash=isSplash,isAsync=True, **kwargs)
        else:
            ret = self.get_(url, isAllow302=isAllow302, isSplash=isSplash,**kwargs)
        return ret

    def get_(self, url, isAllow302=True,  isSplash=False,isAsync=True, **kwargs):
        if isSplash:
            return self.splash(url, **kwargs)
        elif not isAsync:
            return self.getSync(url, **kwargs)

    @classmethod
    def splash(cls,url, **kwargs):
        loop = asyncio.get_running_loop()
        # --proxy-server=socks5://xxx.xxx:xxx
        options = kwargs.get('chrome_options')
        splashTime = kwargs.get('splashTime') or 0.2
        isUsingNewDriver = kwargs.get('isUsingNewDriver')
        driver = None
        if isUsingNewDriver:
            driver = webSplash.getNewDriver(options)
        elif options:
            driver = webSplash.getDriver(options=options)
        future = loop.run_in_executor(None, webSplash.getSource, url, driver, splashTime)
        return future

    @classmethod
    def splashSync(cls, url, **kwargs):
        options = kwargs.get('chrome_options')
        splashTime = kwargs.get('splashTime') or 0.2
        isUsingNewDriver = kwargs.get('isUsingNewDriver')
        driver = None
        if isUsingNewDriver:
            driver = webSplash.getNewDriver(options)
        elif options:
            driver = webSplash.getDriver(options=options)
        return webSplash.getSource(url, driver, splashTime)


    @classmethod
    def proxy(cls,fn, url, isAllow302=True,  isSplash=False, **kwargs):
        from CrawlSpider.Utils.RetrieveProxy import RetrieveProxy
        _kwargs = copy.deepcopy(kwargs)
        isFree = True
        if 'isFree' in _kwargs:
            isFree = _kwargs.pop('isFree')
        if isFree:
            retry = 3
            proxy = RetrieveProxy.getProxyFree()
            print("获取到的免费代理IP:", proxy)
            # proxies requests {}
            httpProxy = f"http://{proxy}"
            _kwargs.update({
                'proxy': httpProxy,
                'chrome_options': [f'--proxy-server={httpProxy}']
            })
            while retry:
                try:
                    ret = fn(url, isAllow302=isAllow302, isSplash=isSplash, **_kwargs)
                    return ret
                except Exception as e:
                    print("e", e)
                    retry -= 1
            ret = RetrieveProxy.delete(proxy)
            print("删除结果:", ret)
        zhiMaProxy = RetrieveProxy.getProxyByZhiMa()
        if zhiMaProxy:
            print("获取到的收费代理IP:", zhiMaProxy)
            ret = RetrieveProxy.addProxy({
                'source': "zhiMa",
                'proxy': zhiMaProxy
            })
            print("添加结果:", ret)
            httpProxy = f"http://{zhiMaProxy}"
            _kwargs.update({
                'proxy': httpProxy,
                'chrome_options': [f'--proxy-server={httpProxy}']
            })
            try:
                ret = fn(url, isAllow302=isAllow302, isSplash=isSplash, **_kwargs)
                return ret
            except Exception as e:
                print("e", e)
                return None


    def post(self, url, isAllow302=True, isUsingProxy=False, isSplash=False,**kwargs):
        if isUsingProxy:
            ret = self.proxy(self.post_, url, isAllow302=isAllow302, isSplash=isSplash, **kwargs)
        else:
            ret = self.post_(url, isAllow302=isAllow302, isSplash=isSplash, **kwargs)

        return ret

    def post_(self, url, isAllow302=True, isSplash=False,isAsync=True,**kwargs):
        ret = self.postSync(url,  **kwargs)
        return ret

    @classmethod
    def toJson(cls, data,**kwargs):
        return json.dumps(data, ensure_ascii=False, cls=MyEncoder, **kwargs)
    @classmethod
    def fromJson(cls, data, encoding='utf-8', **kwargs):
        return json.loads(data, encoding=encoding, **kwargs)


spiderRequest = SpiderRequestSync()
