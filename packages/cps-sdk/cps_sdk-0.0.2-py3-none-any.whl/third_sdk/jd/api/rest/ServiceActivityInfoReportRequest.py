from third_sdk.jd.api.base import RestApi

class ServiceActivityInfoReportRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.timeStamp = None
			self.wxAppId = None
			self.pluginAppId = None
			self.activityIdentification = None
			self.activityDescription = None
			self.serviceIdentification = None
			self.wxNickname = None
			self.token = None
			self.wxOpenId = None
			self.pluginOpenId = None
			self.type = None
			self.prizeType = None
			self.rewardDescription = None
			self.typeDescription = None
			self.count = None
			self.resultStatus = None
			self.testData = None

		def getapiname(self):
			return 'jingdong.service.activity.info.report'

			





