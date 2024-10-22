# Copyright (c) 2024, Harsh Tandiya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from ballot.utils.team import is_election_team_member


class ElectionCandidateApplication(Document):
    def before_save(self):
        if self.modified_by != self.owner and not is_election_team_member(
            self.election, self.modified_by
        ):
            frappe.throw(
                "You do not have the permission to edit this document", frappe.PermissionError
            )
