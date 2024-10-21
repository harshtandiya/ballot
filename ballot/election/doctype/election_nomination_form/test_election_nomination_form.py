# Copyright (c) 2024, Harsh Tandiya and Contributors
# See license.txt

import frappe
import random
import json
from faker import Faker
from frappe.tests import IntegrationTestCase, UnitTestCase

fake = Faker()


class TestElectionNominationForm(IntegrationTestCase):
    def setUp(self):
        team = frappe.get_doc(
            {
                "doctype": "Election Team",
                "team_name": fake.name(),
            }
        )
        team.insert()
        team.reload()
        self.team = team

        election = frappe.get_doc(
            {
                "doctype": "Election",
                "title": fake.name(),
                "organizing_team": team.name,
                "slug": fake.slug(),
                "status": "Live",
            }
        )
        election.insert()
        election.reload()
        self.election = election

        form = frappe.get_doc(
            {
                "doctype": "Election Nomination Form",
                "election": election.name,
                "status": "Live",
            }
        )
        form.insert()
        form.reload()
        self.form = form

    def tearDown(self):
        frappe.delete_doc("Election Team", self.team.name, force=1)
        frappe.delete_doc("Election", self.election.name, force=1)
        frappe.delete_doc("Election Nomination Form", self.form.name, force=1)

    def test_fields_added_on_save(self):
        fields_meta = []
        for i in range(1, 5):
            fields_meta.append(
                {
                    "label": fake.name(),
                    "fieldname": fake.slug(),
                    "mandatory": 0,
                    "fieldtype": random.choice(
                        ["Data", "Textarea", "Section Break", "Column Break", "Checkbox"]
                    ),
                    "options": "",
                }
            )
        
        self.form.fields_meta = json.dumps(fields_meta)
        self.form.save()

        self.form.reload()

        self.assertTrue(len(self.form.form_question) == len(fields_meta))