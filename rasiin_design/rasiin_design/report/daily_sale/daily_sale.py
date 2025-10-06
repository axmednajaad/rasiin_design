# daily_sale.py
# Copyright (c) 2025, Rasiin and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, nowdate, flt, cint
import json
from datetime import datetime, timedelta

def execute(filters=None):
    if not filters:
        filters = {}
    
    columns = get_columns(filters)
    data = get_data(filters)
    
    return columns, data
def get_columns(filters):
    """Define report columns"""
    columns = [
        {
            "fieldname": "posting_date",
            "label": _("Date"),
            "fieldtype": "Date",
            "width": 100
        },
        {
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": 120
        },
        {
            "fieldname": "customer_name",
            "label": _("Customer Name"),
            "fieldtype": "Data",
            "width": 180
        },
        {
            "fieldname": "voucher_type",
            "label": _("Voucher Type"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "voucher_no",
            "label": _("Voucher No"),
            "fieldtype": "Dynamic Link",
            "options": "voucher_type",
            "width": 140
        },
        {
            "fieldname": "discount_amount",
            "label": _("Discount Amount"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "total_amount",
            "label": _("Total Amount"),
            "fieldtype": "Currency",
            "width": 120
        }
    ]
    
    # Add paid amount column
    columns.append({
        "fieldname": "paid_amount",
        "label": _("Paid Amount"),
        "fieldtype": "Currency",
        "width": 120
    })
    
    # Add outstanding amount column if enabled
    if filters.get("show_outstanding"):
        columns.append({
            "fieldname": "outstanding_amount",
            "label": _("Outstanding Amount"),
            "fieldtype": "Currency",
            "width": 130
        })
    
    columns.extend([
        {
            "fieldname": "payment_mode",
            "label": _("Payment Mode"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "custom_refrence",
            "label": _("Reference"),
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "sales_person",
            "label": _("Sales Person"),
            "fieldtype": "Data",
            "width": 120
        }
    ])
    
    return columns

def get_data(filters):
    """Fetch and process sales data based on filters"""
    
    conditions, condition_values = get_conditions(filters)
    
    # Main query to get sales data grouped by invoice
    outstanding_field = ", si.outstanding_amount" if filters.get("show_outstanding") else ""
    
    query = """
        SELECT 
            si.posting_date,
            si.customer,
            si.customer_name,
            'Sales Invoice' as voucher_type,
            si.name as voucher_no,
            si.discount_amount,
            si.grand_total as total_amount,
            (si.grand_total - si.outstanding_amount) as paid_amount
            {outstanding_field},
            (SELECT GROUP_CONCAT(sip.mode_of_payment SEPARATOR ', ') 
             FROM `tabSales Invoice Payment` sip 
             WHERE sip.parent = si.name) as payment_mode,
             si.custom_refrence as custom_refrence,
            (SELECT GROUP_CONCAT(DISTINCT sp.sales_person SEPARATOR ', ') 
             FROM `tabSales Team` sp 
             WHERE sp.parent = si.name) as sales_person
        FROM `tabSales Invoice` si
        WHERE si.docstatus = 1 {conditions}
        ORDER BY si.posting_date DESC, si.name
    """.format(
        outstanding_field=outstanding_field,
        conditions=conditions
    )
    
    try:
        data = frappe.db.sql(query, condition_values, as_dict=1)
    except Exception as e:
        frappe.throw(_("Error fetching data: {0}").format(str(e)))
    
    # Process and enhance data
    processed_data = process_data(data, filters)
    
    return processed_data

def get_conditions(filters):
    """Build conditions based on filters"""
    conditions = []
    condition_values = {}
    
    if filters.get("from_date"):
        conditions.append("si.posting_date >= %(from_date)s")
        condition_values["from_date"] = filters.get("from_date")
    if filters.get("to_date"):
        conditions.append("si.posting_date <= %(to_date)s")
        condition_values["to_date"] = filters.get("to_date")
    if filters.get("customer"):
        conditions.append("si.customer = %(customer)s")
        condition_values["customer"] = filters.get("customer")
    if filters.get("sales_person"):
        conditions.append("si.name IN (SELECT parent FROM `tabSales Team` WHERE sales_person = %(sales_person)s)")
        condition_values["sales_person"] = filters.get("sales_person")
    
    # FIX: Properly handle empty conditions
    if conditions:
        conditions_str = " AND " + " AND ".join(conditions)
    else:
        conditions_str = ""
    
    return conditions_str, condition_values

def process_data(data, filters):
    """Process and enhance the raw data"""
    processed_data = []
    
    for row in data:
        # Ensure numeric values
        row.discount_amount = flt(row.discount_amount)
        row.total_amount = flt(row.total_amount)
        row.paid_amount = flt(row.paid_amount)
        
        # Calculate outstanding amount if not already included
        if filters.get("show_outstanding") and 'outstanding_amount' not in row:
            row.outstanding_amount = get_outstanding_amount(row.voucher_no)
        elif filters.get("show_outstanding"):
            row.outstanding_amount = flt(row.outstanding_amount)
        
        # Format payment mode and sales person for better display
        if row.payment_mode:
            row.payment_mode = row.payment_mode.replace(',', ', ')
        if row.sales_person:
            row.sales_person = row.sales_person.replace(',', ', ')
        
        # Ensure custom_refrence is properly handled
        if not hasattr(row, 'custom_refrence') or row.custom_refrence is None:
            row.custom_refrence = ""
        
        processed_data.append(row)
    
    return processed_data

def get_outstanding_amount(invoice_no):
    """Get outstanding amount for a sales invoice"""
    try:
        return frappe.db.get_value("Sales Invoice", invoice_no, "outstanding_amount") or 0
    except:
        return 0

@frappe.whitelist()
def get_chart_data(filters):
    """Get data for charts, respecting all filters"""
    filters = json.loads(filters) if isinstance(filters, str) else filters
    conditions, condition_values = get_conditions(filters)

    # Daily sales trend
    daily_trend_query = """
        SELECT 
            si.posting_date as date,
            SUM(si.grand_total) as amount,
            SUM(si.discount_amount) as discount
        FROM `tabSales Invoice` si
        WHERE si.docstatus = 1 {conditions}
        GROUP BY si.posting_date
        ORDER BY si.posting_date
    """.format(conditions=conditions)
    
    try:
        daily_data = frappe.db.sql(daily_trend_query, condition_values, as_dict=1)
        
        # Ensure all values are floats for charting
        for item in daily_data:
            item['amount'] = flt(item.get('amount', 0))
            item['discount'] = flt(item.get('discount', 0))
    except Exception as e:
        frappe.log_error(f"Error in daily trend chart: {str(e)}")
        daily_data = []

    # Sales by customer
    customer_sales_query = """
        SELECT 
            si.customer,
            si.customer_name,
            SUM(si.grand_total) as total_sales
        FROM `tabSales Invoice` si
        WHERE si.docstatus = 1 {conditions}
        GROUP BY si.customer, si.customer_name
        ORDER BY total_sales DESC
        LIMIT 10
    """.format(conditions=conditions)
    
    try:
        customer_data = frappe.db.sql(customer_sales_query, condition_values, as_dict=1)
        
        # Ensure all values are floats for charting
        for item in customer_data:
            item['total_sales'] = flt(item.get('total_sales', 0))
    except Exception as e:
        frappe.log_error(f"Error in customer chart: {str(e)}")
        customer_data = []
    
    return {
        "daily_trend": daily_data or [],
        "top_customers": customer_data or []
    }

@frappe.whitelist()
def get_outstanding_summary(filters):
    """Get outstanding amount summary"""
    filters = json.loads(filters) if isinstance(filters, str) else filters
    conditions, condition_values = get_conditions(filters)
    
    # Customer outstanding summary
    customer_outstanding_query = """
        SELECT 
            si.customer,
            si.customer_name,
            SUM(si.grand_total) as total_sales,
            SUM(si.outstanding_amount) as outstanding_amount,
            SUM(si.grand_total - si.outstanding_amount) as total_paid
        FROM `tabSales Invoice` si
        WHERE si.docstatus = 1 {conditions}
        GROUP BY si.customer, si.customer_name
        HAVING outstanding_amount != 0
        ORDER BY outstanding_amount DESC
    """.format(conditions=conditions)
    
    try:
        customer_outstanding = frappe.db.sql(customer_outstanding_query, condition_values, as_dict=1)
        
        # Calculate total outstanding
        total_outstanding = sum(flt(item.get('outstanding_amount', 0)) for item in customer_outstanding)
        
        # Calculate aging summary
        aging_summary = get_aging_summary(filters)
        
    except Exception as e:
        frappe.log_error(f"Error in outstanding summary: {str(e)}")
        customer_outstanding = []
        total_outstanding = 0
        aging_summary = {}
    
    return {
        "customer_outstanding": customer_outstanding,
        "total_outstanding": total_outstanding,
        "aging_summary": aging_summary
    }

def get_aging_summary(filters):
    """Get aging analysis for outstanding amounts"""
    conditions, condition_values = get_conditions(filters)
    
    # Get current date for aging calculation
    current_date = getdate(nowdate())
    
    aging_query = """
        SELECT 
            si.name,
            si.posting_date,
            si.outstanding_amount
        FROM `tabSales Invoice` si
        WHERE si.docstatus = 1 
        AND si.outstanding_amount > 0
        {conditions}
    """.format(conditions=conditions)
    
    try:
        aging_data = frappe.db.sql(aging_query, condition_values, as_dict=1)
        
        range1 = range2 = range3 = range4 = 0  # 0-30, 31-60, 61-90, 90+ days
        
        for invoice in aging_data:
            posting_date = getdate(invoice.get('posting_date'))
            days_old = (current_date - posting_date).days
            outstanding = flt(invoice.get('outstanding_amount', 0))
            
            if days_old <= 30:
                range1 += outstanding
            elif days_old <= 60:
                range2 += outstanding
            elif days_old <= 90:
                range3 += outstanding
            else:
                range4 += outstanding
                
    except Exception as e:
        frappe.log_error(f"Error in aging analysis: {str(e)}")
        range1 = range2 = range3 = range4 = 0
    
    return {
        "range1": range1,
        "range2": range2,
        "range3": range3,
        "range4": range4
    }