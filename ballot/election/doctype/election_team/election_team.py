# Copyright (c) 2024, Harsh Tandiya and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ElectionTeam(Document):
    ROLE = "Election Team Member"

    def before_insert(self):
        """Automatically add the creator as a member."""
        self.append("members", {"user": self.owner})

    def before_save(self):
        """Handle member role assignment and removal."""
        self.add_team_member_role()
        self.remove_team_member_role()

    def add_team_member_role(self):
        """Ensure all team members have the required role."""
        for member in self.members:
            user = frappe.get_doc("User", member.user)
            user_roles = {role.role for role in user.get("roles")}

            if self.ROLE not in user_roles:
                user.append("roles", {"role": self.ROLE, "doctype": "Has Role"})
                user.save(ignore_permissions=True)

    def remove_team_member_role(self):
        """Remove the role from users who are no longer in the team."""
        prev_doc = self.get_doc_before_save()
        if not prev_doc:
            return

        current_users = {member.user for member in self.members}

        for member in prev_doc.members:
            if member.user not in current_users:
                if self.user_in_other_teams(member.user):
                    continue

                self.remove_role_from_user(member.user)

    def user_in_other_teams(self, user):
        """Check if the user is part of other Election Teams."""
        return frappe.db.exists(
            self.ROLE, {"user": user, "parent": ("!=", self.name)}
        )

    def remove_role_from_user(self, user):
        """Remove the role from a user if they are not part of any other teams."""
        user_doc = frappe.get_doc("User", user)
        role_map = {role.role: role for role in user_doc.get("roles")}

        if self.ROLE in role_map:
            user_doc.get("roles").remove(role_map[self.ROLE])
            user_doc.save(ignore_permissions=True)
