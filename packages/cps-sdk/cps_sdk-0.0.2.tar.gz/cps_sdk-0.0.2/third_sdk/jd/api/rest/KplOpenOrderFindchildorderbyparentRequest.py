from third_sdk.jd.api.base import RestApi

class KplOpenOrderFindchildorderbyparentRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.orderId = None

		def getapiname(self):
			return 'jd.kpl.open.order.findchildorderbyparent'

		def get_version(self):
			return '1.0'
			
	




