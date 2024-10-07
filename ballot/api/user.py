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
