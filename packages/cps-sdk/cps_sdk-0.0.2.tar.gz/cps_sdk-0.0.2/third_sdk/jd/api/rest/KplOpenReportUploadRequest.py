from third_sdk.jd.api.base import RestApi

class KplOpenReportUploadRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.dataJson = None

		def getapiname(self):
			return 'jd.kpl.open.report.upload'

		def get_version(self):
			return '1.0'
			
	




