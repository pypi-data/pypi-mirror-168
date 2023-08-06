from keap.XML import DataService, ContactService, AffiliateService, AffiliateProgramService, DiscountService, \
    EmailService, FileService, FunnelService, InvoiceService, OrderService, ProductService, SearchService, \
    ShippingService, WebFormService


class XML:
    def __init__(self, keap):
        self.keap = keap
        self.AffiliateProgramService = AffiliateProgramService(keap)
        self.AffiliateService = AffiliateService(keap)
        self.ContactService = ContactService(keap)
        self.DataService = DataService(keap)
        self.DiscountService = DiscountService(keap)
        self.EmailService = EmailService(keap)
        self.FileService = FileService(keap)
        self.FunnelService = FunnelService(keap)
        self.InvoiceService = InvoiceService(keap)
        self.OrderService = OrderService(keap)
        self.ProductService = ProductService(keap)
        self.SearchService = SearchService(keap)
        self.ShippingService = ShippingService(keap)
        self.WebFormService = WebFormService(keap)
