from third_sdk.jd.api.base import RestApi

class KeplerPushmsgGetAppConfigTemplateListRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.appid = None
			self.openid = None
			self.maps = None

		def getapiname(self):
			return 'jingdong.kepler.pushmsg.getAppConfigTemplateList'

			
	




