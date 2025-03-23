import frappe


@frappe.whitelist(allow_guest=True)
def get_all_candidates(election: str):
    """
    Get all the candidate application submissions of an election

    args:
        election(str): election ID

    returns:
        list of candidates
    """

    candidates = frappe.db.get_all(
        "Election Candidate Application",
        {"election": election, "status": "Accepted"},
        ["full_name", "designation", "organization", "photo", "submission_meta", "name"],
        page_length=999,
        order_by="creation",
    )

    return candidates


@frappe.whitelist(allow_guest=True)
def get_candidate_details(candidate: str):
    """
    Get the details of a candidate's candidature form through the ID

    args:
        candidate(str): ID

    returns:
        dict: details of the form
    """

    form = frappe.db.get_value(
        "Election Candidate Application",
        candidate,
        ["photo", "full_name", "designation", "organization", "submission_meta", "name"],
        as_dict=1,
    )

    return form


@frappe.whitelist()
def get_candidate_list_for_voting(election: str):
    """
    Get the list of candidates for voting

    args:
        election(str): election ID

    returns:
        list of candidates
    """

    candidates = frappe.db.get_all(
        "Election Candidate Application",
        {"election": election, "status": "Accepted"},
        ["full_name", "designation", "organization", "photo", "submission_meta", "name"],
        page_length=999,
        order_by="creation",
    )

    for candidate in candidates:
        candidate["candidate_id"] = frappe.db.get_value(
            "Election Candidate", {"linked_application": candidate["name"]}, "name"
        )

    return candidates
