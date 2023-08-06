from third_sdk.jd.api.base import RestApi

class KplOpenXuanpinSearchgoodsRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.queryParam = None
			self.pageParam = None
			self.orderField = None

		def getapiname(self):
			return 'jd.kpl.open.xuanpin.searchgoods'

		def get_version(self):
			return '1.0'
			
	

class QueryParam(object):
		def __init__(self):
			"""
			"""
			self.keywords = None
			self.skuId = None


class PageParam(object):
		def __init__(self):
			"""
			"""
			self.pageNum = None
			self.pageSize = None





