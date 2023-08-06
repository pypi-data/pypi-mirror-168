from third_sdk.jd.api.base import RestApi

class KeplerSettledAftermarketQueryservicedetailRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.queryServiceDetailParam = None
			self.client = None

		def getapiname(self):
			return 'jd.kepler.settled.aftermarket.queryservicedetail'

		def get_version(self):
			return '1.0'
			
	

class OperatorInfoParam(object):
		def __init__(self):
			"""
			"""
			self.operatorPin = None
			self.operatorName = None
			self.operatorRemark = None
			self.operatorDate = None


class QueryServiceDetailParam(object):
		def __init__(self):
			"""
			"""
			self.afsServiceId = None
			self.buId = None
			self.operatorInfoParam = None


class Client(object):
		def __init__(self):
			"""
			"""
			self.uid = None
			self.userIp = None





