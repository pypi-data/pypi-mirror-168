import hashlib
import time
from urllib.parse import urlencode
import requests


class PddClient:
    """
    拼多多api sdk
    """

    def __init__(self, host="https://gw-api.pinduoduo.com/api/router",
                 appkey='',
                 secert='',
                 timeout=30):
        self.__host = host
        self.__client_id = appkey
        self.__client_secert = secert
        self.__data_type = "JSON"
        self.__timeout = timeout

    @staticmethod
    def __sign_md5(params):
        """
        对拼接好的字符串进行md5签名
        """
        hl = hashlib.md5()
        hl.update(params.encode(encoding='utf-8'))
        return hl.hexdigest().upper()

    @staticmethod
    def __set_real_params(api_type, params={}):
        params['type'] = api_type
        params['timestamp'] = f"{time.time()}".split(".")[0]

    def __set_sys_params(self, params={}):
        params['client_id'] = self.__client_id
        params['data_type'] = self.__data_type

    def __splice_str(self, params={}):
        """
        升序排序请求参数，连接字符串，并在首尾加上client_secret
        """

        reverse_list = sorted([(k, str(v)) for k, v in params.items()], key=lambda x: x[0])
        reverse_list.insert(0, ("", self.__client_secert))
        reverse_list.append(("", self.__client_secert))
        reverse_list_str = list(map(lambda x: "".join(x), reverse_list))
        result = "".join(reverse_list_str)
        return result, params

    def __urlencode_data(self, params, pdd_dict):
        pdd_dict["sign"] = PddClient.__sign_md5(params)
        result = urlencode(pdd_dict)
        url = f"{self.__host}?{result}"
        return url

    def pdd_ddk_goods_detail(self, **kwargs):
        """
        多多客商品详情查询接口
        """
        return self.api_invoke("pdd.ddk.goods.detail", **kwargs)

    def pdd_ddk_goods_search(self, **kwargs):
        """
        多多客搜索接口
        """
        return self.api_invoke("pdd.ddk.goods.search", **kwargs)

    def pdd_goods_cats_get(self, **kwargs):
        """
        商品类目查询接口
        """
        return self.api_invoke("pdd.goods.cats.get", **kwargs)

    def pdd_goods_opt_get(self, **kwargs):
        return self.api_invoke("pdd.goods.opt.get", **kwargs)

    def api_invoke(self, api_type, **kwargs):
        """
        Api 调用通用方法
        """
        headers = {
            "accept": "application/json"
        }
        params = {}
        # 实时参数
        PddClient.__set_real_params(api_type, params)
        # 系统参数
        self.__set_sys_params(params)
        # 业务参数
        params.update(kwargs)

        params, pdd_dict = self.__splice_str(params)
        url = self.__urlencode_data(params, pdd_dict)
        return requests.post(url=url, headers=headers, timeout=self.__timeout)
