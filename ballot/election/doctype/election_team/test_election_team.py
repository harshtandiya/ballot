# Copyright (c) 2024, Harsh Tandiya and Contributors
# See license.txt

import frappe
from faker import Faker
from frappe.tests import IntegrationTestCase

from ballot.id.roles import TEAM_MEMBER as ROLE
from ballot.id.doctypes import TEAM
from ballot.tests.utils import create_election_team

fake = Faker()

TEAM_OWNER = "test1@example.com"
NEW_MEMBER = "test2@example.com"


class TestElectionTeam(IntegrationTestCase):
    def setUp(self):
        frappe.set_user(TEAM_OWNER)
        self.election_team = create_election_team()
        self.team_owner = TEAM_OWNER
        frappe.set_user("Administrator")

    def tearDown(self):
        frappe.delete_doc(TEAM, self.election_team.name, force=True)

    def test_owner_added_to_team(self):
        # Check if the owner is added to the team
        self.assertEqual(self.election_team.members[0].user, self.team_owner)

    def role_exists(self, user: str) -> bool:
        """Check if the `Election Team Member` role exists for a user."""
        return bool(frappe.db.exists("Has Role", {"role": ROLE, "parent": user}))

    def docshare_exists(self, team, user: str) -> bool:
        """Check if the `team` is shared with user"""
        return bool(
            frappe.db.exists(
                "DocShare",
                {"share_doctype": TEAM, "share_name": team, "user": user},
            )
        )

    def test_team_member_role_added(self):
        # Given an Election Team Member: self.election_team.members[0]
        # When the Election Team Member is created
        # Then the Election Team Member should have the role "Election Team Member"

        self.assertTrue(self.role_exists(self.team_owner))

        self.election_team.append(
            "members",
            {
                "user": NEW_MEMBER,
            },
        )
        self.election_team.save()

        self.assertTrue(self.role_exists(NEW_MEMBER))

    def test_team_member_role_removed(self):
        # Given an Election Team Member: self.election_team.members[0]
        # When the Election Team Member is removed
        # Then the Election Team Member should not have the role "Election Team Member"

        self.election_team.append(
            "members",
            {
                "user": NEW_MEMBER,
            },
        )
        self.election_team.save()

        self.assertTrue(self.role_exists(NEW_MEMBER))

        self.election_team.members = [
            m for m in self.election_team.members if m.user != NEW_MEMBER
        ]
        self.election_team.save()

        self.assertFalse(self.role_exists(NEW_MEMBER))

    def test_team_member_role_not_removed(self):
        # Given an Election Team Member: NEW_MEMBER
        # When the Election Team Member is removed
        # And the Election Team Member is part of another team
        # Then the Election Team Member should still have the role "Election Team Member"

        # Create another Election Team
        frappe.set_user(TEAM_OWNER)

        _election_team = frappe.get_doc(
            {
                "doctype": TEAM,
                "team_name": fake.name(),
            }
        )
        _election_team.insert()

        # Append New Member to this new team
        _election_team.append(
            "members",
            {
                "user": NEW_MEMBER,
            },
        )
        _election_team.save()
        self.assertTrue(self.role_exists(NEW_MEMBER))

        # Append new member to the original team
        self.election_team.append(
            "members",
            {
                "user": NEW_MEMBER,
            },
        )
        self.election_team.save()
        self.assertTrue(self.role_exists(NEW_MEMBER))

        # Remove new member from the new team
        _election_team.members = [m for m in _election_team.members if m.user != NEW_MEMBER]
        _election_team.save()

        # The role should retain
        self.assertTrue(self.role_exists(NEW_MEMBER))

        frappe.set_user("Administrator")
        _election_team.delete(force=1)

    def test_docshare_created_on_member_addition(self):
        """Test that a DocShare entry is created when a member is added."""
        self.assertFalse(self.docshare_exists(self.election_team.name, NEW_MEMBER))

        self.election_team.append("members", {"user": NEW_MEMBER})
        self.election_team.save()

        self.assertTrue(self.docshare_exists(self.election_team.name, NEW_MEMBER))

    def test_docshare_removed_on_member_removal(self):
        """Test that the DocShare entry is removed when a member is removed."""
        # Add the member first
        self.election_team.append("members", {"user": NEW_MEMBER})
        self.election_team.save()

        self.assertTrue(self.docshare_exists(self.election_team.name, NEW_MEMBER))

        # Remove the Member
        self.election_team.members = [
            m for m in self.election_team.members if m.user != NEW_MEMBER
        ]
        self.election_team.save()

        self.assertFalse(self.docshare_exists(self.election_team.name, NEW_MEMBER))
