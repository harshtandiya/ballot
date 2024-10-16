import frappe

@frappe.whitelist()
def has_nomination_form(election: str) -> bool:
    '''
    Check whether the election has created nomination form

    args:
        election : election id
    
    returns:
        bool: true or false
    '''

    if frappe.db.exists('Election Nomination Form', {'election': election}):
        return True
    
    return False