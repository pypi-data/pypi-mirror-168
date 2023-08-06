from third_sdk.jd.api.base import RestApi

class KplOpenCouponSearchSkuRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.couponBatchId = None
			self.pageParam = None

		def getapiname(self):
			return 'jd.kpl.open.coupon.search.sku'

		def get_version(self):
			return '1.0'
			
	

class PageParam(object):
		def __init__(self):
			"""
			"""
			self.pageNum = None
			self.pageSize = None





