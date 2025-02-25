import frappe

from ballot.id.doctypes import TEAM_MEMBER, TEAM


def execute():
    """
    In this patch, the code will go through all the existing Election teams,
    and create a DocShare document for all the existing members of the teams.
    """
    members = frappe.db.get_all(TEAM_MEMBER, ["*"], page_length=9999)

    for member in members:
        docshare = frappe.get_doc(
            {
                "doctype": "DocShare",
                "share_doctype": TEAM,
                "share_name": member.parent,
                "user": member.user,
                "read": 1,
                "write": 1,
                "share": 1,
            }
        )
        docshare.flags.ignore_share_permission = 1
        docshare.insert(ignore_permissions=True)
