# daily_cash_flow.py
# Copyright (c) 2025, Rasiin and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, nowdate, flt, cint
import json

def execute(filters=None):
    if not filters:
        filters = {}
    
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart_data(data)
    
    # Calculate meaningful totals for the message
    message = get_custom_totals_message(data)
    
    return columns, data, message, chart


def get_custom_totals_message(data):
    """Simple version of custom totals"""
    if not data:
        return None
    
    transaction_data = [d for d in data if d.get('voucher_type') not in ['Opening Balance', 'Closing Balance']]
    
    total_cash_in = sum(flt(row.get('debit', 0)) for row in transaction_data)
    total_cash_out = sum(flt(row.get('credit', 0)) for row in transaction_data)
    
    opening_balance = next((flt(row.get('balance', 0)) for row in data if row.get('voucher_type') == 'Opening Balance'), 0)
    closing_balance = next((flt(row.get('balance', 0)) for row in data if row.get('voucher_type') == 'Closing Balance'), 0)
    
    message = f"""
    <div style='background: #f0f2f5; padding: 10px; border-radius: 5px; margin: 10px 0;'>
        <b>Summary:</b> 
        Opening: {hardcoded_format_currency(opening_balance)} | 
        Cash In: <span style='color: green'>{hardcoded_format_currency(total_cash_in)}</span> | 
        Cash Out: <span style='color: red'>{hardcoded_format_currency(total_cash_out)}</span> | 
        Closing: <span style='color: blue'>{hardcoded_format_currency(closing_balance)}</span>
    </div>
    """
    
    return message


def hardcoded_format_currency(amount, currency=None):
    """A simple, hardcoded currency formatter that uses a dollar sign."""
    try:
        # Format to 2 decimal places with thousand separators
        formatted_amount = "{:,.2f}".format(flt(amount))
        return f"$ {formatted_amount}"
    except (TypeError, ValueError):
        return "$ 0.00"


def get_columns():
    """Define report columns"""
    return [
        {
            "fieldname": "posting_date",
            "label": _("Date"),
            "fieldtype": "Date",
            "width": 100
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
            "fieldname": "party",
            "label": _("Party"),
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "debit",
            "label": _("Cash In"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "credit",
            "label": _("Cash Out"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "balance",
            "label": _("Running Balance"),
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "fieldname": "mode_of_payment",
            "label": _("Payment Mode"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "custom_refrence",
            "label": _("Reference"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "remarks",
            "label": _("Remarks"),
            "fieldtype": "Data",
            "width": 180
        }
    ]


def get_data(filters):
    """Fetch and process ONLY actual cash transactions"""
    
    conditions = get_conditions(filters)
    
    # Get cash and bank account names
    cash_bank_accounts = get_cash_bank_accounts(filters.get("account"))
    
    if not cash_bank_accounts:
        return []
    
    # Get opening balance
    opening_balance = get_opening_balance(filters, cash_bank_accounts)
    
    # MAIN QUERY - Only get transactions that represent actual cash movement
    # Exclude Sales Invoice and Purchase Invoice as they don't represent cash movement
    query = """
        SELECT 
            posting_date,
            voucher_type,
            voucher_no,
            party,
            debit,
            credit,
            against,
            remarks
        FROM `tabGL Entry`
        WHERE docstatus = 1 
        AND is_cancelled = 0
        AND account IN ({accounts})
        AND voucher_type NOT IN ('Sales Invoice', 'Purchase Invoice')  /* EXCLUDE INVOICES - they are accruals, not cash */
        {conditions}
        ORDER BY posting_date, creation
    """.format(
        accounts=", ".join(["%s"] * len(cash_bank_accounts)),
        conditions=conditions
    )
    
    try:
        data = frappe.db.sql(query, cash_bank_accounts, as_dict=1)
    except Exception as e:
        frappe.throw(_("Error fetching data: {0}").format(str(e)))
    
    # Process data and calculate running balance
    processed_data = process_data(data, opening_balance, filters)
    
    return processed_data


def get_cash_bank_accounts(specific_account=None):
    """Get list of cash and bank accounts"""
    if specific_account:
        return [specific_account]
    
    accounts = frappe.get_all("Account", 
        filters={
            "account_type": ["in", ["Cash", "Bank"]],
            "is_group": 0,
            "disabled": 0
        },
        pluck="name"
    )
    return accounts or []


def get_conditions(filters):
    """Build conditions based on filters"""
    conditions = []
    
    if filters.get("from_date"):
        conditions.append("posting_date >= '{0}'".format(filters.get("from_date")))
    if filters.get("to_date"):
        conditions.append("posting_date <= '{0}'".format(filters.get("to_date")))
    if filters.get("voucher_type"):
        conditions.append("voucher_type = '{0}'".format(filters.get("voucher_type")))
    if filters.get("party"):
        conditions.append("party = '{0}'".format(filters.get("party")))
    if filters.get("mode_of_payment"):
        # For Payment Entries, we'll filter in process_data
        conditions.append("(voucher_type != 'Payment Entry' OR 1=1)")  # Placeholder
    
    if conditions:
        return " AND " + " AND ".join(conditions)
    else:
        return ""


def get_opening_balance(filters, accounts):
    """Calculate opening balance before from_date"""
    if not filters.get("from_date"):
        return 0
    
    conditions = []
    if filters.get("voucher_type"):
        conditions.append("voucher_type = '{0}'".format(filters.get("voucher_type")))
    if filters.get("party"):
        conditions.append("party = '{0}'".format(filters.get("party")))
    
    # Add exclusion of invoices to opening balance calculation for consistency
    conditions.append("voucher_type NOT IN ('Sales Invoice', 'Purchase Invoice')")
    
    condition_str = " AND " + " AND ".join(conditions) if conditions else ""
    
    query = """
        SELECT 
            SUM(debit - credit) as opening_balance
        FROM `tabGL Entry`
        WHERE docstatus = 1 
        AND is_cancelled = 0
        AND posting_date < '{from_date}'
        AND account IN ({accounts})
        {conditions}
    """.format(
        from_date=filters.get("from_date"),
        accounts=", ".join(["%s"] * len(accounts)),
        conditions=condition_str
    )
    
    try:
        result = frappe.db.sql(query, accounts, as_dict=1)
        opening_balance = flt(result[0].get('opening_balance', 0)) if result else 0
    except Exception as e:
        frappe.log_error(f"Error calculating opening balance: {str(e)}")
        opening_balance = 0
    
    return opening_balance


def process_data(data, opening_balance, filters):
    """Process data and calculate running balance"""
    processed_data = []
    running_balance = opening_balance
    
    # Add opening balance row
    if filters.get("from_date"):
        opening_row = {
            "posting_date": filters.get("from_date"),
            "voucher_type": "Opening Balance",
            "voucher_no": "",
            "party": "",
            "debit": 0,
            "credit": 0,
            "balance": running_balance,
            "mode_of_payment": "",
            "custom_refrence": "",
            "remarks": "Opening Balance"
        }
        processed_data.append(opening_row)
    
    for row in data:
        # Skip if mode_of_payment filter doesn't match (for Payment Entries)
        if filters.get("mode_of_payment"):
            mop = get_mode_of_payment(row.voucher_type, row.voucher_no)
            if mop != filters.get("mode_of_payment"):
                continue
        
        # Calculate running balance
        running_balance += flt(row.debit) - flt(row.credit)
        
        # Get custom reference for Sales Invoice (though we exclude them now, keeping for other vouchers)
        custom_refrence = ""
        if row.voucher_type == "Sales Invoice" and row.voucher_no:
            custom_refrence = get_custom_refrence(row.voucher_type, row.voucher_no)
        
        processed_row = {
            "posting_date": row.posting_date,
            "voucher_type": row.voucher_type,
            "voucher_no": row.voucher_no,
            "party": row.party or "",
            "debit": flt(row.debit),
            "credit": flt(row.credit),
            "balance": running_balance,
            "mode_of_payment": get_mode_of_payment(row.voucher_type, row.voucher_no),
            "custom_refrence": custom_refrence,
            "remarks": row.remarks or row.against or ""
        }
        
        processed_data.append(processed_row)
    
    # Add closing balance row
    if processed_data:
        closing_row = {
            "posting_date": filters.get("to_date") or processed_data[-1]["posting_date"],
            "voucher_type": "Closing Balance",
            "voucher_no": "",
            "party": "",
            "debit": 0,
            "credit": 0,
            "balance": running_balance,
            "mode_of_payment": "",
            "custom_refrence": "",
            "remarks": "Closing Balance"
        }
        processed_data.append(closing_row)
    
    return processed_data


def get_mode_of_payment(voucher_type, voucher_no):
    """Get mode of payment for payment entries"""
    if voucher_type == "Payment Entry" and voucher_no:
        try:
            return frappe.db.get_value("Payment Entry", voucher_no, "mode_of_payment")
        except:
            return ""
    return ""


def get_custom_refrence(voucher_type, voucher_no):
    """Get custom_refrence field for Sales Invoice"""
    if voucher_type == "Sales Invoice" and voucher_no:
        try:
            # Replace 'custom_refrence' with the actual fieldname in your Sales Invoice
            return frappe.db.get_value("Sales Invoice", voucher_no, "custom_refrence") or ""
        except Exception:
            # In case the field doesn't exist or there's an error
            return ""
    return ""


def get_chart_data(data):
    """Prepare chart data for cash flow visualization"""
    if not data:
        return None
    
    # Filter out opening/closing balance rows for chart
    transaction_data = [d for d in data if d.get('voucher_type') not in ['Opening Balance', 'Closing Balance']]
    
    if not transaction_data:
        return None
    
    # Prepare daily summary for chart
    daily_summary = {}
    for row in transaction_data:
        date = row.get('posting_date')
        if date:
            date_str = date.strftime('%d-%m-%Y') if hasattr(date, 'strftime') else str(date)
            if date_str not in daily_summary:
                daily_summary[date_str] = {'cash_in': 0, 'cash_out': 0}
            daily_summary[date_str]['cash_in'] += flt(row.get('debit', 0))
            daily_summary[date_str]['cash_out'] += flt(row.get('credit', 0))
    
    dates = sorted(daily_summary.keys())
    
    chart = {
        "data": {
            "labels": dates,
            "datasets": [
                {
                    "name": "Cash In",
                    "values": [daily_summary[date]['cash_in'] for date in dates]
                },
                {
                    "name": "Cash Out", 
                    "values": [daily_summary[date]['cash_out'] for date in dates]
                }
            ]
        },
        "type": "bar",
        "colors": ["#28a745", "#dc3545"],
        "barOptions": {
            "stacked": False
        }
    }
    
    return chart


@frappe.whitelist()
def get_cash_flow_summary(filters):
    """Get cash flow summary for additional insights"""
    filters = json.loads(filters) if isinstance(filters, str) else filters
    
    # Get cash and bank accounts
    accounts = get_cash_bank_accounts(filters.get("account"))
    
    if not accounts:
        return {"voucher_summary": [], "top_cash_sources": []}
    
    account_placeholders = ", ".join(["%s"] * len(accounts))
    
    summary_query = """
        SELECT 
            voucher_type,
            COUNT(*) as total_transactions,
            SUM(debit) as total_cash_in,
            SUM(credit) as total_cash_out,
            SUM(debit - credit) as net_cash_flow
        FROM `tabGL Entry`
        WHERE docstatus = 1 
        AND is_cancelled = 0
        AND posting_date BETWEEN %s AND %s
        AND account IN ({accounts})
        AND voucher_type NOT IN ('Sales Invoice', 'Purchase Invoice')  /* Exclude invoices */
        GROUP BY voucher_type
        ORDER BY total_cash_in DESC
    """.format(accounts=account_placeholders)
    
    summary_data = frappe.db.sql(summary_query, [filters.get("from_date"), filters.get("to_date")] + accounts, as_dict=1)
    
    # Top cash sources
    cash_sources_query = """
        SELECT 
            party,
            SUM(debit) as total_received
        FROM `tabGL Entry`
        WHERE docstatus = 1 
        AND is_cancelled = 0
        AND posting_date BETWEEN %s AND %s
        AND debit > 0
        AND account IN ({accounts})
        AND voucher_type NOT IN ('Sales Invoice', 'Purchase Invoice')  /* Exclude invoices */
        GROUP BY party
        ORDER BY total_received DESC
        LIMIT 10
    """.format(accounts=account_placeholders)
    
    cash_sources = frappe.db.sql(cash_sources_query, [filters.get("from_date"), filters.get("to_date")] + accounts, as_dict=1)
    
    return {
        "voucher_summary": summary_data or [],
        "top_cash_sources": cash_sources or []
    }