# Copyright (c) 2024, Harsh Tandiya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CandidateVote(Document):
    def before_insert(self):
        if not self.is_voting_live():
            frappe.throw("Voting is closed for this election", frappe.ValidationError)

        if self.has_already_voted():
            frappe.throw("You have already voted in this election", frappe.ValidationError)

    def validate(self):
        self.validate_user()

    def has_already_voted(self):
        has_already_voted = frappe.db.exists(
            "Candidate Vote",
            {"vote_by": self.vote_by, "election": self.election},
        )

        return bool(has_already_voted)

    def validate_user(self):
        if not frappe.db.exists("User", {"name": self.vote_by}):
            frappe.throw("User does not exist", frappe.ValidationError)

    def is_voting_live(self):
        voting_status = frappe.db.get_value("Election", {"name": self.election}, "voting_status")
        return bool(voting_status == "Live")
