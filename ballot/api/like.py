import frappe


@frappe.whitelist()
def toggle_like(reference_doctype: str, reference_name: str, comment_email: str) -> None:
    """
    Add a 'Like' comment to the specified document.

    Args:
        reference_doctype (str): The doctype of the document being liked.
        reference_name (str): The name of the document being liked.
        comment_email (str): The email of the user liking the document.

    Returns:
        None

    Raises:
        ValueError: If any of the input parameters are invalid.
        frappe.exceptions.ValidationError: If the document cannot be inserted.
    """
    if not reference_doctype or not reference_name or not comment_email:
        raise ValueError("All parameters must be provided and non-empty.")

    try:
        if is_already_liked(
            reference_doctype=reference_doctype,
            reference_name=reference_name,
            comment_email=comment_email,
        ):
            frappe.db.delete(
                "Comment",
                {
                    "reference_doctype": reference_doctype,
                    "reference_name": reference_name,
                    "comment_email": comment_email,
                    "comment_type": "Like",
                },
            )
        else:
            like = frappe.get_doc(
                {
                    "doctype": "Comment",
                    "comment_type": "Like",
                    "reference_doctype": reference_doctype,
                    "reference_name": reference_name,
                    "comment_email": comment_email,
                    "content": "Liked",
                }
            )
            like.insert(ignore_permissions=True)
    except Exception as e:
        frappe.log_error(message=str(e), title="Like Doc Insertion Failed")
        frappe.throw(frappe.ValidationError)


@frappe.whitelist(allow_guest=True)
def get_likes_count(reference_doctype: str, reference_name: str) -> int:
    """
    Get the count of likes for the specified document.

    Args:
        reference_doctype (str): The doctype of the document.
        reference_name (str): The name of the document.

    Returns:
        int: The number of likes for the document.
    """

    if not reference_doctype or not reference_name:
        raise ValueError(
            "Both reference_doctype and reference_name must be provided and non-empty."
        )

    return frappe.db.count(
        "Comment",
        filters={
            "reference_doctype": reference_doctype,
            "reference_name": reference_name,
            "comment_type": "Like",
        },
    )


@frappe.whitelist()
def is_already_liked(reference_doctype: str, reference_name: str, comment_email: str) -> bool:
    """
    Check if the specified document has already been liked by the given email.

    Args:
        reference_doctype (str): The doctype of the document.
        reference_name (str): The name of the document.
        comment_email (str): The email of the user.

    Returns:
        bool: True if the document is already liked by the given email, False otherwise.
    """

    if not reference_doctype or not reference_name or not comment_email:
        raise ValueError("All parameters must be provided and non-empty.")

    return (
        frappe.db.exists(
            "Comment",
            {
                "reference_doctype": reference_doctype,
                "reference_name": reference_name,
                "comment_email": comment_email,
                "comment_type": "Like",
            },
        )
        is not None
    )
