from keap.XML import BaseService


class ContactService(BaseService):
    def __init__(self, keap):
        super().__init__(keap)

    def add(self, values):
        return self.call("add", values)

    def add_with_dupe_check(self, values, dup_check_type):
        return self.call("addWithDupCheck", values, dup_check_type)

    def update(self, contact_id, fields):
        return self.call("update", contact_id, fields)

    def load(self, contact_id, fields):
        return self.call("load", contact_id, fields)

    def delete(self, table, contact_id):
        return self.call("delete", table, contact_id)

    def merge(self, receiving_id, providing_id):
        return self.call("merge", receiving_id, providing_id)

    def find_by_email(self, email, fields):
        return self.call("findByEmail", email, fields)

    def add_to_group(self, contact_id, tag_id):
        return self.call("addToGroup", contact_id, tag_id)

    def add_tag(self, contact_id, tag_id):
        return self.add_to_group(contact_id, tag_id)

    def remove_from_group(self, contact_id, tag_id):
        return self.call("removeFromGroup", contact_id, tag_id)

    def remove_tag(self, contact_id, tag_id):
        return self.remove_from_group(contact_id, tag_id)

    def link_contacts(self, contact_id_1, contact_id_2, link_type_id):
        return self.call("linkContacts", contact_id_1, contact_id_2, link_type_id)

    def unlink_contacts(self, contact_id_1, contact_id_2, link_type_id):
        return self.call("unlinkContacts", contact_id_1, contact_id_2, link_type_id)

    def list_linked_contacts(self, contact_id):
        return self.call("listLinkedContacts", contact_id)

    def get_app_setting(self, module, setting):
        return self.call("getAppSetting", module, setting)
