from third_sdk.jd.api.base import RestApi

class KplOpenAftermarketRefundRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.afsRefundDetailDto = None
			self.client = None

		def getapiname(self):
			return 'jd.kpl.open.aftermarket.refund'

		def get_version(self):
			return '1.0'
			
	

class AfsRefundDetailDto(object):
		def __init__(self):
			"""
			"""
			self.orderId = None
			self.afsServiceId = None
			self.datatype = None
			self.page = None
			self.pagesize = None


class Client(object):
		def __init__(self):
			"""
			"""
			self.uid = None
			self.userIp = None





