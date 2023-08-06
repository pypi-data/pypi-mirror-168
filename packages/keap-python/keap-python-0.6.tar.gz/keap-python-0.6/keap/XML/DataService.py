from keap.XML import BaseService


class DataService(BaseService):
    def __init__(self, keap):
        super().__init__(keap)

    def create(self, table, values):
        return self.call("create", table, values)

    def load(self, table, record, fields):
        return self.call("load", table, record, fields)

    def update(self, table, id, fields):
        return self.call("update", table, id, fields)

    def delete(self, table, id):
        return self.call("delete", table, id)

    def count(self, table, query):
        return self.call("count", table, query)

    def query(self, table, limit, page, query, return_fields, sort_by, ascending):
        return self.call("query", table, limit, page, query, return_fields, sort_by, ascending)

    def find_by_field(self, table, limit, page, field_name, field_value, return_fields):
        return self.call("findByField", table, limit, page, field_name, field_value, return_fields)

    def add_custom_field(self, table, display, type, header_id):
        return self.call("addCustomField", table, display, type, header_id)

    def update_custom_field(self, id, values):
        return self.call("updateCustomField", id, values)

    def get_app_setting(self, module, setting):
        return self.call("getAppSetting", module, setting)
