from third_sdk.jd.api.base import RestApi

class WirelessWarePriceGetRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.sku_ids = None
			self.origin = None

		def getapiname(self):
			return 'jingdong.wireless.ware.price.get'

			





