from third_sdk.jd.api.base import RestApi

class KplOpenCpsConvertKeplerurlRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.request = None

		def getapiname(self):
			return 'jd.kpl.open.cps.convert.keplerurl'

		def get_version(self):
			return '1.0'
			
	

class Request(object):
		def __init__(self):
			"""
			"""
			self.sourceEmt = None
			self.unionId = None
			self.webId = None
			self.skuList = None
			self.appKey = None
			self.type = None
			self.subUnionId = None





