# Copyright (c) 2024, Harsh Tandiya and Contributors
# See license.txt

import frappe
from faker import Faker
from frappe.tests.utils import FrappeTestCase

ELECTION_DOC = "Election"
TEAM_DOC = "Election Team"
CANDIDATE_DOC = "Election Candidate"
FORM_DOC = "Election Nomination Form"
APPLICATION_DOC = "Election Candidate Application"
TEAM_OWNER = "test1@example.com"
CANDIDATE_1 = "test2@example.com"
CANDIDATE_2 = "test3@example.com"

fake = Faker()


class TestElectionCandidateApplication(FrappeTestCase):
    def setUp(self):
        frappe.set_user(TEAM_OWNER)

        team = frappe.get_doc(
            {
                "doctype": TEAM_DOC,
                "team_name": fake.name(),
            }
        )
        team.insert()
        self.team = team

        election = frappe.get_doc(
            {
                "doctype": ELECTION_DOC,
                "title": fake.name(),
                "organizing_team": self.team.name,
            }
        )
        election.insert()
        self.election = election

        form = frappe.get_doc(
            {
                "doctype": FORM_DOC,
                "status": "Live",
                "election": self.election.name,
            }
        )
        form.insert()

        self.form = form

        frappe.set_user(CANDIDATE_1)
        application = frappe.get_doc(
            {
                "doctype": APPLICATION_DOC,
                "user": CANDIDATE_1,
                "election": self.election.name,
                "nomination_form": self.form.name,
                "full_name": fake.name(),
                "email": fake.email(),
            }
        )
        application.insert()

        self.application = application
        self.candidate_user = CANDIDATE_1

        frappe.set_user("Administrator")

    def tearDown(self):
        frappe.set_user("Administrator")
        frappe.delete_doc(FORM_DOC, self.election.name, force=1)
        frappe.delete_doc(ELECTION_DOC, self.election.name, force=1)
        frappe.delete_doc(TEAM_DOC, self.team.name, force=1)

    def test_create_accepted_application(self):
        # Given a candidate: CANDIDATE_1
        # When the candidate creates an application for an election with status "Accepted"
        # Then the application should not be created

        frappe.set_user(CANDIDATE_2)

        application = frappe.get_doc(
            {
                "doctype": APPLICATION_DOC,
                "user": CANDIDATE_2,
                "election": self.election.name,
                "nomination_form": self.form.name,
                "full_name": fake.name(),
                "email": fake.email(),
                "status": "Accepted",
            }
        )

        with self.assertRaises(frappe.PermissionError):
            application.insert()

    def test_modify_other_application(self):
        # Given a candidate: CANDIDATE_1
        # When the candidate tries to modify an application of another candidate
        # Then the candidate should not be able to modify the application
        frappe.set_user(self.candidate_user)

        self.application.full_name = fake.name()
        self.application.save()
        self.application.reload()

        self.assertTrue(
            self.application.get_doc_before_save().full_name != self.application.full_name
        )

        frappe.set_user(CANDIDATE_2)

        self.application.full_name = fake.name()

        with self.assertRaises(frappe.PermissionError):
            self.application.save()

    def test_modify_by_team_member(self):
        # Given a candidate: CANDIDATE_1
        # When a team member tries to modify the application of the candidate
        # Then the team member should be able to modify the application
        frappe.set_user(TEAM_OWNER)

        self.application.status = "Rejected"
        self.application.save()
        self.application.reload()

        self.assertTrue(self.application.status == "Rejected")

    def test_modify_by_random_team_role_user(self):
        frappe.set_user("test4@example.com")

        _team = frappe.get_doc(
            {
                "doctype": TEAM_DOC,
                "team_name": fake.name(),
            }
        )
        _team.insert()
        _team.reload()

        self.application.status = "Accepted"

        with self.assertRaises(frappe.PermissionError):
            self.application.save()

    def test_candidate_creation(self):
        # Given an application with status "Pending"
        # When the application status is changed to "Accepted"
        # Then a candidate should be created
        frappe.set_user(TEAM_OWNER)

        self.application.status = "Accepted"
        self.application.save()
        self.application.reload()

        candidate_exists = frappe.db.exists(
            CANDIDATE_DOC,
            {"election": self.application.election, "linked_application": self.application.name},
        )
        self.assertTrue(candidate_exists)
