# CrawlSpider

**CrawlSpider** is a simple, yet light, spider library.


```python
import asyncio
from CrawlSpider.Utils.SpiderRequest import spiderRequest

async def get(url):
    res = await spiderRequest.get(
        url,
        form='json'
    )
    print(res)

if __name__ == '__main__':
    asyncio.run(get("https://httpbin.org/get"))
```

响应结果
```json
{
    "status_code": 200,
    "content": {
        "args": {},
        "headers": {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Cookie": "_hjAbsoluteSessionInProgress=0; _sp_id.eeee=d332c9c-a67e-4564-80ed-114737664d84",
            "Host": "httpbin.org",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
            "X-Amzn-Trace-Id": "Root=1-62c6edbe-3de25d31339352e"
        },
        "origin": "xxx.xxx.xxx.xxx",
        "url": "https://httpbin.org/get"
    }
}
```

CrawlSpider allows you to crawl data from website extremely easily.
There’s no need to manually change proxy and request's headers in crawling data




## Installing CrawlSpider and Supported Versions

Requests is available on PyPI:

```console
$ python -m pip install CrawlSpider
```

CrawlSpider officially supports Python 3.7+.
    
    
    
    
    
    
    