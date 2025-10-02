# utils/notification_utils.py
import frappe
from frappe.utils import now, format_date
from frappe import _

def get_notification_users(notification_type="overdue"):
    """
    Get list of users to notify based on notification type
    """
    notification_configs = {
        "overdue": {
            # "users": ["Administrator", "jamal@gmail.com"],
            "users": ["Administrator"],
            # "roles": ["Accounts Manager", "Accounts User", "System Manager"]
            "roles": ["System Manager"]
        },
        "low_stock": {
            # "users": ["Administrator", "jamal@gmail.com"],
            "users": ["Administrator"],
            # "roles": ["Stock Manager", "Purchase Manager", "Item Manager", "System Manager"]
            "roles": ["System Manager"]
        }
    }
    
    config = notification_configs.get(notification_type, {
        "users": ["Administrator"],
        "roles": ["System Manager"]
    })
    
    users_from_list = config.get("users", [])
    roles_from_list = config.get("roles", [])
    
    valid_users = set()
    
    # Add individual users
    for user in users_from_list:
        if is_valid_user(user):
            valid_users.add(user)
    
    # Add users from roles
    for role in roles_from_list:
        users_in_role = get_users_with_role(role)
        valid_users.update(users_in_role)
    
    return list(valid_users)

def is_valid_user(user):
    """Check if user exists and is enabled"""
    try:
        if not frappe.db.exists("User", user):
            return False
        
        user_enabled = frappe.db.get_value("User", user, "enabled")
        return bool(user_enabled)
        
    except Exception:
        return False

def get_users_with_role(role_name):
    """Get all enabled users with a specific role"""
    try:
        if not frappe.db.exists("Role", role_name):
            return []
        
        users = frappe.db.sql("""
            SELECT DISTINCT hr.parent as user
            FROM `tabHas Role` hr
            INNER JOIN `tabUser` u ON hr.parent = u.name
            WHERE hr.role = %s AND hr.parenttype = 'User' AND u.enabled = 1
        """, role_name, as_dict=True)
        
        return [user.user for user in users]
        
    except Exception:
        return []

def send_notification_to_users(users, subject, message, doc=None, channel="System Notification"):
    """Send notifications to multiple users"""
    if not users:
        return []
    
    notified_users = []
    
    for user in users:
        try:
            if send_single_notification(user, subject, message, doc, channel):
                notified_users.append(user)
        except Exception:
            continue
    
    return notified_users

def send_single_notification(user, subject, message, doc=None, channel="System Notification"):
    """Send notification to a single user"""
    try:
        if not is_valid_user(user):
            return False
        
        doc_type = doc.get('doctype', 'Notification') if doc else 'Notification'
        doc_name = doc.get('name', 'Notification') if doc else 'Notification'
        
        # Create Notification Log
        notification_log = frappe.get_doc({
            "doctype": "Notification Log",
            "subject": subject,
            "type": "Alert",
            "email_content": message,
            "document_type": doc_type,
            "document_name": doc_name,
            "for_user": user
        })
        notification_log.insert(ignore_permissions=True)
        
        # Publish realtime event
        publish_realtime_notification(user, subject, notification_log.name, doc_type, doc_name)
        
        # Send email if configured
        if channel == "Email":
            send_email_notification(user, subject, message, doc)
        
        return True
        
    except Exception:
        return False

def publish_realtime_notification(user, subject, notification_log_name, doc_type, doc_name):
    """Publish realtime notification event"""
    try:
        frappe.publish_realtime(
            event="new_notification",
            message={
                "type": "new_notice",
                "notification_log": notification_log_name,
                "for_user": user,
                "subject": subject,
                "document_type": doc_type,
                "document_name": doc_name,
                "timestamp": now()
            },
            user=user,
            after_commit=True
        )
    except Exception:
        pass

def send_email_notification(recipient, subject, message, reference_doc=None):
    """Send email notification"""
    try:
        frappe.sendmail(
            recipients=recipient,
            subject=subject,
            message=message,
            reference_doctype=reference_doc.get('doctype', 'Notification') if reference_doc else 'Notification',
            reference_name=reference_doc.get('name', 'Notification') if reference_doc else 'Notification',
            now=True
        )
    except Exception:
        pass


# --------- NOTIFY EACH DAY ONCE
# def has_been_notified_today(doc_type, doc_name, subject_pattern):
#     """Check if document was notified today"""
#     try:
#         existing = frappe.db.sql("""
#             SELECT 1 FROM `tabNotification Log`
#             WHERE document_type = %s AND document_name = %s 
#             AND creation >= CURDATE() AND subject LIKE %s
#             LIMIT 1
#         """, (doc_type, doc_name, f"%{subject_pattern}%"))
        
#         return bool(existing)
#     except Exception:
#         return False
    

# -----------   Never Notify Again    
def has_been_notified_ever(doc_type, doc_name, subject_pattern):
    """Check if document was EVER notified - never repeat notifications"""
    try:
        existing = frappe.db.sql("""
            SELECT 1 FROM `tabNotification Log`
            WHERE document_type = %s AND document_name = %s 
            AND subject LIKE %s
            LIMIT 1
        """, (doc_type, doc_name, f"%{subject_pattern}%"))
        
        return bool(existing)
    except Exception:
        return False