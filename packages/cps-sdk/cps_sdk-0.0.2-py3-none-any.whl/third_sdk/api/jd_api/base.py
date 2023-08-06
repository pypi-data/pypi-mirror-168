from third_sdk.jd.api.rest.UnionOpenGoodsQueryRequest import UnionOpenGoodsQueryRequest
from third_sdk.jd.api.base import RestApi
from third_sdk.jd import appinfo

class JdClient:

    def __init__(self, host='https://api.jd.com/routerjson', port=80, appkey='', secret='', timeout=30):
        self.__host = host
        self.__port = port
        self.__appkey = appkey
        self.__secret = secret
        self.__timeout = timeout

    def jd_union_open_goods_query(self, req: UnionOpenGoodsQueryRequest = None, access_token=None,
                                  **kwargs):
        if req is None:
            req = UnionOpenGoodsQueryRequest(self.__host, self.__port)
        return self.api_invoke(req, access_token, **kwargs)

    def api_invoke(self, req: RestApi, access_token=None, **kwargs):
        assert req is not None
        req.set_app_info(appinfo(self.__appkey, self.__secret))
        for k, v in kwargs.items():
            setattr(req, k, v)
        return req.getResponse(access_token=access_token, timeout=self.__timeout)
