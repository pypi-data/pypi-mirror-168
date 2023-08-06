from third_sdk.jd.api.base import RestApi

class KplOpenTradeGetorderrefundRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.orderId = None
			self.client = None

		def getapiname(self):
			return 'jd.kpl.open.trade.getorderrefund'

		def get_version(self):
			return '1.0'
			
	

class Client(object):
		def __init__(self):
			"""
			"""
			self.uid = None
			self.userId = None





