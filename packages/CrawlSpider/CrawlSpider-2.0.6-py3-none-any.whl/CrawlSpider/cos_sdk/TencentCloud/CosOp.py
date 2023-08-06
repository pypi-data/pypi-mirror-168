import os

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from uuid import uuid4
import sys
import logging
from CrawlSpider.conf.settings import logger

import imghdr


logging.basicConfig(level=logger['level'], stream=sys.stdout)




class CosOp:
    IMG_MAX_SIZE = 5 * 1024 * 1024
    IMG_THUMBNAIL_SIZE = 200 * 1024

    def __init__(self, cosConf):
        secret_id = cosConf['secretId']  # 替换为用户的 secretId(登录访问管理控制台获取)
        secret_key = cosConf['secretKey']  # 替换为用户的 secretKey(登录访问管理控制台获取)
        region = cosConf['regionId']  # 替换为用户的 Region
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
        # 2. 获取客户端对象
        self.client:CosS3Client = CosS3Client(config)
        self.cosConf = cosConf

    def getInfo(self, fileName:str, Content:bytes, rule=None):

        flag, msg = self.isImage(top32Bit=Content[:32])
        suffix = fileName.split('.')[-1] if not flag else msg
        uid = uuid4().hex
        Key = f"{self.cosConf['fileDirName']}/{uid}.{suffix}"
        Url = f"{self.cosConf['baseUrl']}/{Key}"
        print("flag, msg:", flag, msg)
        thumbnailKey = None
        PicOperations = ''
        length = len(Content)
        print("length:", length/1024)
        if flag and length > self.IMG_THUMBNAIL_SIZE:
            thumbnailKey = f"{uid}-tt.{suffix}"
            Key = f"{self.cosConf['fileDirName']}/{uid}-o.{suffix}"
            Url = f"{self.cosConf['baseUrl']}/{self.cosConf['fileDirName']}/{thumbnailKey}"
            scale = self.getCompressSize(length=length)
            v = rule or f"imageMogr2/thumbnail/!{scale}p"
            PicOperations = '{"is_pic_info":1,"rules":[{"fileid":"%s","rule":"%s", "bucket":"%s"}]}' % (thumbnailKey, v, self.cosConf['bucketName'])
        return dict(
            url=Url,
            key=Key,
            thumbnailKey=thumbnailKey,
            PicOperations=PicOperations
        )

    def getCompressSize(self, length):
        return str(int(round(self.IMG_THUMBNAIL_SIZE/length, 2)*100+15))




    def _uploadFile(self, FileName, Content:bytes, ContentMD5 = None, **kwargs):
        # PicOperations={"is_pic_info":1,"rules":[{"fileid":"format.jpg","rule":"imageView2/format/png"}]}
        # imageMogr2/thumbnail/!".concat(scale.toString()).concat("p")
        # newFileName.concat("-tt").concat(".").concat(suffixName)
        ret = {}
        if len(Content) > self.IMG_MAX_SIZE:
            return {
                'fileName': FileName,
                'url': "",
                'msg': '图片大于5M'
            }
        # ContentMD5 md5字符串
        if ContentMD5:
            kwargs['ContentMD5'] = ContentMD5
        rule = 'rule' in kwargs and kwargs.pop('rule')
        info = self.getInfo(FileName, Content, rule=rule)
        """
        url=Url,
        key=Key,
        thumbnailKey=thumbnailKey,
        PicOperations=PicOperations
        """
        Key = info.get('key')
        url = info.get('url')

        if info.get('PicOperations'):
            res = self.client.ci_put_object(self.cosConf['bucketName'], Body=Content,Key=Key,PicOperations=info['PicOperations'],**kwargs)
        else:
            res = self.client.put_object(self.cosConf['bucketName'], Body=Content,Key=Key,**kwargs)
        print("返回结果:", res)
        if isinstance(res, tuple):
            res = res[0]
        if not res.get('ETag'):
            url = ""
        res = {
            'fileName': FileName,
            'url': url
        }
        return res

    def uploadFile(self, FilePath:str, ContentMD5 = None, **kwargs):
        with open(FilePath, 'rb') as f:
            Content = f.read()

        FileName = FilePath.split('/')[-1]

        res = self._uploadFile(FileName, Content, ContentMD5=ContentMD5, **kwargs)
        print("res:", res)
        return res



    @classmethod
    def isImage(cls, filePath=None, top32Bit:bytes=None):
        if not filePath and not top32Bit:
            return False, '参数不能都为空'
        if not top32Bit and os.path.exists(filePath):
            with open(filePath, 'rb') as f:
                top32Bit = f.read(32)
        try:
            res = imghdr.what(filePath, top32Bit)
        except FileNotFoundError as e:
            return False, e.strerror
        if res:
            return True, res
        else:
            return False,'不是图片'


if __name__ == '__main__':
    # PicOperations='{"is_pic_info":1,"rules":[{"fileid":"format.jpg","rule":"imageView2/format/png"}]}'
    # imageMogr2/format/webp
    cosOp = CosOp({})
    cosOp.uploadFile('./test.jfif', rule='imageMogr2/format/webp')