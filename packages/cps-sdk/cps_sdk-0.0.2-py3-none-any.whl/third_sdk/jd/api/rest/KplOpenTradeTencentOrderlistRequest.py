from third_sdk.jd.api.base import RestApi

class KplOpenTradeTencentOrderlistRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.client = None
			self.orderListReq = None

		def getapiname(self):
			return 'jd.kpl.open.trade.tencent.orderlist'

		def get_version(self):
			return '1.0'
			
	

class Client(object):
		def __init__(self):
			"""
			"""
			self.clientFlow = None
			self.uid = None
			self.userIp = None
			self.logId = None


class OrderListReq(object):
		def __init__(self):
			"""
			"""
			self.size = None
			self.page = None
			self.state = None
			self.startDate = None
			self.endDate = None





