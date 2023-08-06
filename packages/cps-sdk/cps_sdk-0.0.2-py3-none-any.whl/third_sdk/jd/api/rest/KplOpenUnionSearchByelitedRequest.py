from third_sdk.jd.api.base import RestApi

class KplOpenUnionSearchByelitedRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.unionSearchParam = None

		def getapiname(self):
			return 'jd.kpl.open.union.search.byelited'

		def get_version(self):
			return '1.0'
			
	

class UnionSearchParam(object):
		def __init__(self):
			"""
			"""
			self.eliteId = None
			self.pageIndex = None
			self.pageSize = None
			self.sortName = None
			self.sortType = None





