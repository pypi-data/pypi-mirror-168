from third_sdk.jd.api.base import RestApi

class KeplerPushmsgSaveBatchSubBehaviourRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.param = None

		def getapiname(self):
			return 'jingdong.kepler.pushmsg.saveBatchSubBehaviour'

			
	

class BusinessBehaviourJsfDto(object):
		def __init__(self):
			"""
			"""
			self.templateId = None
			self.behaviour = None
			self.businessCode = None
			self.businessId = None


class Param(object):
		def __init__(self):
			"""
			"""
			self.pin = None
			self.appid = None
			self.openid = None
			self.behaviourJsfDtoList = None





