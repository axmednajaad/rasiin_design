from . import __version__ as app_version

app_name = "rasiin_design"
app_title = "Rasiin Design"
app_publisher = "Rasiin"
app_description = "Rasiin Design"
app_email = "rasiin@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = [
    "/assets/rasiin_design/css/new_app_page.css" , 
    "/assets/rasiin_design/css/new_design.css" , 
    "/assets/rasiin_design/css/anfac_retailss.css" , 
    "/assets/rasiin_design/css/first-page.css" ,
    '/assets/rasiin_design/js/lib/tabulator/dist/css/tabulator.min.css',
    '/assets/rasiin_design/js/lib/tabulator/dist/css/tabulator_simple.min.css',
    '/assets/rasiin_design/js/lib/fontawesome/css/all.min.css'
    
    # '/assets/rasiin_design/js/lib/tailwind/index.css'
    # ,
     

    
   
      
      
      
        ]


app_include_js = [
    "/assets/rasiin_design/js/new_design.js" ,
    "/assets/rasiin_design/js/customreport.js" , 
    '/assets/rasiin_design/js/lib/tabulator/dist/js/tabulator.min.js',
     '/assets/rasiin_design/js/lib/tailwind.js'
    
    ]

# ,"/assets/rasiin_design/js/customform.js"
# include js, css files in header of web template
# web_include_css = "/assets/rasiin_design/css/rasiin_design.css"
# web_include_js = "/assets/rasiin_design/js/rasiin_design.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "rasiin_design/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "rasiin_design.utils.jinja_methods",
#	"filters": "rasiin_design.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "rasiin_design.install.before_install"
# after_install = "rasiin_design.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "rasiin_design.uninstall.before_uninstall"
# after_uninstall = "rasiin_design.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "rasiin_design.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"rasiin_design.tasks.all"
#	],
#	"daily": [
#		"rasiin_design.tasks.daily"
#	],
#	"hourly": [
#		"rasiin_design.tasks.hourly"
#	],
#	"weekly": [
#		"rasiin_design.tasks.weekly"
#	],
#	"monthly": [
#		"rasiin_design.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "rasiin_design.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "rasiin_design.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "rasiin_design.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"rasiin_design.auth.validate"
# ]
