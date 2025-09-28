from ast import List
import dis
# from msilib.text import tables
from xmlrpc.client import Boolean
import frappe
from collections import defaultdict
import frappe
from frappe.utils import getdate
from frappe.desk.query_report import run


from frappe.utils.pdf import get_pdf
from frappe.www.printview import get_print_style
from frappe.utils import getdate
company = frappe.defaults.get_user_default("company")
abbr    = frappe.db.get_value("Company" , company , "abbr")
curren =  frappe.db.get_value("Company" , company , "default_currency")
base_template_path = "frappe/www/printview.html"





