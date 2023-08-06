from keap.XML import BaseService


class EmailService(BaseService):
    _service = "APIEmailService"

    def __init__(self, keap):
        super().__init__(keap)

