from third_sdk.jd.api.base import RestApi

class KeplerPushmsgCreateSubSendTaskRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.param = None

		def getapiname(self):
			return 'jingdong.kepler.pushmsg.createSubSendTask'

			
	

class Param(object):
		def __init__(self):
			"""
			"""
			self.appId = None
			self.contentData = None
			self.businessCode = None
			self.otherParamsData = None
			self.sendTime = None
			self.sendType = None
			self.jumpPage = None
			self.businessId = None
			self.miniprogramState = None
			self.channel = None
			self.taskName = None





