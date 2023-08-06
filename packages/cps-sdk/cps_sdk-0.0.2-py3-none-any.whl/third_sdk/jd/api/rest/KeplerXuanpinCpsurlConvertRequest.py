from third_sdk.jd.api.base import RestApi

class KeplerXuanpinCpsurlConvertRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.pin = None
			self.webId = None
			self.positionId = None
			self.materalId = None

		def getapiname(self):
			return 'jd.kepler.xuanpin.cpsurl.convert'

		def get_version(self):
			return '1.0'
			
	




