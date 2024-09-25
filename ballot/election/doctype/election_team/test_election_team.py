# Copyright (c) 2024, Harsh Tandiya and Contributors
# See license.txt

import frappe
from faker import Faker
from frappe.tests.utils import FrappeTestCase

fake = Faker()

ROLE = "Election Team Member"
TEAM_OWNER = "test1@example.com"
NEW_MEMBER = "test2@example.com"

class TestElectionTeam(FrappeTestCase):
	def setUp(self):
		frappe.set_user(TEAM_OWNER)
		
		# Create a new Election Team
		election_team = frappe.get_doc({
			"doctype": "Election Team",
			"team_name": fake.name(),
		})
		election_team.insert()
		self.election_team = election_team
		self.team_owner = TEAM_OWNER

		frappe.set_user("Administrator")
	
	def tearDown(self):
		frappe.delete_doc("Election Team", self.election_team.name)

	def test_owner_added_to_team(self):
		# Check if the owner is added to the team
		self.assertEqual(self.election_team.members[0].user, self.team_owner)

	def test_team_member_role_added(self):
		# Given an Election Team Member: self.election_team.members[0]
		# When the Election Team Member is created
		# Then the Election Team Member should have the role "Election Team Member"

		self.assertTrue(frappe.db.exists("Has Role", {
			"role": ROLE,
			"parent": self.team_owner
		}))

		self.election_team.append("members", {
			"user": NEW_MEMBER,
		})
		self.election_team.save()

		self.assertTrue(frappe.db.exists("Has Role", {
			"role": ROLE,
			"parent": NEW_MEMBER,
		}))

	def test_team_member_role_removed(self):
		# Given an Election Team Member: self.election_team.members[0]
		# When the Election Team Member is removed
		# Then the Election Team Member should not have the role "Election Team Member"


		self.election_team.append("members", {
			"user": NEW_MEMBER,
		})
		self.election_team.save()

		self.assertTrue(frappe.db.exists("Has Role", {
			"role": ROLE,
			"parent": NEW_MEMBER,
		}))

		self.election_team.members = [m for m in self.election_team.members if m.user != NEW_MEMBER]
		self.election_team.save()

		self.assertFalse(frappe.db.exists("Has Role", {
			"role": ROLE,
			"parent": NEW_MEMBER,
		}))

	def test_team_member_role_not_removed(self):
		# Given an Election Team Member: NEW_MEMBER
		# When the Election Team Member is removed
		# And the Election Team Member is part of another team
		# Then the Election Team Member should still have the role "Election Team Member"

		# Create another Election Team
		frappe.set_user(TEAM_OWNER)

		_election_team = frappe.get_doc({
			"doctype": "Election Team",
			"team_name": fake.name(),
		})
		_election_team.insert()

		_election_team.append("members", {
			"user": NEW_MEMBER,
		})
		_election_team.save()

		self.assertTrue(frappe.db.exists("Has Role", {
			"role": ROLE,
			"parent": NEW_MEMBER,
		}))

		self.election_team.append("members", {
			"user": NEW_MEMBER,
		})
		self.election_team.save()

		self.assertTrue(frappe.db.exists("Has Role", {
			"role": ROLE,
			"parent": NEW_MEMBER,
		}))

		frappe.set_user("Administrator")

		_election_team.members = [m for m in _election_team.members if m.user != NEW_MEMBER]
		_election_team.save()

		self.assertTrue(frappe.db.exists("Has Role", {
			"role": ROLE,
			"parent": NEW_MEMBER,
		}))
