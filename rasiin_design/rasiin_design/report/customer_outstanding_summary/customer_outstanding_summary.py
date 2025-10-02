# Copyright (c) 2025, Rasiin and contributors
# For license information, please see license.txt

# import frappe


# def execute(filters=None):
# 	columns, data = [], []
# 	return columns, data


# customers_outstanding_report.py
import frappe
from erpnext.accounts.utils import get_balance_on

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 200},
        {"label": "Customer Name", "fieldname": "customer_name", "fieldtype": "Data", "width": 200},
        {"label": "Mobile Number", "fieldname": "mobile_number", "fieldtype": "Data", "width": 150},
        {"label": "Outstanding Amount", "fieldname": "outstanding_amount", "fieldtype": "Currency", "width": 150},
    ]

def get_data(filters):
    company = filters.get('company') or frappe.defaults.get_user_default("company")
    
    customers = frappe.get_all('Customer', 
        fields=['name', 'customer_name', 'custom_mobile_number', 'default_currency'],
        filters={'disabled': 0}  # Only active customers
    )
    
    data = []
    for customer in customers:
        balance = get_balance_on(
            party_type='Customer',
            party=customer.name,
            company=company,
            date=filters.get('as_on_date')  # Optional date filter
        )
        
        if balance != 0:  # Only include customers with balance
            data.append({
                'customer': customer.name,
                'customer_name': customer.customer_name,
                'mobile_number': customer.custom_mobile_number,
                'outstanding_amount': balance,
            })
    
    # Sort by outstanding amount descending
    return sorted(data, key=lambda x: x['outstanding_amount'], reverse=True)