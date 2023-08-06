from third_sdk.jd.api.base import RestApi

class KplOpenWfpVscPreviewRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.interfaceName = None
			self.methodName = None
			self.param = None

		def getapiname(self):
			return 'jd.kpl.open.wfp.vsc.preview'

		def get_version(self):
			return '1.0'
			
	

class Data(object):
		def __init__(self):
			"""
			"""
			self.cardNum = None
			self.pwd = None


class Param(object):
		def __init__(self):
			"""
			"""
			self.merchantCode = None
			self.appCode = None
			self.token = None
			self.source = None
			self.businessType = None
			self.data = None
			self.operator = None
			self.clientIp = None
			self.clientPort = None
			self.trackerId = None





