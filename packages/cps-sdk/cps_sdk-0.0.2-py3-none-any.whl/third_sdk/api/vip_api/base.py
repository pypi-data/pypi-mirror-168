import hmac
import json
import time
import requests
from urllib.parse import urlencode


class VipClient:

    __base_params_name = ['appKey', 'format', 'method', 'service', 'timestamp', 'version']

    __default_headers = {
        "contentType": "application/json"
    }

    def __init__(self, host='https://vop.vipapis.com', appkey='', secret='', timeout=30):
        self.__host = host
        self.__appKey = appkey
        self.__appSecret = secret
        self.__timeout = timeout

    def __get_system_params(self, service='com.vip.adp.api.open.service.UnionGoodsService', version='1.0.0', method='',format='json'):
        """
         获取系统参数
        """
        return {
            'service': service,
            'version': version,
            'method': method,
            'timestamp': int(time.time()),
            'format': format,
            'appKey': self.__appKey
        }

    def get_by_goods_ids_v2(self, **kwargs):
        """
        获取商品详情查询接口
        """
        return self.api_invoke(method='getByGoodsIdsV2', **kwargs)


    def api_invoke(self, method='', **kwargs):
        """
        Api 调用通用方法
        """
        params = self.__get_system_params(method=method)
        req_str = ''
        for key in self.__base_params_name:
            req_str += key + str(params[key])
        req_str += json.dumps(kwargs, ensure_ascii=False)
        m = hmac.new(self.__appSecret.encode(), req_str.encode())
        params['sign'] = m.hexdigest().upper()
        return requests.post(f'{self.__host}?{urlencode(params)}', headers=self.__default_headers, json=kwargs, timeout=self.__timeout)





