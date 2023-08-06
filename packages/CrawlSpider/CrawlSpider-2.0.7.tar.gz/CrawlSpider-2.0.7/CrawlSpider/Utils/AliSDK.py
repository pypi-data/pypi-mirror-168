# -*- coding: utf-8 -*-
# __author__ : Ricky
# __createTime__ : 2022/2/24 下午2:49
# __fileName__ : spiderAssistant AliSDK.py
# __devIDE__ : PyCharm
import uuid
from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
import json
from aliyunsdkcore.request import RoaRequest
from aliyunsdkcore.http import format_type
from aliyunsdkgreen.endpoint import endpoint_data


class TextAsyncScanRequest(RoaRequest):

    def __init__(self):
        RoaRequest.__init__(self, 'Green', '2018-05-09', 'TextAsyncScan', 'green')
        self.set_uri_pattern('/green/text/scan')
        self.set_method('POST')
        if hasattr(self, "endpoint_map"):
            setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
        if hasattr(self, "endpoint_regional"):
            setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())

    def get_ClientInfo(self):
        return self.get_query_params().get('ClientInfo')

    def set_ClientInfo(self, ClientInfo):
        self.add_query_param('ClientInfo', ClientInfo)


class AliClient:
    def __init__(
        self,
        ak=None,
        secret=None,
        region_id="cn-hangzhou",
        **kwargs
    ):
        self.clt = client.AcsClient(ak, secret, region_id, **kwargs)
        self.region_id = region_id


    def TextReview(self, tasks: list, bizType='default', product_name='Green', end_point='green.cn-shanghai.aliyuncs.com'):

        region_provider.modify_point(product_name, self.region_id, end_point=end_point)
        request = TextAsyncScanRequest()
        request.set_accept_format('JSON')
        request.set_headers({
            'Content-Type': format_type.APPLICATION_JSON
        })

        request.set_body_params(
            {
                "scenes": ["antispam"],
                "bizType": bizType,
                "tasks": tasks
            }
        )


        try:
            response = self.clt.do_action_with_exception(request)
            return response
        except Exception as err:
            return err.__str__()





if __name__ == '__main__':
    ali = AliClient()
    response = ali.TextReview([
        {
            'dataId': str(uuid.uuid4()),
            'content': 'marketing strategy and planning in the uk pharmaceutical industry some preliminary findings стратегия маркетинга и планирования в британской фармацевтической промышленности некоторые предварительные результаты'
        }

    ]).decode()

    response = json.loads(response)
    response['data'][0].pop('content')
    print(response)
