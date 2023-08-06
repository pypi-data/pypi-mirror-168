from keap.XML import BaseService


class AffiliateService(BaseService):
    _service = "APIAffiliateService"

    def __init__(self, keap):
        super().__init__(keap)

    def retrieve_running_totals(self, affiliate_ids):
        return self.affRunningTotals(affiliate_ids)
