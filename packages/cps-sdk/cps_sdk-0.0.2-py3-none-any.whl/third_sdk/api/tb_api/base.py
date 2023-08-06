from third_sdk import top


class TbClient:

    def __init__(self, host='http://gw.api.taobao.com/router/rest', port=80, appkey='', secret='', timeout=30):
        self.__host = host
        self.__port = port
        self.__appkey = appkey
        self.__secret = secret
        self.__timeout = timeout

    def taobao_tbk_dg_material_optional(self, req: top.api.TbkDgMaterialOptionalRequest = None, access_token=None, **kwargs):
        """
        物料搜索
        """
        if req is None:
            req = top.api.TbkDgMaterialOptionalRequest(self.__host, self.__port)
        return self.api_invoke(req, access_token, **kwargs)

    def taobao_tbk_dg_item_info_get(self, req: top.api.TbkItemInfoGetRequest = None, access_token=None, **kwargs):
        """
        商品详情查询(简版)
        """
        if req is None:
            req = top.api.TbkItemInfoGetRequest(self.__host, self.__port)
        return self.api_invoke(req, access_token, **kwargs)

    def api_invoke(self, req: top.api.base.RestApi, access_token=None, **kwargs):
        """
        api 调用通用方法
        """
        assert req is not None
        req.set_app_info(top.appinfo(self.__appkey, self.__secret))
        for k, v in kwargs.items():
            setattr(req, k, v)
        return req.getResponse(authrize=access_token, timeout=self.__timeout)