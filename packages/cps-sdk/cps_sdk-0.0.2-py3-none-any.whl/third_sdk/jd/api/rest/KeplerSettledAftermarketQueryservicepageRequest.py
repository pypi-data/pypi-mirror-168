from third_sdk.jd.api.base import RestApi

class KeplerSettledAftermarketQueryservicepageRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.queryServicePageParam = None
			self.client = None

		def getapiname(self):
			return 'jd.kepler.settled.aftermarket.queryservicepage'

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


class QueryServicePageParam(object):
		def __init__(self):
			"""
			"""
			self.afsServiceId = None
			self.buId = None
			self.orderId = None
			self.wareId = None
			self.afsApplyTimeBegin = None
			self.afsApplyTimeEnd = None
			self.approvedDateBegin = None
			self.approvedDateEnd = None
			self.trackPin = None
			self.customerPin = None
			self.customerName = None
			self.customerTel = None
			self.orderType = None
			self.newOrderId = None
			self.expressCode = None
			self.afsServiceStep = None
			self.pageSize = None
			self.pageIndex = None
			self.operatorInfoParam = None


class Client(object):
		def __init__(self):
			"""
			"""
			self.uid = None
			self.userIp = None





