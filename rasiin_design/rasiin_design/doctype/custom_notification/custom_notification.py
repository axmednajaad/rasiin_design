# Copyright (c) 2025, Axmed Najaad and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now
from datetime import datetime

class CustomNotification(Document):
    pass


# def evaluate_custom_notifications(doc, method):
#     """
#     Checks for any matching Custom Notification rules and creates a Notification Log if conditions are met.
#     """
#     event_map = {
#         "on_update": "Save",
#         "on_submit": "Submit",
#         "on_cancel": "Cancel",
#     }
#     send_on_event = event_map.get(method)

#     if not send_on_event:
#         return

#     # Get doc_before_save for comparison
#     doc_before_save = doc.get_doc_before_save()

#     # Skip if this is part of a submit/cancel action
#     if send_on_event == "Save" and doc_before_save and doc.docstatus != doc_before_save.docstatus:
#         return

#     try:
#         custom_notifications = frappe.get_all(
#             "Custom Notification",
#             filters={"enabled": 1, "document_type": doc.doctype, "send_on": send_on_event},
#             fields=["name", "condition", "subject", "message", "channel"],
#         )

#         for cn in custom_notifications:
#             if not check_condition(doc, cn.condition):
#                 continue

#             # Skip if there are no actual field changes (for Save events)
#             if send_on_event == "Save" and doc_before_save and not has_actual_changes(doc, doc_before_save):
#                 continue

#             recipient_rules = frappe.get_all(
#                 "Custom Notification Recipient",
#                 filters={"parent": cn.name, "parenttype": "Custom Notification"},
#                 fields=["specific_user", "receiver_by_role", "receiver_by_document_field"]
#             )

#             recipients = get_recipients(doc, recipient_rules)
#             if not recipients:
#                 continue

#             # Enhanced generic context with doc_before_save and old field values
#             context = build_template_context(doc, doc_before_save)
            
#             subject = frappe.render_template(cn.subject, context)
#             message = frappe.render_template(cn.message, context)

#             for user in recipients:
#                 send_notification(doc, user, subject, message, cn.channel)

#     except Exception as e:
#         frappe.log_error(f"Custom Notification Error for {doc.doctype} {doc.name}: {e}", "Custom Notification Evaluation")

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

    # Get doc_before_save for comparison
    doc_before_save = doc.get_doc_before_save()

    # Skip if this is part of a submit/cancel action
    if send_on_event == "Save" and doc_before_save and doc.docstatus != doc_before_save.docstatus:
        return

    try:
        custom_notifications = frappe.get_all(
            "Custom Notification",
            filters={
                "enabled": 1, 
                "document_type": doc.doctype, 
                "send_on": send_on_event
            },
            fields=["name", "condition", "subject", "message", "channel"],
        )

        frappe.logger().info(f"Found {len(custom_notifications)} notifications for {doc.doctype} on {send_on_event}")

        for cn in custom_notifications:
            frappe.logger().debug(f"Processing notification: {cn.name}")

            # Check condition
            if not check_condition(doc, cn.condition):
                frappe.logger().debug(f"Condition not met for {cn.name}")
                continue

            # Skip if no actual changes (for Save events)
            if send_on_event == "Save" and doc_before_save and not has_actual_changes(doc, doc_before_save):
                frappe.logger().debug(f"No actual changes for {cn.name}")
                continue

            # Get recipient rules (NEW STRUCTURE)
            recipient_rules = frappe.get_all(
                "Custom Notification Recipient",
                filters={"parent": cn.name},
                fields=["recipient_type", "recipient_value"]
            )

            frappe.logger().debug(f"Found {len(recipient_rules)} recipient rules for {cn.name}")

            # Get recipients
            recipients = get_recipients(doc, recipient_rules)
            
            # Validation for empty recipients
            if not recipients:
                frappe.log_error(f"No valid recipients found for notification {cn.name}", "Custom Notification")
                continue

            # Create context and render templates
            context = build_template_context(doc, doc_before_save)
            subject = frappe.render_template(cn.subject, context)
            message = frappe.render_template(cn.message, context)

            frappe.logger().info(f"Sending notification '{cn.name}' to {len(recipients)} recipients")

            # Send notifications
            for user in recipients:
                send_notification(doc, user, subject, message, cn.channel)
                
            # Success logging
            frappe.logger().info(f"Custom Notification '{cn.name}' successfully sent to {len(recipients)} users: {recipients}")

    except Exception as e:
        frappe.log_error(f"Custom Notification Error for {doc.doctype} {doc.name}: {e}", "Custom Notification Evaluation")
        
        

def has_actual_changes(doc, doc_before_save):
    """
    Check if there are any actual field value changes between current doc and previous version.
    """
    # List of fields to ignore when checking for changes
    ignore_fields = {'modified', 'modified_by', 'amended_from', '_user_tags', '_comments', '_assign', '_liked_by'}
    
    for field in doc.meta.get_valid_columns():
        if field in ignore_fields:
            continue
            
        current_value = doc.get(field)
        previous_value = doc_before_save.get(field)
        
        if current_value != previous_value:
            return True
    
    return False

def build_template_context(doc, doc_before_save):
    """
    Build a comprehensive template context with old field values for any document type.
    """
    context = {
        "doc": doc, 
        "doc_before_save": doc_before_save,
        "now": now, 
        "datetime": datetime, 
        "frappe": frappe
    }
    
    # Add old field values for all fields that changed
    if doc_before_save:
        for field in doc.meta.get_valid_columns():
            if hasattr(doc_before_save, field):
                old_field_name = f"old_{field}"
                context[old_field_name] = getattr(doc_before_save, field)
    
    return context



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
    """Gathers a unique list of recipients based on the enhanced rules."""
    users = set()

    for rule in recipient_rules:
        recipient_type = rule.recipient_type
        recipient_value = rule.recipient_value

        if not recipient_type or not recipient_value:
            continue

        try:
            if recipient_type == "User":
                # Validate and add specific user
                if frappe.db.exists("User", recipient_value):
                    user_enabled = frappe.db.get_value("User", recipient_value, "enabled")
                    if user_enabled:
                        users.add(recipient_value)
                        frappe.logger().debug(f"Added user: {recipient_value}")
                    else:
                        frappe.log_error(f"User {recipient_value} is disabled", "Custom Notification Recipient")
                else:
                    frappe.log_error(f"User {recipient_value} not found", "Custom Notification Recipient")

            elif recipient_type == "Role":
                # Get all users with the specified role
                users_with_role = frappe.get_all(
                    "Has Role",
                    filters={
                        "role": recipient_value,
                        "parenttype": "User"
                    },
                    fields=["parent"],
                    distinct=True
                )
                
                if users_with_role:
                    for user_role in users_with_role:
                        user_name = user_role.parent
                        if user_name and frappe.db.exists("User", user_name):
                            # Check if user is enabled
                            if frappe.db.get_value("User", user_name, "enabled"):
                                users.add(user_name)
                                frappe.logger().debug(f"Added user {user_name} from role {recipient_value}")
                    frappe.logger().info(f"Found {len(users_with_role)} users with role {recipient_value}")
                else:
                    frappe.log_error(f"No users found with role {recipient_value}", "Custom Notification Recipient")

        except Exception as e:
            frappe.log_error(f"Error processing recipient rule {recipient_type}: {recipient_value}. Error: {e}", "Custom Notification Recipient")

    # Remove None values and return sorted list
    valid_users = sorted(list(filter(None, users)))
    frappe.logger().info(f"Final recipient list: {valid_users}")
    return valid_users



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