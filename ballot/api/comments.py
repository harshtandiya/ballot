import frappe
from .user import get_user_details


@frappe.whitelist(allow_guest=True)
def get_all_comments(doctype: str, docname: str) -> list:
    """
    Get all the comments of a doctype's document.

    args:
        doctype: doctype name/id
        docname: id of document whose comment's are needed

    returns:
        list: list of all comments
    """
    if (
        frappe.db.count(
            "Comment",
            {"reference_doctype": doctype, "reference_name": docname, "comment_type": "Comment"},
        )
        == 0
    ):
        return []

    comments = frappe.db.get_all(
        "Comment",
        {"reference_doctype": doctype, "reference_name": docname, "comment_type": "Comment"},
        [
            "comment_email",
            "subject",
            "content",
            "comment_by",
            "name",
            "reference_doctype",
            "reference_name",
            "creation",
        ],
        page_length=9999,
    )

    for comment in comments:
        user = get_user_details(comment.comment_email)
        comment["full_name"] = user.full_name
        comment["user_image"] = user.user_image
        comment["replies"] = get_all_comments("Comment", comment.name)

    return comments


@frappe.whitelist()
def add_comment(reference_doctype: str, reference_name: str, content: str) -> None:
    """
    Add a comment to permitted doctypes

    args:
        reference_doctype: doctype to add comment to
        reference_name: name of the document
        content: content of the comment
    """

    if reference_doctype not in ["Election Candidate Application", "Comment"]:
        frappe.throw("Not allowed to add comment to this doctype", frappe.PermissionError)

    comment = frappe.get_doc(
        {
            "doctype": "Comment",
            "comment_type": "Comment",
            "reference_doctype": reference_doctype,
            "reference_name": reference_name,
            "content": content,
        }
    )
    comment.insert(ignore_permissions=True)
