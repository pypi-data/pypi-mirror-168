from third_sdk.jd.api.base import RestApi

class KeplerXuanpinSearchSkuRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.queryParam = None
			self.pageParam = None
			self.orderField = None

		def getapiname(self):
			return 'jd.kepler.xuanpin.search.sku'

		def get_version(self):
			return '1.0'
			
	

class QueryParam(object):
		def __init__(self):
			"""
			"""
			self.keywords = None
			self.cids1 = None
			self.cids2 = None
			self.cids3 = None
			self.sellerType = None
			self.minPrice = None
			self.maxPrice = None


class PageParam(object):
		def __init__(self):
			"""
			"""
			self.pageNum = None
			self.pageSize = None





