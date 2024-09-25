# Copyright (c) 2024, Harsh Tandiya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ElectionTeam(Document):
    def before_insert(self):
        self.append(
            "members",
            {
                "user": self.owner,
            },
        )

    def before_save(self):
        self.add_team_member_role()
        self.handle_member_removal()

    def add_team_member_role(self):
        ROLE = "Election Team Member"

        for member in self.members:
            # Add the role to the user
            user = frappe.get_doc("User", member.user)
            existing_roles = {d.role: d for d in user.get("roles")}

            if ROLE in existing_roles:
                continue

            user.append("roles", {"role": ROLE, "doctype": "Has Role"})
            user.save(ignore_permissions=True)

    def handle_member_removal(self):
        prev_doc = self.get_doc_before_save()
        if not prev_doc:
            return

        ROLE = "Election Team Member"

        for member in prev_doc.members:
            if member.user not in [m.user for m in self.members]:
                has_other_teams = frappe.db.exists(
                    "Election Team Member", {"user": member.user, "parent": ("!=", self.name)}
                )

                if has_other_teams:
                    continue

                # Remove the role from the user
                user = frappe.get_doc("User", member.user)
                existing_roles = {d.role: d for d in user.get("roles")}

                if ROLE in existing_roles:
                    user.get("roles").remove(existing_roles[ROLE])
                    user.save(ignore_permissions=True)
