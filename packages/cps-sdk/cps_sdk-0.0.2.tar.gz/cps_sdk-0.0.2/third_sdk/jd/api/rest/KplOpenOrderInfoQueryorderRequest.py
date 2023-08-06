from third_sdk.jd.api.base import RestApi

class KplOpenOrderInfoQueryorderRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.var1 = None

		def getapiname(self):
			return 'jd.kpl.open.order.info.queryorder'

		def get_version(self):
			return '1.0'
			
	

class Var1(object):
		def __init__(self):
			"""
			"""
			self.unionId = None
			self.childUnionId = None
			self.optType = None
			self.time = None
			self.pageNo = None
			self.pageSize = None





