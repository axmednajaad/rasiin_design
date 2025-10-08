import frappe 
from frappe.utils import getdate
# from anfac_retail.anfac_retail.page.dashboard_page.dashboard_page import get_data
# from frappe.desk.desktop import get_workspace_sidebar_items
# import matplotlib.pyplot as plt
# from random import randrange
# import random

# @frappe.whitelist()
# def get_html():
#     data = get_data("2022-1-11" , "2022-11-20")
#     # frappe.errprint(get_balance_shet())
#     return frappe.render_template("anfac_retail/api/templates/dashboard_workspace.html", {"data" : data}) , get_prof_and_los() , get_balance_shet()
#     # return frappe.render_template("anfac_retail.anfac_retail.page.dashboard_page.dashboard_page.html", {"data" : data})
def has_role(user, role):
    roles = frappe.get_roles(user)
    return role in roles

@frappe.whitelist()
def get_workspace_sidebar_items():
	"""Get list of sidebar items for desk"""

	has_access =1
	# don't get domain restricted pages
	allowed_modules = []
	if frappe.db.exists("User Home", frappe.session.user, cache=True):
		user_page = frappe.get_doc("User Home", frappe.session.user).allowed_modules
		
		for page in user_page:
			allowed_modules.append(page.module)
	
	
	filters = {
	
		"name": ["in", allowed_modules],
		# "image_icon" :  ["!=", ""]
	 }

	if frappe.session.user == "Administrator" or has_role(frappe.session.user , "Full Admin"):
		filters = {}
	
	# pages sorted based on sequence id
	order_by = "name asc"
	fields = ["name", "label", 'color',  "module", "icon", "image_icon"]
	all_pages = frappe.get_all(
		"Home Page", fields=fields, filters=filters, order_by=order_by, ignore_permissions=True
	)
	pages = []
	private_pages = []

	# Filter Page based on Permission
	# for page in all_pages:
	# 	try:
	# 		workspace = Workspace(page, True)
	# 		if has_access or workspace.is_permitted():
	# 			if page.public:
	# 				pages.append(page)
	# 			elif page.for_user == frappe.session.user:
	# 				private_pages.append(page)
	# 			page["label"] = _(page.get("name"))
	# 	except frappe.PermissionError:
	# 		pass
	# if private_pages:
	# 	pages.extend(private_pages)

	return {"pages": all_pages, "has_access": has_access}


@frappe.whitelist()
def app_page():
	# data = get_data("2022-1-11" , "2022-11-20")
	# frappe.errprint(get_balance_shet())
	data = get_workspace_sidebar_items()['pages']
	# frappe.errprint(data)
	# return frappe.render_template("rasiin_design/api/templates/new_app_page.html", {"data" : data})  , "test"


	renderedTemplate = frappe.render_template("rasiin_design/api/templates/new_app_page.html", {"data" : data});

	return [renderedTemplate,data];

	# return frappe.render_template("anfac_retail.anfac_retail.page.dashboard_page.dashboard_page.html", {"data" : data})




