from third_sdk.jd.api.base import RestApi

class KplOpenAlphaGetconfigurewithloginRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.baseInfo = None

		def getapiname(self):
			return 'jd.kpl.open.alpha.getconfigurewithlogin'

		def get_version(self):
			return '1.0'
			
	

class BaseInfo(object):
		def __init__(self):
			"""
			"""
			self.app_key = None
			self.pin_key = None
			self.device_id = None
			self.mac_address = None
			self.sn = None
			self.version = None
			self.os_type = None
			self.app_version = None
			self.timestamp = None
			self.skill = None
			self.command = None
			self.source_type = None
			self.extend = None
			self.client_ip = None





