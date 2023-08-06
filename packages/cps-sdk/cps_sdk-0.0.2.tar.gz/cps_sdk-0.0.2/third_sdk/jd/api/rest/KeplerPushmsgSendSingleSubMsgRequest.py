from third_sdk.jd.api.base import RestApi

class KeplerPushmsgSendSingleSubMsgRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.param = None

		def getapiname(self):
			return 'jingdong.kepler.pushmsg.sendSingleSubMsg'

			
	

class Param(object):
		def __init__(self):
			"""
			"""
			self.miniProgramState = None
			self.otherParams = None
			self.appId = None
			self.page = None
			self.pin = None
			self.businessCode = None
			self.data = None
			self.businessId = None
			self.openId = None





