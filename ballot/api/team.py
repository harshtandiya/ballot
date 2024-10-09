import frappe

from .user import get_user_details


@frappe.whitelist()
def create_team(team_name: str):
    try:
        team = frappe.get_doc({"doctype": "Election Team", "team_name": team_name})
        team.insert()
    except Exception as e:
        frappe.throw("Error while creating team!" + repr(e))


@frappe.whitelist()
def get_user_teams(user: str):
    """
    Get teams of a user

    Args:
        user: User ID

    Returns:
        list of teams
    """

    teams = []

    member_docs = frappe.get_all(
        "Election Team Member",
        filters={"user": user, "parenttype": "Election Team"},
        fields=["parent"],
    )

    for member in member_docs:
        team = frappe.db.get_value(
            "Election Team", member["parent"], ["name", "team_name"], as_dict=1
        )
        team.update({"members": get_member_details(member["parent"])})
        teams.append(team)

    return teams


def get_member_details(team: str):
    """
    Get members of a team

    Args:
        team: Team ID

    Returns:
        list of members
    """

    members = []

    member_docs = frappe.get_all(
        "Election Team Member",
        filters={"parent": team},
        fields=["user"],
    )

    for member in member_docs:
        user = get_user_details(member["user"])
        members.append(user)

    return members
