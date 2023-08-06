from third_sdk.jd.api.base import RestApi

class KeplerSettledAftermarketGetbackmodeRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.orderId = None
			self.wareId = None
			self.backAddr = None
			self.client = None

		def getapiname(self):
			return 'jd.kepler.settled.aftermarket.getbackmode'

		def get_version(self):
			return '1.0'
			
	

class BackAddr(object):
		def __init__(self):
			"""
			"""
			self.expect = None
			self.province = None
			self.city = None
			self.county = None
			self.village = None
			self.detailAddress = None


class Client(object):
		def __init__(self):
			"""
			"""
			self.uid = None
			self.userIp = None





