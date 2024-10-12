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
            "Election Team", member["parent"], ["name", "team_name", "owner"], as_dict=1
        )
        team.update({"members": get_member_details(member["parent"])})
        team.update({"owner_name": get_team_owner(team.name, user)})
        teams.append(team)

    return teams

@frappe.whitelist()
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


def get_team_owner(team: str, user: str = None):
    """
    Get the owner name of the team.

    Args:
        team: team ID

    Return:
        owner name or "You" if the session user is the owner.
    """

    owner = frappe.db.get_value("Election Team", team, "owner")

    owner_details = get_user_details(owner)

    if user and owner == user:
        return "You"

    return owner_details["full_name"]

@frappe.whitelist()
def add_member_to_team(team: str, user: str):
    '''
    Add a user as a member to a team.

    Args:
        team: team id
        user: user id / email
    '''

    if not frappe.db.exists("User", user):
        frappe.throw("Sorry, we couldn't find that user. Please make sure they are registered.")

    team_doc = frappe.get_doc("Election Team", team)
    team_doc.append("members", {
        "user": user,
    })
    team_doc.save(ignore_permissions = True)