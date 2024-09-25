import frappe


def is_election_team_member(election: str, user: str):
    """
    Check if the user is a member of the election's team

    Args:
        election (str): Election ID
        user (str): User ID

    Returns:
        bool: True if the user is a member of the election's team, False otherwise
    """
    team_id = frappe.db.get_value("Election", election, "organizing_team")

    is_team_member = frappe.db.exists(
        "Election Team Member", {"parent": team_id, "parenttype": "Election Team", "user": user}
    )

    return bool(is_team_member)
