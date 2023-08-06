from third_sdk.jd.api.base import RestApi

class KeplerOrderCancelorderRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.cancelOrderReq = None
			self.client = None

		def getapiname(self):
			return 'jd.kepler.order.cancelorder'

		def get_version(self):
			return '1.0'
			
	

class CancelOrderReq(object):
		def __init__(self):
			"""
			"""
			self.orderId = None
			self.applyDate = None
			self.applyPin = None
			self.applyName = None


class Client(object):
		def __init__(self):
			"""
			"""
			self.uid = None
			self.userIp = None





