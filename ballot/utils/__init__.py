import frappe


@frappe.whitelist()
def is_slug_valid(doctype: str, slug: str, docname: str = None):
    """
    Check the validity of slug, whether it is unique or not for a particular doctype

    args:
        doctype: Doctype Name
        slug: slug to check

    returns:
        bool: true or false
    """
    filters = {}

    if docname:
        filters.update({"name": ["!=", docname]})
    filters.update({"slug": slug})

    if frappe.db.exists(doctype, filters):
        return False

    return True
