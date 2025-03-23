# Copyright (c) 2024, Harsh Tandiya and Contributors
# See license.txt

import frappe
from faker import Faker
from frappe.tests import IntegrationTestCase

from ballot.id.doctypes import (
    CANDIDATE,
    CANDIDATE_APPLICATION,
    ELECTION,
    NOMINATION_FORM,
    TEAM,
    VOTE,
)
from ballot.tests.utils import (
    create_candidate_application,
    create_election,
    create_election_team,
    create_nomination_form,
)

fake = Faker()


TEAM_OWNER = "test1@example.com"
CANDIDATE_USER = "test2@example.com"
VOTER = "test3@example.com"


class TestCandidateVote(IntegrationTestCase):
    def setUp(self):
        frappe.set_user(TEAM_OWNER)
        self.election_team = create_election_team()
        self.election = create_election(
            "Test Election", self.election_team.name, voting_status="Live"
        )
        self.nomination_form = create_nomination_form(self.election, status="Live")
        frappe.set_user(CANDIDATE_USER)
        self.candidate_application = create_candidate_application(
            self.election.name, self.nomination_form.name
        )
        self.candidate = frappe.get_doc(
            CANDIDATE,
            {
                "linked_application": self.candidate_application.name,
                "election": self.election.name,
            },
        )

    def tearDown(self):
        frappe.set_user("Administrator")
        frappe.delete_doc(TEAM, self.election_team.name, force=True)
        frappe.delete_doc(ELECTION, self.election.name, force=1)
        frappe.delete_doc(NOMINATION_FORM, self.nomination_form.name, force=1)
        frappe.delete_doc(CANDIDATE_APPLICATION, self.candidate_application.name, force=1)
        frappe.delete_doc(CANDIDATE, self.candidate.name, force=1)

    def test_single_candidate_vote(self):
        frappe.set_user(VOTER)

        candidate_vote = frappe.get_doc(
            {
                "doctype": VOTE,
                "vote_by": frappe.session.user,
                "election": self.election.name,
                "candidate_tiers": [
                    {
                        "rank": 1,
                        "candidate": self.candidate.name,
                    }
                ],
            }
        )
        candidate_vote.submit()

        # Given a Voter has already voted for a Candidate, they should not be able to vote again
        second_vote = frappe.get_doc(
            {
                "doctype": VOTE,
                "vote_by": frappe.session.user,
                "election": self.election.name,
                "candidate_tiers": [
                    {
                        "rank": 1,
                        "candidate": self.candidate.name,
                    }
                ],
            }
        )
        with self.assertRaises(frappe.ValidationError):
            second_vote.submit()

    def test_valid_user_vote(self):
        frappe.set_user(VOTER)

        candidate_vote = frappe.get_doc(
            {
                "doctype": VOTE,
                "vote_by": "not_a_valid_user@example.com",
                "election": self.election.name,
                "candidate_tiers": [
                    {
                        "rank": 1,
                        "candidate": self.candidate.name,
                    }
                ],
            }
        )

        with self.assertRaises(frappe.ValidationError):
            candidate_vote.submit()

    def test_voting_when_voting_is_closed(self):
        frappe.set_user(TEAM_OWNER)
        self.election.voting_status = "Closed"
        self.election.save()

        frappe.set_user(VOTER)

        candidate_vote = frappe.get_doc(
            {
                "doctype": VOTE,
                "vote_by": frappe.session.user,
                "election": self.election.name,
                "candidate_tiers": [
                    {
                        "rank": 1,
                        "candidate": self.candidate.name,
                    }
                ],
            }
        )

        with self.assertRaises(frappe.ValidationError):
            candidate_vote.submit()
