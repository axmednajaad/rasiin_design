import frappe
from frappe.utils import nowdate, add_days

def trigger_overdue_notifications():
    """Force-trigger notifications for invoices that became overdue via scheduled job"""
    # Get invoices that became overdue in the last day AND haven't been notified recently
    overdue_invoices = frappe.get_all("Sales Invoice", 
        filters={
            "status": "Overdue", 
            "docstatus": 1, 
            "modified": [">", add_days(nowdate(), -1)],
            "posting_date": [">", add_days(nowdate(), -30)]  # Only recent invoices
        },
        fields=["name", "modified"]
    )
    
    notified_count = 0
    for inv in overdue_invoices:
        try:
            # Check if notification was already sent recently
            existing_notification = frappe.get_all("Notification Log",
                filters={
                    "document_type": "Sales Invoice",
                    "document_name": inv.name,
                    "creation": [">", add_days(nowdate(), -1)]
                },
                limit=1
            )
            
            if not existing_notification:
                doc = frappe.get_doc("Sales Invoice", inv.name)
                doc.save(ignore_permissions=True)
                notified_count += 1
                
            frappe.db.commit()
            
        except Exception as e:
            frappe.log_error(f"Error triggering notification for {inv.name}: {str(e)}")
            frappe.db.rollback()
    
    frappe.logger().info(f"Triggered overdue notifications for {notified_count} invoices")

def check_low_stock_and_notify():
    """Alternative approach for low stock alerts that might be more efficient"""
    # You can also implement a direct notification approach here if needed
    pass