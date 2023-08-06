from third_sdk.jd.api.base import RestApi

class KplOpenPromiseDosConfigRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.req = None

		def getapiname(self):
			return 'jd.kpl.open.promise.dos.config'

		def get_version(self):
			return '1.0'
			
	

class SkuProperty(object):
		def __init__(self):
			"""
			"""
			self.sku = None
			self.venderType = None
			self.storeProperty = None
			self.skuMark = None


class Req(object):
		def __init__(self):
			"""
			"""
			self.source = None
			self.provinceId = None
			self.cityId = None
			self.countyId = None
			self.townId = None
			self.skuProperties = None





