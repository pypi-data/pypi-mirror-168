from third_sdk.jd.api.base import RestApi

class KeplerPushmsgSendBatchMsgRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.param = None

		def getapiname(self):
			return 'jingdong.kepler.pushmsg.sendBatchMsg'

			
	

class Param(object):
		def __init__(self):
			"""
			"""
			self.miniProgramState = None
			self.otherParams = None
			self.appId = None
			self.page = None
			self.bCode = None
			self.data = None
			self.bId = None





