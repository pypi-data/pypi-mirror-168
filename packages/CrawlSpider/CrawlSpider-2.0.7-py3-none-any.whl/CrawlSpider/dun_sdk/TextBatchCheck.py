# -*- coding: utf-8 -*-
# __author__ : Ricky
# __createTime__ : 2022/4/18 2:55
# __fileName__ : XueshuSpider DunSDK.py
# __devIDE__ : PyCharm
import hashlib
import time
import random
import requests
import json


class TextCheckAPI(object):
    """文本批量在线检测接口示例代码"""

    API_URL = "http://as.dun.163.com/v5/text/batch-check"
    VERSION = "v5.2"

    def __init__(self, secret_id, secret_key, business_id):
        """
        Args:
            secret_id (str) 产品密钥ID，产品标识
            secret_key (str) 产品私有密钥，服务端生成签名信息使用
            business_id (str) 业务ID，易盾根据产品业务特点分配
        """
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.business_id = business_id



    def gen_signature(self, params=None):
        """生成签名信息
           Args:
               secretKey 产品私钥
               params 接口请求参数，不包括signature参数
       """
        params_str = ""
        for k in sorted(params.keys()):
            params_str += str(k) + str(params[k])
        params_str += self.secret_key
        return hashlib.md5(params_str.encode()).hexdigest()

    def check(self, params):
        """请求易盾接口
        Args:
            params (object) 请求参数
        Returns:
            请求结果，json格式
        """
        params["secretId"] = self.secret_id
        params["businessId"] = self.business_id
        params["version"] = self.VERSION
        params["timestamp"] = int(time.time() * 1000)
        params["nonce"] = int(random.random() * 100000000)
        # params["signatureMethod"] = "SM3"  # 签名方法，默认MD5，支持SM3
        params["signature"] = self.gen_signature(params)

        try:
            res = requests.post(self.API_URL, data=params).json()
            return res
        except Exception as ex:
            print("调用API接口失败:", str(ex))


if __name__ == "__main__":
    """示例代码入口"""
    businessId = '6ad86b847de443ce36c7fae4854e61a0'
    secretId = '1389d67989cbdd09acd236d173dda841'
    secretKey = '3b8e223c4b27d021b85174a3d2a6fd0e'
    api = TextCheckAPI(secretId, secretKey, businessId)

    # 私有请求参数
    texts: list = []
    text1 = {
        "dataId": "ebfcad1c-dba1-490c-b4de-e784c2691768",
        "content": "易盾批量检测接口！v5接口!",
    }
    text2 = {
        "dataId": "ebfcad1c-dba1-490c-b4de-e784c2691678",
        "content": "易盾批量检测接口！v5接口!",
    }
    texts.append(text1)
    texts.append(text2)
    params = {
        "texts": json.dumps(texts),
        # "checkLabels": "200, 500"  # 指定过检分类
    }

    ret = api.check(params)

    code: int = ret["code"]
    msg: str = ret["msg"]
    if code == 200:
        resultArray: list = ret["result"]
        if resultArray is not None and len(resultArray) > 0:
            for result in resultArray:
                dataId: str = result["dataId"]
                taskId: str = result["taskId"]
                action: int = result["action"]
                status: int = result["status"]
                print("dataId=%s，批量文本提交返回taskId:%s" % (dataId, taskId))
                if status == 0:
                    labelArray: list = result["labels"]
                    for labelItem in labelArray:
                        label: int = labelItem["label"]
                        level: int = labelItem["level"]
                        details: dict = labelItem["details"]
                        hintArray: list = details["hint"]
                        subLabels: list = labelItem["subLabels"]
                    if action == 0:
                        print("taskId: %s, 文本机器检测结果: 通过" % taskId)
                    elif action == 1:
                        print("taskId: %s, 文本机器检测结果: 嫌疑, 需人工复审, 分类信息如下: %s" % (taskId, labelArray))
                    elif action == 2:
                        print("taskId=%s, 文本机器检测结果: 不通过, 分类信息如下: %s" % (taskId, labelArray))
                else:
                    print("提交失败")
    else:
        print("ERROR: code=%s, msg=%s" % (ret["code"], ret["msg"]))