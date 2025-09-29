# Copyright (c) 2025, Axmed Najaad and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now
from datetime import datetime

class CustomNotification(Document):
    pass

# This is the main function that will be called by the hooks
def evaluate_custom_notifications(doc, method):
    """
    Checks for any matching Custom Notification rules and creates a Notification Log if conditions are met.
    """
    event_map = {
        "on_update": "Save",
        "on_submit": "Submit",
        "on_cancel": "Cancel",
    }
    send_on_event = event_map.get(method)

    if not send_on_event:
        return

    # --- IMPROVEMENT: PREVENT DUPLICATE NOTIFICATIONS ---
    # This block checks if a "Save" event is part of a "Submit" or "Cancel" action.
    # If the document's status is changing, it stops the "Save" notification from firing,
    # allowing only the more specific "Submit" or "Cancel" event to proceed.
    if send_on_event == "Save":
        doc_before_save = doc.get_doc_before_save()
        if doc_before_save and doc.docstatus != doc_before_save.docstatus:
            return  # Exit because this is a state-changing event, not a simple save.
    # --- END OF IMPROVEMENT ---

    try:
        custom_notifications = frappe.get_all(
            "Custom Notification",
            filters={"enabled": 1, "document_type": doc.doctype, "send_on": send_on_event},
            fields=["name", "condition", "subject", "message", "channel"],
        )

        for cn in custom_notifications:
            # The rest of your logic remains the same
            if not check_condition(doc, cn.condition):
                continue

            recipient_rules = frappe.get_all(
                "Custom Notification Recipient",
                filters={"parent": cn.name, "parenttype": "Custom Notification"},
                fields=["specific_user", "receiver_by_role", "receiver_by_document_field"]
            )

            recipients = get_recipients(doc, recipient_rules)
            if not recipients:
                continue

            context = {"doc": doc, "now": now, "datetime": datetime, "frappe": frappe}
            subject = frappe.render_template(cn.subject, context)
            message = frappe.render_template(cn.message, context)

            for user in recipients:
                send_notification(doc, user, subject, message, cn.channel)

    except Exception as e:
        frappe.log_error(f"Custom Notification Error for {doc.doctype} {doc.name}: {e}", "Custom Notification Evaluation")

def check_condition(doc, condition_str):
    """Checks if the condition is met."""
    if not condition_str or not condition_str.strip():
        return True

    condition_str = condition_str.strip()
    
    try:
        # Handle JSON-style conditions
        if condition_str.startswith('{') and condition_str.endswith('}'):
            return evaluate_dict_condition(doc, condition_str)
        else:
            # Handle Python expression conditions
            return evaluate_expression_condition(doc, condition_str)
    except Exception as e:
        frappe.log_error(f"Error evaluating condition '{condition_str}' for doc {doc.doctype} {doc.name}: {e}", "Custom Notification Condition Error")
        return False

def evaluate_dict_condition(doc, condition_str):
    """Evaluate JSON-style conditions"""
    import json
    import operator
    
    # Map operator strings to actual operator functions
    operator_map = {
        ">": operator.gt,
        ">=": operator.ge,
        "<": operator.lt,
        "<=": operator.le,
        "==": operator.eq,
        "!=": operator.ne,
        "in": lambda a, b: a in b if hasattr(b, '__contains__') else False,
        "not in": lambda a, b: a not in b if hasattr(b, '__contains__') else True,
    }
    
    try:
        conditions = json.loads(condition_str)
        
        for field, expected_value in conditions.items():
            # Remove 'doc.' prefix if present
            clean_field = field.replace('doc.', '')
            actual_value = doc.get(clean_field)
            
            # Handle comparison operators [">", 1000]
            if isinstance(expected_value, list) and len(expected_value) == 2:
                op_str, compare_value = expected_value
                
                # If compare_value is a string starting with 'doc.', get the field value
                if isinstance(compare_value, str) and compare_value.startswith('doc.'):
                    compare_field = compare_value.replace('doc.', '')
                    compare_value = doc.get(compare_field)
                
                if op_str in operator_map:
                    if not operator_map[op_str](actual_value, compare_value):
                        return False
                else:
                    frappe.log_error(f"Unknown operator '{op_str}' in condition", "Custom Notification Condition Error")
                    return False
            else:
                # Direct equality check
                if actual_value != expected_value:
                    return False
        
        return True
        
    except json.JSONDecodeError as e:
        frappe.log_error(f"Invalid JSON condition: {condition_str}. Error: {e}", "Custom Notification Condition Error")
        return False

def evaluate_expression_condition(doc, condition_str):
    """Evaluate Python expression conditions safely."""
    # Create a safe context
    context = {
        "doc": doc,
        "frappe": frappe,
        "now": frappe.utils.now,
        "datetime": datetime
    }
    
    try:
        # Use safe_eval for security
        result = frappe.safe_eval(condition_str, context)
        return bool(result)
    except Exception as e:
        frappe.log_error(f"Failed to evaluate expression: {condition_str}. Error: {e}", "Custom Notification Condition Error")
        return False

def get_recipients(doc, recipient_rules):
    """Gathers a unique list of recipients based on the rules."""
    users = set()

    for rule in recipient_rules:
        # 1. Specific User
        if rule.specific_user:
            users.add(rule.specific_user)

        # 2. Role-based recipients
        if rule.receiver_by_role:
            users_with_role = frappe.get_users_with_role(rule.receiver_by_role)
            users.update(users_with_role)

        # 3. Document field recipients
        if rule.receiver_by_document_field:
            user_from_field = doc.get(rule.receiver_by_document_field)
            if user_from_field and frappe.db.exists("User", user_from_field):
                users.add(user_from_field)
    
    return list(users)


def send_notification(doc, user, subject, message, channel):
    """Creates the Notification Log and sends emails/SMS as configured."""
    # Create the Notification Log
    notification_log = frappe.get_doc({
        "doctype": "Notification Log",
        "document_type": doc.doctype,
        "document_name": doc.name,
        "for_user": user,
        "subject": subject,
        "type": "Alert",
        "email_content": message
    })
    
    notification_log.insert(ignore_permissions=True)
    
    # PUBLISH REALTIME EVENT for frontend
    frappe.publish_realtime(
        event="new_notification",  # Event name that frontend will listen to
        message={
            "type": "new_notice",
            "notification_log": notification_log.name,
            "for_user": user,
            "subject": subject,
            "document_type": doc.doctype,
            "document_name": doc.name,
            "timestamp": now()
        },
        user=user,  # Only send to the specific user
        after_commit=True  # Ensure it's sent after the transaction is committed
    )
    
    # Also publish a general event for all users (if you want admin/other users to see)
    # frappe.publish_realtime(
    #     event="notification_update",  # General event for notification count updates
    #     message={
    #         "type": "count_update",
    #         "for_user": user
    #     },
    #     user=user,
    #     after_commit=True
    # )

    # Send Email
    if channel == "Email":
        frappe.sendmail(
            recipients=user,
            subject=subject,
            message=message,
            reference_doctype=doc.doctype,
            reference_name=doc.name,
            now=True # Send immediately
        )

    # Send SMS
    elif channel == "Sms":
        if frappe.db.get_single_value("SMS Settings", "sms_enabled"):
            user_doc = frappe.get_doc("User", user)
            if user_doc.mobile_no:
                frappe.send_sms(
                    receiver_list=[user_doc.mobile_no],
                    message=frappe.utils.strip_html_tags(message) # SMS messages should be plain text
                )
            else:
                frappe.log_error(f"SMS not sent for Custom Notification. User {user} has no mobile number.", "Custom Notification SMS Error")


@frappe.whitelist()
def get_user_link_fields(doctype):
    """Returns a list of fieldnames that are links to the User doctype for use in client scripts."""
    if not doctype or not frappe.db.exists("DocType", doctype):
        return []
    
    meta = frappe.get_meta(doctype)
    user_fields = {"owner", "modified_by"}
    
    for df in meta.get("fields", {"fieldtype": "Link", "options": "User"}):
        user_fields.add(df.fieldname)
            
    return sorted(list(user_fields))