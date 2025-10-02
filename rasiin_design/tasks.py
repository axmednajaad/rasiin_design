# scheduled_tasks.py
import frappe
from frappe.utils import now, today, format_date
from frappe import _

from rasiin_design.utils.notification_utils import (
    send_notification_to_users,
    get_notification_users,
    # has_been_notified_today
    has_been_notified_ever
)

def check_and_notify_overdue_invoices():
    """Check for overdue invoices and send notifications"""
    try:
        overdue_invoices = frappe.db.sql("""
            SELECT name, customer, customer_name, due_date, outstanding_amount, 
                   currency, DATEDIFF(CURDATE(), due_date) as days_overdue
            FROM `tabSales Invoice`
            WHERE docstatus = 1 AND outstanding_amount > 0 AND due_date < CURDATE()
        """, as_dict=1)
        
        frappe.logger().info(f"Found {len(overdue_invoices)} overdue invoices")
        
        notified_count = 0
        for invoice in overdue_invoices:
            try:
                # if has_been_notified_today("Sales Invoice", invoice.name, "Overdue"):
                if has_been_notified_ever("Sales Invoice", invoice.name, "Overdue"):
                    continue
                
                if send_overdue_notification(invoice):
                    notified_count += 1
                    frappe.db.commit()
                
            except Exception as e:
                frappe.log_error(f"Error notifying invoice {invoice.name}: {str(e)}")
                frappe.db.rollback()
        
        frappe.logger().info(f"Sent notifications for {notified_count} invoices")
        
    except Exception as e:
        frappe.log_error(f"Error in overdue invoice check: {str(e)}")

def send_overdue_notification(invoice):
    """Send overdue notification"""
    try:
        subject = _("🔔 Overdue Invoice: {0} - {1} due {2}").format(
            invoice.name, 
            format_currency(invoice.outstanding_amount, invoice.currency),
            format_date(invoice.due_date)
        )
        
        message = _("""
Overdue Invoice Alert

Invoice: {invoice_name}
Customer: {customer}
Due Date: {due_date} ({days_overdue} days overdue)
Amount Due: {outstanding_amount}

Please follow up with the customer for payment.
        """).format(
            invoice_name=invoice.name,
            customer=invoice.customer,
            due_date=format_date(invoice.due_date),
            days_overdue=invoice.days_overdue,
            outstanding_amount=format_currency(invoice.outstanding_amount, invoice.currency)
        )
        
        users = get_notification_users("overdue")
        doc_ref = frappe._dict({'doctype': 'Sales Invoice', 'name': invoice.name})
        
        result = send_notification_to_users(users, subject, message, doc_ref, "System Notification")
        return len(result) > 0
        
    except Exception as e:
        frappe.log_error(f"Error sending overdue notification: {str(e)}")
        return False

def check_and_notify_low_stock():
    """Check for low stock items and send notifications"""
    try:
        low_stock_items = frappe.db.sql("""
            SELECT bin.item_code, bin.warehouse, bin.actual_qty,
                   item.item_name, item.stock_uom, ware.warehouse_name
            FROM `tabBin` bin
            INNER JOIN `tabItem` item ON bin.item_code = item.name
            INNER JOIN `tabWarehouse` ware ON bin.warehouse = ware.name
            WHERE bin.actual_qty <= 10 AND bin.actual_qty > 0 AND item.disabled = 0
        """, as_dict=1)
        
        frappe.logger().info(f"Found {len(low_stock_items)} low stock items")
        
        notified_count = 0
        for item in low_stock_items:
            try:
                doc_name = f"{item.item_code}-{item.warehouse}"
                
                # if has_been_notified_today("Bin", doc_name, "Low Stock"):
                if has_been_notified_ever("Bin", doc_name, "Low Stock"):
                    continue
                
                if send_low_stock_notification(item):
                    notified_count += 1
                    frappe.db.commit()
                
            except Exception as e:
                frappe.log_error(f"Error notifying low stock: {str(e)}")
                frappe.db.rollback()
        
        frappe.logger().info(f"Sent notifications for {notified_count} low stock items")
        
    except Exception as e:
        frappe.log_error(f"Error in low stock check: {str(e)}")

def send_low_stock_notification(item):
    """Send low stock notification"""
    try:
        subject = _("⚠️ Low Stock: {0} - {1} {2} left").format(
            item.item_code, item.actual_qty, item.stock_uom
        )
        
        message = _("""
Low Stock Alert

Item: {item_code} - {item_name}
Warehouse: {warehouse}
Current Stock: {actual_qty} {stock_uom}

Please consider restocking to avoid stockouts.
        """).format(
            item_code=item.item_code,
            item_name=item.item_name,
            warehouse=item.warehouse,
            actual_qty=item.actual_qty,
            stock_uom=item.stock_uom
        )
        
        users = get_notification_users("low_stock")
        doc_ref = frappe._dict({'doctype': 'Bin', 'name': f"{item.item_code}-{item.warehouse}"})
        
        result = send_notification_to_users(users, subject, message, doc_ref, "System Notification")
        return len(result) > 0
        
    except Exception as e:
        frappe.log_error(f"Error sending low stock notification: {str(e)}")
        return False

def format_currency(amount, currency):
    """Format currency amount"""
    try:
        return frappe.format_value(amount, {'fieldtype': 'Currency', 'options': currency})
    except:
        return f"{amount} {currency}"

# Manual triggers for testing
@frappe.whitelist()
def trigger_overdue_check():
    check_and_notify_overdue_invoices()
    return "Overdue check completed"

@frappe.whitelist()
def trigger_low_stock_check():
    check_and_notify_low_stock()
    return "Low stock check completed"

