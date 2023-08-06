
import aiofiles
from urllib.parse import urlparse
from urllib3 import encode_multipart_formdata
from typing import AnyStr,List
from CrawlSpider.Utils.SpiderRequest import spiderRequest
from CrawlSpider.Utils.Helper import md5_text
from CrawlSpider.cos_sdk.TencentCloud.CosOp import CosOp


class FileUpload:

    def __init__(self, cosConf, cosOp=None):
        self.cosOp = cosOp or CosOp(cosConf)



    async def uploadFilesToOss(self, fileList:List[AnyStr]):
        fileDic = {}
        for file in fileList:
            async with aiofiles.open(file, 'rb') as fr:
                f = await fr.read()
            data = await self.uploadFileToOss(file, f)
            fileDic.setdefault(file, data)
        return fileDic

    async def uploadFileToOss(self, fileName,fileData:bytes, ContentMD5=None, **kwargs):
        if not fileData:
            res = {
                'fileName': fileName,
                'url': ""
            }
        else:
            res = self.cosOp._uploadFile(fileName, fileData, ContentMD5=ContentMD5, **kwargs)
        print("res:", res)
        return res

    async def _uploadFileToOss(self, fileName,fileData:bytes, ossUploadApi=""):
        data = {
            'file': (fileName, fileData)
        }
        if fileData:
            encode_data = encode_multipart_formdata(data)
            print(encode_data[1])
            res = await spiderRequest.post(ossUploadApi, headers={'Content-Type': encode_data[1]},
              data=encode_data[0], form="json", verify_ssl=False)
            print("res", res)
        else:
            res = None

        if res:
            return res['data']
        else:
            return {
                "fileName": fileName,
                "url": None
            }

    async def uploadFileFromNetToOss(self, url):
        parseResult = urlparse(url)
        # 这里可能有问题，后续再优化
        ext = parseResult.query.lstrip('wx_fmt=')
        uniqueFlag = parseResult.path.split('/')[-2]
        fileName = f"{uniqueFlag}.{ext}"
        print(f"当前图片名称为:{fileName}")
        res = await spiderRequest.get(url)
        data = await self.uploadFileToOss(fileName, res)
        return data

    async def uploadFileFromNetToOssCommon(self, url, fileName=None):
        fileName = fileName or md5_text(url)+'.jpeg'
        print(f"当前图片名称为:{fileName}")
        res = await spiderRequest.get(url)
        data = await self.uploadFileToOss(fileName, res)
        return data



if __name__ == '__main__':
    import asyncio
    fileUpload = FileUpload({})
    loop = asyncio.get_event_loop()
    url = "https://mmbiz.qpic.cn/mmbiz_jpg/rCOKPvQb9vvN0c0ttdLIta9f73N0MRibNWhiaGqhWcufjKpJ51qn5Uqcjic0Js9p25SkezkG45caFoNia6Jmr6cJhg/640?wx_fmt=jpeg"
    s = loop.create_task(fileUpload.uploadFileFromNetToOss(url))
    loop.run_until_complete(s)


