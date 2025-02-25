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
        self.manage_docshare_on_save()

    def after_insert(self):
        self.manage_docshare_on_insert()

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
        return frappe.db.exists(self.ROLE, {"user": user, "parent": ("!=", self.name)})

    def remove_role_from_user(self, user):
        """Remove the role from a user if they are not part of any other teams."""
        user_doc = frappe.get_doc("User", user)
        role_map = {role.role: role for role in user_doc.get("roles")}

        if self.ROLE in role_map:
            user_doc.get("roles").remove(role_map[self.ROLE])
            user_doc.save(ignore_permissions=True)

    def manage_docshare_on_save(self):
        """Manage DocShare for team members, adding and removing as needed."""
        if self.is_new():
            return

        prev_doc = self.get_doc_before_save()
        current_users = {member.user for member in self.members}
        prev_users = {member.user for member in prev_doc.members} if prev_doc else set()

        # Add DocShare for new members
        new_users = current_users - prev_users
        for user in new_users:
            self.add_docshare(user)

        # Remove DocShare for removed members
        removed_users = prev_users - current_users
        for user in removed_users:
            self.remove_docshare(user)

    def manage_docshare_on_insert(self):
        """Manage DocShare creation for members at time of Team creation"""
        current_users = {member.user for member in self.members}

        for user in current_users:
            self.add_docshare(user)

    def add_docshare(self, user):
        """Create a DocShare entry if it doesn't already exist."""
        if not frappe.db.exists(
            "DocShare", {"share_doctype": "Election Team", "share_name": self.name, "user": user}
        ):
            docshare = frappe.get_doc(
                {
                    "doctype": "DocShare",
                    "share_doctype": "Election Team",
                    "share_name": self.name,
                    "user": user,
                    "read": 1,
                    "write": 1,
                    "share": 1,
                }
            )
            docshare.flags.ignore_share_permission = 1
            docshare.insert(ignore_permissions=True)

    def remove_docshare(self, user):
        """Delete the DocShare entry for the removed member."""
        frappe.db.delete(
            "DocShare", {"share_doctype": "Election Team", "share_name": self.name, "user": user}
        )
