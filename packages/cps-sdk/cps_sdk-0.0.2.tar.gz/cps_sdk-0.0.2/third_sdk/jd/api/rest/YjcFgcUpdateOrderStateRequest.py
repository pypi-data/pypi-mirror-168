from third_sdk.jd.api.base import RestApi

class YjcFgcUpdateOrderStateRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.orderId = None

		def getapiname(self):
			return 'jingdong.yjc.fgc.updateOrderState'

			





