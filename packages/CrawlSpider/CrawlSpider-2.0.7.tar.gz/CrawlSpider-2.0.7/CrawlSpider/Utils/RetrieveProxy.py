import asyncio
from CrawlSpider.conf.settings import aBuYunCurrIp, aBuYunSwitchIp
from CrawlSpider.Utils.SpiderRequest import spiderRequest
from retrying import retry

class RetrieveProxy:
    proxyApi = None
    zhiMaDaiLi = None
    proxyHost = None
    proxyPort = None
    proxyUser = None
    proxyPass = None

    @classmethod
    def initProxyConf(cls, **kwargs):
        for k in kwargs:
            v = kwargs.get(k)
            setattr(cls, k, v)

    @classmethod
    async def getProxyFree(cls):

        proxyObj = await spiderRequest.get(cls.proxyApi+'/get/', form='json')
        proxy = proxyObj.get('proxy')
        return proxy, proxy


    @staticmethod
    async def getAbuYunIp():
        proxyMeta, proxies = await RetrieveProxy.getProxyByAbuYun()
        txt = await spiderRequest.get(aBuYunCurrIp, form='text', proxy=proxyMeta)
        return txt.split(',')[0]

    @staticmethod
    async def switchAbuYunIp():
        proxyMeta, proxies = await RetrieveProxy.getProxyByAbuYun()
        res = await spiderRequest.get(aBuYunSwitchIp, form='text', proxy=proxyMeta)

        txt = res.get('content')
        print(f"proxy:{txt}")
        # await asyncio.sleep(0.1)
        return txt and txt.split(',')[0] or None

    @classmethod
    async def getProxyByZhiMa(cls):

        res = await spiderRequest.get(cls.zhiMaDaiLi, form='text')

        jsonData = spiderRequest.fromJson(res.get('content') or '{}')
        ret = None
        if jsonData['code'] == 0:
            data = jsonData.get('data')
            print(data)
            if data:
                item = data[0]
                ip = item['ip']
                port = item['port']
                proxy = '%s:%s' % (ip, port)
                print(proxy)
                ret = proxy
        return ret, ret

    @staticmethod
    async def getProxy(proxyType):
        if proxyType == 'ZhiMa':
            return await RetrieveProxy.getProxyByZhiMa()
        elif proxyType == 'AbuYun':
            return await RetrieveProxy.getProxyByAbuYun()


    @classmethod
    @retry(stop_max_attempt_number=5, wait_fixed=500)
    async def getProxyByAbuYun(cls):
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": cls.proxyHost,
            "port": cls.proxyPort,
            "user": cls.proxyUser,
            "pass": cls.proxyPass,
        }
        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        print(f"proxies:{proxies}")

        return proxyMeta, proxies

    @classmethod
    async def addProxy(cls, data):
        res = await spiderRequest.post(cls.proxyApi + '/put/', data=data, form='json')
        return res

    @classmethod
    async def delete(cls, p):
        res = await spiderRequest.get(cls.proxyApi+"/delete/?proxy={}".format(p), form='text')
        return res


async def main():
    proxy = await RetrieveProxy.getProxyFree()
    print("获取到的免费代理IP:", proxy)


if __name__ == '__main__':
    asyncio.run(main())
