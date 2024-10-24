import frappe


@frappe.whitelist()
def get_user_details(user: str):
    """
    Get user details such as full_name, profile_photo from user ID

    Args:
        user: User ID

    Returns:
        dict with user details
    """

    details = frappe.db.get_value("User", user, ["full_name", "user_image", "username"], as_dict=1)

    return details


@frappe.whitelist()
def get_user_submissions(user: str):
    """
    Returns all the candidature submissions of a user for all elections

    args:
        user: user id / email

    returns:
        list: of candidature forms with details
    """

    submissions = frappe.db.get_all(
        "Election Candidate Application",
        {"user": user},
        ["election", "creation", "status", "name"],
        page_length=999,
        order_by="creation desc",
    )

    for submission in submissions:
        election = frappe.db.get_value(
            "Election", submission.election, ["title", "slug"], as_dict=1
        )
        submission["election_title"] = election.title
        submission["route"] = f"/election/{election.slug}/c/{submission.name}"

    return submissions
