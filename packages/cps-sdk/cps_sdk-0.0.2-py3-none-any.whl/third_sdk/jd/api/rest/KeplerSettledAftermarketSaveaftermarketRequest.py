from third_sdk.jd.api.base import RestApi

class KeplerSettledAftermarketSaveaftermarketRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.afsApplyDto = None
			self.client = None

		def getapiname(self):
			return 'jd.kepler.settled.aftermarket.saveaftermarket'

		def get_version(self):
			return '1.0'
			
	

class CustomerDto(object):
		def __init__(self):
			"""
			"""
			self.customerPin = None
			self.customerName = None
			self.customerContactName = None
			self.customerTel = None
			self.customerMobilePhone = None
			self.customerEmail = None
			self.customerPostcode = None
			self.customerGrade = None


class PickwareDto(object):
		def __init__(self):
			"""
			"""
			self.pickwareType = None
			self.pickwareProvince = None
			self.pickwareCity = None
			self.pickwareCounty = None
			self.pickwareVillage = None
			self.doorPickReserveType = None
			self.pickwareAddress = None
			self.reserveDateStr = None
			self.reserveDateBegin = None
			self.reserveDateEnd = None


class ReturnwareDto(object):
		def __init__(self):
			"""
			"""
			self.returnwareType = None
			self.returnwareProvince = None
			self.returnwareCity = None
			self.returnwareCounty = None
			self.returnwareVillage = None
			self.returnwareAddress = None


class RefundDto(object):
		def __init__(self):
			"""
			"""
			self.bankCode = None
			self.bankName = None
			self.bankProvince = None
			self.bankCity = None
			self.branchBankAddress = None
			self.bankAccountHolder = None
			self.refundType = None


class AfsApplyDetailDto(object):
		def __init__(self):
			"""
			"""
			self.wareName = None
			self.wareBrand = None
			self.wareDescribe = None
			self.wareId = None
			self.wareNum = None
			self.afsDetailType = None
			self.payPrice = None
			self.expandTag = None


class AfsApplyDto(object):
		def __init__(self):
			"""
			"""
			self.platformSrc = None
			self.orderId = None
			self.orderType = None
			self.customerExpect = None
			self.changeSku = None
			self.questionTypeCid1 = None
			self.questionTypeCid2 = None
			self.questionDesc = None
			self.isNeedDetectionReport = None
			self.questionPic = None
			self.isHasPackage = None
			self.packageDesc = None
			self.createName = None
			self.isHasInvoice = None
			self.invoiceCode = None
			self.invoiceTime = None
			self.customerDto = None
			self.pickwareDto = None
			self.returnwareDto = None
			self.refundDto = None
			self.afsApplyDetailDtos = None
			self.applyIdYhd = None


class Client(object):
		def __init__(self):
			"""
			"""
			self.uid = None
			self.userIp = None





