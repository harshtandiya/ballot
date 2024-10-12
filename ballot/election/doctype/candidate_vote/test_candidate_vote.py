# Copyright (c) 2024, Harsh Tandiya and Contributors
# See license.txt

import frappe
from faker import Faker
from frappe.tests import IntegrationTestCase

fake = Faker()

ELECTION = "Election"
TEAM = "Election Team"
CANDIDATE_DOC = "Election Candidate"
FORM = "Election Nomination Form"
APPLICATION_DOC = "Election Candidate Application"
VOTE_DOC = "Candidate Vote"
TEAM_OWNER = "test1@example.com"
CANDIDATE_1 = "test2@example.com"
CANDIDATE_2 = "test3@example.com"


class TestCandidateVote(IntegrationTestCase):
    def setUp(self):
        frappe.set_user(TEAM_OWNER)

        # Create a Team
        team = frappe.get_doc(
            {
                "doctype": TEAM,
                "team_name": fake.name(),
            }
        )
        team.insert()
        self.team = team

        # Create an Election, linked to the above team
        election = frappe.get_doc(
            {
                "doctype": ELECTION,
                "title": fake.name(),
                "organizing_team": self.team.name,
            }
        )
        election.insert()
        self.election = election

        # Create a Nomination Form for the election
        form = frappe.get_doc(
            {
                "doctype": FORM,
                "status": "Live",
                "election": self.election.name,
            }
        )
        form.insert()
        self.form = form

        # Create a 1st Candidate Application for the election
        frappe.set_user(CANDIDATE_1)
        application_1 = frappe.get_doc(
            {
                "doctype": APPLICATION_DOC,
                "user": CANDIDATE_1,
                "election": self.election.name,
                "nomination_form": form.name,
                "full_name": fake.name(),
                "email": fake.email(),
            }
        )
        application_1.insert()

        # Create a 2nd Candidate Application for the election
        frappe.set_user(CANDIDATE_2)
        application_2 = frappe.get_doc(
            {
                "doctype": APPLICATION_DOC,
                "user": CANDIDATE_2,
                "election": self.election.name,
                "nomination_form": form.name,
                "full_name": fake.name(),
                "email": fake.email(),
            }
        )
        application_2.insert()

        # Accept the applications
        frappe.set_user(TEAM_OWNER)
        application_1.status = "Accepted"
        application_1.save()

        application_2.status = "Accepted"
        application_2.save()

        self.application_1 = application_1
        self.application_2 = application_2

        frappe.set_user("Administarator")

        # Get Candidate Docs
        candidate_1 = frappe.get_doc(
            CANDIDATE_DOC,
            {
                "election": self.election.name,
                "linked_application": self.application_1.name,
            },
            ["*"],
        )
        candidate_2 = frappe.get_doc(
            CANDIDATE_DOC,
            {
                "election": self.election.name,
                "linked_application": self.application_2.name,
            },
            ["*"],
        )

        self.candidate_1 = candidate_1
        self.candidate_2 = candidate_2

    def tearDown(self):
        frappe.set_user("Administrator")
        frappe.delete_doc(TEAM, self.team.name, force=1)
        frappe.delete_doc(ELECTION, self.election.name, force=1)
        frappe.delete_doc(FORM, self.form.name, force=1)
        frappe.delete_doc(APPLICATION_DOC, self.application_1.name, force=1)
        frappe.delete_doc(APPLICATION_DOC, self.application_2.name, force=1)
        frappe.delete_doc(CANDIDATE_DOC, self.candidate_1.name, force=1)
        frappe.delete_doc(CANDIDATE_DOC, self.candidate_2.name, force=1)

    def test_single_vote(self):
        # Given a candidate vote is created for an election
        # When the user tries to vote for another candidate in the same election
        # Then the user should not be able to vote for another candidate

        frappe.set_user("test4@example.com")
        vote1 = frappe.get_doc(
            {
                "doctype": VOTE_DOC,
                "vote_by": frappe.session.user,
                "election": self.election.name,
                "candidate": self.candidate_1.name,
            }
        )
        vote1.insert()

        vote2 = frappe.get_doc(
            {
                "doctype": VOTE_DOC,
                "vote_by": frappe.session.user,
                "election": self.election.name,
                "candidate": self.candidate_2.name,
            }
        )

        with self.assertRaises(frappe.ValidationError):
            vote2.insert()

        vote1.delete(force=1)
