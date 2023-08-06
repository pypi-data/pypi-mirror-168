from third_sdk.jd.api.base import RestApi

class KplOpenRegularPlanQueryplancountRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.planParam = None

		def getapiname(self):
			return 'jd.kpl.open.regular.plan.queryplancount'

		def get_version(self):
			return '1.0'
			
	

class PlanParam(object):
		def __init__(self):
			"""
			"""
			self.venderId = None
			self.planNumber = None
			self.payMode = None
			self.skuId = None
			self.planStartTime = None
			self.planEndTime = None





