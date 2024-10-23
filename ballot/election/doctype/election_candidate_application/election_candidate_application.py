# Copyright (c) 2024, Harsh Tandiya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from ballot.utils.team import is_election_team_member


class ElectionCandidateApplication(Document):
    def before_insert(self):
        if self.status != "Pending":
            frappe.throw(
                "You can only create a candidate application with status 'Pending'",
                frappe.PermissionError,
            )

    def after_insert(self):
        accept_incoming = frappe.db.get_value(
            "Election Nomination Form", self.nomination_form, "accept_incoming_applications"
        )

        if accept_incoming:
            self.status = 'Accepted'
            self.save(ignore_permissions=True)

    def before_save(self):
        if (
            self.modified_by != self.owner
            and frappe.session.user != "Administrator"
            and not is_election_team_member(self.election, self.modified_by)
        ):
            frappe.throw(
                "You do not have the permission to edit this document", frappe.PermissionError
            )

        if self.has_value_changed("status"):
            if self.status == "Accepted":
                self.create_candidate()

    def create_candidate(self):
        candidate = frappe.get_doc(
            {
                "doctype": "Election Candidate",
                "election": self.election,
                "linked_application": self.name,
            }
        )
        candidate.insert(ignore_permissions=True)
