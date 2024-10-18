import frappe


@frappe.whitelist(allow_guest=True)
def get_election_from_slug(slug: str) -> dict:
    """
    Get the election details from its slug

    args:
        slug: str

    returns:
        dict with election details
    """

    election = frappe.db.get_value(
        "Election",
        {"slug": slug},
        ["name", "slug", "title", "status", "organizing_team", "description"],
        as_dict=True,
    )

    return election


@frappe.whitelist(allow_guest=True)
def has_nomination_form(election: str) -> bool:
    """
    Check whether the election has created nomination form

    args:
        election : election id

    returns:
        bool: true or false
    """

    if frappe.db.exists("Election Nomination Form", {"election": election}):
        return True

    return False


@frappe.whitelist(allow_guest=True)
def get_election_candidature_form(election: str) -> dict:
    """
    Returns the candidate form details of an election

    arg:
        election(str): election id

    returns:
        dict: form details
    """

    form = frappe.db.get_value(
        "Election Nomination Form",
        {"election": election},
        ["status", "name", "description", "fields_meta"],
        as_dict=True,
    )

    return form
