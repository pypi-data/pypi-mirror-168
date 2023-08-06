from third_sdk.jd.api.base import RestApi

class KplOpenBatchConvertCpslinkRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.KeplerUrlparam = None

		def getapiname(self):
			return 'jd.kpl.open.batch.convert.cpslink'

		def get_version(self):
			return '1.0'
			
	

class KeplerUrlparam(object):
		def __init__(self):
			"""
			"""
			self.urls = None
			self.type = None
			self.appKey = None
			self.subUnionId = None
			self.jdShortUrl = None





