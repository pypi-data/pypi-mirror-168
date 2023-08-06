from third_sdk.jd.api.base import RestApi

class KplOpenTradeMasterUsecouponRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.client = None
			self.couponKey = None

		def getapiname(self):
			return 'jd.kpl.open.trade.master.usecoupon'

		def get_version(self):
			return '1.0'
			
	

class Client(object):
		def __init__(self):
			"""
			"""
			self.uid = None
			self.userIp = None
			self.clientFlow = None
			self.logId = None





