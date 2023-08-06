from third_sdk.jd.api.base import RestApi

class KplOpenRankInfoGatherServiceRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.clientParam = None
			self.rankParam = None

		def getapiname(self):
			return 'jingdong.kpl.open.RankInfoGatherService'

			
	

class ClientParam(object):
		def __init__(self):
			"""
			"""
			self.channel = None
			self.source = None


class RankParam(object):
		def __init__(self):
			"""
			"""
			self.rankType = None
			self.ids = None
			self.params = None





