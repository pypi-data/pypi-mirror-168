from third_sdk.jd.api.base import RestApi

class KeplerTradeSubmitRequest(RestApi):
		def __init__(self,domain='gw.api.360buy.com',port=80):
			"""
			"""
			RestApi.__init__(self,domain, port)
			self.cartReq = None
			self.orderParam = None

		def getapiname(self):
			return 'jd.kepler.trade.submit'

		def get_version(self):
			return '1.0'
			
	

class User(object):
		def __init__(self):
			"""
			"""
			self.pin = None
			self.level = None
			self.flagInfo = None


class GiftSkuReq(object):
		def __init__(self):
			"""
			"""
			self.sku = None
			self.num = None


class SkuExtentionReq(object):
		def __init__(self):
			"""
			"""
			self.thirdCategoryId = None
			self.vendor = None
			self.vendorType = None


class SkuReq(object):
		def __init__(self):
			"""
			"""
			self.sku = None
			self.num = None
			self.name = None
			self.tagList = None
			self.selectedPromoIdList = None
			self.thirdCategoryId = None
			self.vendor = None
			self.vendorType = None
			self.giftSkuRequestList = None
			self.skuExtentionReq = None


class SuitMainSkuReq(object):
		def __init__(self):
			"""
			"""
			self.sku = None
			self.num = None
			self.thirdCategoryId = None
			self.vendor = None
			self.vendorType = None
			self.tagList = None
			self.selectedPromoIdList = None
			self.giftSkuRequestList = None


class SuitReq(object):
		def __init__(self):
			"""
			"""
			self.promotionId = None
			self.num = None
			self.skuList = None
			self.vskuId = None
			self.virtualSuitType = None


class SelectedPromotionGiftsReq(object):
		def __init__(self):
			"""
			"""
			self.promotionId = None
			self.promotionType = None
			self.giftSkuReqList = None


class CartReq(object):
		def __init__(self):
			"""
			"""
			self.ip = None
			self.areaId = None
			self.user = None
			self.skuList = None
			self.suitList = None
			self.giftList = None
			self.selectedPromotionGiftsReqList = None


class OrderUnionParam(object):
		def __init__(self):
			"""
			"""
			self.unpl = None
			self.unionId = None
			self.unionSiteId = None
			self.unionUserName = None
			self.unionTime = None
			self.unionEx = None
			self.mt_xid = None
			self.mt_subsite = None
			self.mt_ext = None
			self.dmpjs = None


class Address(object):
		def __init__(self):
			"""
			"""
			self.addressId = None
			self.addressType = None
			self.name = None
			self.provinceId = None
			self.cityId = None
			self.countyId = None
			self.townId = None
			self.provinceName = None
			self.cityName = None
			self.countyName = None
			self.townName = None
			self.addressDetail = None
			self.postCode = None
			self.mobile = None
			self.phone = None
			self.email = None
			self.orgId = None
			self.longitude = None
			self.latitude = None
			self.coord_type = None
			self.addressDefault = None
			self.addressName = None
			self.paymentId = None
			self.pickId = None
			self.pickName = None


class CombinationPayment(object):
		def __init__(self):
			"""
			"""
			self.mainPaymentType = None
			self.subPaymentType = None


class InvoiceConsignee(object):
		def __init__(self):
			"""
			"""
			self.consigneeName = None
			self.provinceId = None
			self.province = None
			self.cityId = None
			self.city = None
			self.countyId = None
			self.county = None
			self.townId = None
			self.town = None
			self.phone = None
			self.address = None


class VatInvoice(object):
		def __init__(self):
			"""
			"""
			self.companyName = None
			self.code = None
			self.regAddr = None
			self.regPhone = None
			self.regBank = None
			self.regBankAccount = None
			self.normalInvoiceContent = None
			self.bookInvoiceContent = None
			self.invoiceConsignee = None


class NormalInvoice(object):
		def __init__(self):
			"""
			"""
			self.selectedInvoiceTitle = None
			self.companyName = None
			self.normalInvoiceContent = None
			self.bookInvoiceContent = None
			self.invoiceConsignee = None
			self.code = None


class ElectroInvoice(object):
		def __init__(self):
			"""
			"""
			self.selectInvoiceTitle = None
			self.selectBookInvoiceContent = None
			self.selectNormalInvoiceContent = None
			self.invoiceConsigneeEmail = None
			self.invoiceConsigneePhone = None
			self.compayName = None
			self.code = None


class Invoice(object):
		def __init__(self):
			"""
			"""
			self.selectInvoiceType = None
			self.invoicePutType = None
			self.vatInvoice = None
			self.normalInvoice = None
			self.electroInvoice = None


class GeneralFreight(object):
		def __init__(self):
			"""
			"""
			self.freight = None
			self.verderId = None


class RemoteRegionFreightParam(object):
		def __init__(self):
			"""
			"""
			self.skuId = None
			self.num = None
			self.freight = None
			self.venderId = None


class Freight(object):
		def __init__(self):
			"""
			"""
			self.generalFreight = None
			self.remoteRegionFreightList = None


class ClientInfo(object):
		def __init__(self):
			"""
			"""
			self.serverName = None
			self.userIP = None
			self.countKey = None
			self.netBuySourceType = None
			self.invokeInvoiceBasicService = None
			self.originId = None


class OrderFrom(object):
		def __init__(self):
			"""
			"""
			self.webOriginId = None
			self.flowId = None
			self.siteId = None
			self.originId = None
			self.easybuy = None
			self.locBuy = None
			self.giftbuy = None
			self.lipinkaPhysical = None
			self.contractMachine = None
			self.whiteBar = None
			self.resetDefaultAddress = None
			self.resetResevsion = None
			self.flowType = None
			self.factoryShopId = None
			self.factoryRegionId = None
			self.presale = None
			self.invokeNewCouponInterface = None
			self.resetFlag = None


class OrderParam(object):
		def __init__(self):
			"""
			"""
			self.orderUnionParam = None
			self.payPassword = None
			self.checkcodeTxt = None
			self.checkCodeAnswer = None
			self.trackID = None
			self.userAgent = None
			self.remark = None
			self.sopNotPutInvoice = None
			self.presaleMobile = None
			self.presalePayType = None
			self.giftBuyHidePrice = None
			self.checkCodeRid = None
			self.paymentId = None
			self.orderGuid = None
			self.address = None
			self.combinationPayment = None
			self.invoice = None
			self.freight = None
			self.orderNeedMoney = None
			self.orderNeedMoneyStr = None
			self.clientInfo = None
			self.orderFrom = None
			self.clientPin = None
			self.serverName = None
			self.userIP = None
			self.countKey = None
			self.userKey = None
			self.requestPath = None
			self.repAbsPathPrex = None
			self.fullName = None
			self.gendan = None





