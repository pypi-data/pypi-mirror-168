from third_sdk.jd.api.base import RestApi

class KplOpenPromotionPidurlconvertRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.webId = None
			self.positionId = None
			self.materalId = None
			self.pid = None
			self.subUnionId = None
			self.shortUrl = None
			self.kplClick = None

		def getapiname(self):
			return 'jd.kpl.open.promotion.pidurlconvert'

		def get_version(self):
			return '1.0'
			
	




