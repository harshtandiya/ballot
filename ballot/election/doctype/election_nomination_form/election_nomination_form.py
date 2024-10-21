# Copyright (c) 2024, Harsh Tandiya and contributors
# For license information, please see license.txt
import json

import frappe
from frappe.model.document import Document


class ElectionNominationForm(Document):
    def on_trash(self):
        self.delete_existing_form_fields()

    def before_save(self):
        self.add_fields_to_table()

    def add_fields_to_table(self):
        self.delete_existing_form_fields()

        if self.fields_meta is None:
            fields = []
        elif isinstance(self.fields_meta, str):
            fields = json.loads(self.fields_meta)
        elif isinstance(self.fields_meta, list):
            fields = self.fields_meta
        else:
            frappe.throw("fields_meta should be a JSON string or a list")


        for field in fields:
            self.append(
                "form_question",
                {
                    "label": field.get('label'),
                    "fieldtype": field.get('fieldtype'),
                    "fieldname": field.get('fieldname'),
                    "mandatory": field.get('mandatory'),
                    "options": field.get('options'),
                },
            )

    def delete_existing_form_fields(self):
        if len(self.form_question) == 0:
            return

        for q in self.form_question:
            frappe.delete_doc("Ballot Custom Question", q.name, force=1)
