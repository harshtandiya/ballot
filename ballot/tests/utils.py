import frappe
from faker import Faker

fake = Faker()


def create_election_team():
    """
    Creates and returns an Election Team.

    Note: session user is auto added as a team member
    """
    election_team = frappe.get_doc(
        {
            "doctype": "Election Team",
            "team_name": fake.name(),
        }
    )
    election_team.insert()

    return election_team


def create_election(title, team_name):
    """Creates and returns an Election linked to an Election Team."""
    election = frappe.get_doc(
        {
            "doctype": "Election",
            "title": title,
            "organizing_team": team_name,
            "status": "Draft",
        }
    )
    election.insert()

    return election
