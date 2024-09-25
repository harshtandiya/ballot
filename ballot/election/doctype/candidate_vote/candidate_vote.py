# Copyright (c) 2024, Harsh Tandiya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CandidateVote(Document):
    def before_insert(self):
        if self.has_already_voted():
            frappe.throw("You have already voted in this candidate", frappe.ValidationError)

    def has_already_voted(self):
        has_already_voted = frappe.db.exists(
            "Candidate Vote",
            {"vote_by": self.vote_by, "election": self.election},
        )

        return bool(has_already_voted)
