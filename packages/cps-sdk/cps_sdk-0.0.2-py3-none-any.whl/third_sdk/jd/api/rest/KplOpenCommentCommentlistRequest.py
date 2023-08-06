from third_sdk.jd.api.base import RestApi

class KplOpenCommentCommentlistRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.param = None

		def getapiname(self):
			return 'jd.kpl.open.comment.commentlist'

		def get_version(self):
			return '1.0'
			
	

class Param(object):
		def __init__(self):
			"""
			"""
			self.productId = None
			self.score = None
			self.sortType = None
			self.pageIndex = None
			self.pageSize = None
			self.logId = None





