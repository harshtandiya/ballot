import frappe
from faker import Faker

from ballot.id.doctypes import CANDIDATE, CANDIDATE_APPLICATION, ELECTION, NOMINATION_FORM, TEAM

fake = Faker()


def create_election_team() -> dict:
    """
    Creates and returns an Election Team.

    Note: session user is auto added as a team member
    """
    election_team = frappe.get_doc(
        {
            "doctype": TEAM,
            "team_name": fake.name(),
        }
    )
    election_team.insert()

    return election_team


def create_election(title: str, team_id: str, **kwargs) -> dict:
    """Creates and returns an Election linked to an Election Team."""
    election = frappe.get_doc(
        {
            "doctype": ELECTION,
            "title": title,
            "organizing_team": team_id,
            "status": kwargs.get("status", "Draft"),
            "voting_status": kwargs.get("voting_status", "Unopened"),
            "allowed_preference_count": kwargs.get("allowed_preference_count", 1),
        }
    )
    election.insert()

    return election


def create_nomination_form(election, **kwargs) -> dict:
    """Creates and returns a Nomination Form linked to an Election."""
    nomination_form = frappe.get_doc(
        {
            "doctype": NOMINATION_FORM,
            "election": election.name,
            "status": kwargs.get("status", "Draft"),
            "accept_incoming_applications": kwargs.get("accept_incoming_applications", 1),
        }
    )
    nomination_form.insert()

    return nomination_form


def create_candidate_application(election_id: str, form_id: str, **kwargs) -> dict:
    """Creates and returns a Candidate Application linked to a Nomination Form.

    Note: session user is auto added as a candidate
    """

    candidate_application = frappe.get_doc(
        {
            "user": kwargs.get("user", frappe.session.user),
            "doctype": CANDIDATE_APPLICATION,
            "election": election_id,
            "nomination_form": form_id,
            "status": kwargs.get("status", "Pending"),
            "full_name": fake.name(),
            "email": fake.email(),
            "designation": fake.job(),
            "organization": fake.company(),
        }
    )
    candidate_application.insert()

    return candidate_application


def create_candidate(election_id: str, application_id: str) -> dict:
    """Creates and returns a Candidate linked to a Candidate Application."""
    candidate = frappe.get_doc(
        {
            "doctype": CANDIDATE,
            "election": election_id,
            "linked_application": application_id,
        }
    )
    candidate.insert()

    return candidate
