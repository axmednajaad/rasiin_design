from ast import List
import dis
from distutils.command.build_scripts import first_line_re
from hmac import new
# from msilib.text import tables
from xmlrpc.client import Boolean
import frappe
from collections import defaultdict
import frappe
from frappe.utils import getdate
from frappe.desk.query_report import run
import re
from datetime import datetime


from frappe.utils.pdf import get_pdf
from frappe.www.printview import get_print_style
from frappe.utils import getdate
company = frappe.defaults.get_user_default("company")
abbr    = frappe.db.get_value("Company" , company , "abbr")
curren =  frappe.db.get_value("Company" , company , "default_currency")
base_template_path = "frappe/www/printview.html"
pattern = r'[^A-Za-z0-9 ]'
@frappe.whitelist()
def get_report_design(from_date =  getdate() , to_date = getdate() ,withsidebar = 1 , loading = 1):
	
	series = [
		{
			"name": 'Browsers',
			"genderByPoint": "true",
			"data": [
				{
					"name": 'Chrome',
					"y": 63.06,
					"drilldown": 'Chrome'
				},
				{
					"name": 'Safari',
					"y": 19.84,
					"drilldown": 'Safari'
				},
				{
					"name": 'Firefox',
					"y": 4.18,
					"drilldown": 'Firefox'
				},
				{
					"name": 'Edge',
					"y": 4.12,
					"drilldown": 'Edge'
				},
				{
					"name": 'Opera',
					"y": 2.33,
					"drilldown": 'Opera'
				},
				{
					"name": 'Internet Explorer',
					"y": 0.45,
					"drilldown": 'Internet Explorer'
				},
				{
					"name": 'Other',
					"y": 1.582,
					"drilldown": "null"
				}
			]
		}
	],
   
	data = [{
		"name": 'Customer Support',
		"y": 21.3
	}, {
		"name": 'Development',
		"y": 18.7
	}, {
		"name": 'Sales',
		"y": 20.2
	}, {
		"name": 'Marketing',
		"y": 14.2
	}, {
		"name": 'Other',
		"y": 25.6
	}
	]
	
	summaries = [
		{
			"icon" :"fa-solid fa-bed",
			"title" :"OPD Income",
			"data" : 250
		},
		{
			"icon" :"fa-solid fa-bed",
			"title" :"OPD Income",
			"data" : 250
		},
		{
			"icon" :"fa-solid fa-bed",
			"title" :"OPD Income",
			"data" : 250
		},
		{
			"icon" :"fa-solid fa-bed",
			"title" :"OPD Income",
			"data" : 250
		},
		{
			"icon" :"fa-solid fa-bed",
			"title" :"OPD Income",
			"data" : 250
		},
		{
			"icon" :"fa-solid fa-bed",
			"title" :"OPD Income",
			"data" : 250
		},
		{
			"icon" :"fa-solid fa-bed",
			"title" :"OPD Income",
			"data" : 250
		}
	]
	table =[
		{
			"columns":[
	{"title":"Name", "field":"name"},
	{"title":"Progress", "field":"progress",},
	{"title":"Gender", "field":"gender"},
	{"title":"Rating", "field":"rating", },
	{"title":"Favourite gender", "field":"id"},
	{"title":"Date Of Birth", "field":"age"},
	{"title":"Driver", "field":"car"},
	],
	"data" :[
	{"id":1, "name":"Brie", "progress":"mould", "age":"4 weeks", "gender":"white", "gender":"brie.jpg"},
	{"id":1, "name":"Brie", "progress":"mould", "age":"4 weeks", "gender":"white", "gender":"brie.jpg"},
	{"id":1, "name":"Brie", "progress":"mould", "age":"4 weeks", "gender":"white", "gender":"brie.jpg"},
	
]
		}
	]
   
   
	yAxis = "Total market Sheet"
	drilldown = {
		"breadcrumbs": {
			"position": {
				"align": 'right'
			}
		},
		"series": [
			{
				"name": 'Chrome',
				"id": 'Chrome',
				"data": [
					[
						'v65.0',
						0.1
					],
					[
						'v64.0',
						1.3
					],
					[
						'v63.0',
						53.02
					],
					[
						'v62.0',
						1.4
					],
					[
						'v61.0',
						0.88
					],
					[
						'v60.0',
						0.56
					],
					[
						'v59.0',
						0.45
					],
					[
						'v58.0',
						0.49
					],
					[
						'v57.0',
						0.32
					],
					[
						'v56.0',
						0.29
					]
				]
			},
			{
				"name": 'Firefox',
				"id": 'Firefox',
				"data": [
					[
						'v58.0',
						1.02
					],
					[
						'v57.0',
						7.36
					]
				]
			},
			{
				"name": 'Internet Explorer',
				"id": 'Internet Explorer',
				"data": [
					[
						'v11.0',
						6.2
					],
					[
						'v10.0',
						0.29
					]
				]
			},
			{
				"name": 'Safari',
				"id": 'Safari',
				"data": [
					[
						'v11.0',
						3.39
					],
					[
						'v10.1',
						0.96
					],
					[
						'v10.0',
						0.36
					]
				]
			},
			{
				"name": 'Edge',
				"id": 'Edge',
				"data": [
					[
						'v16',
						2.6
					],
					[
						'v15',
						0.92
					]
				]
			},
			{
				"name": 'Opera',
				"id": 'Opera',
				"data": [
					[
						'v50.0',
						0.96
					],
					[
						'v49.0',
						0.82
					],
					[
						'v12.1',
						0.14
					]
				]
			}
		]
	}
	
	
	charts = [
	{
	"chart_type" : "column",
	"series" : series,
	"drilldown" : drilldown,
	"chart_title" : "Column  Chart ",
	"chart_subtitle" : "clickc to know more",
	"yAxis" : yAxis 
	},
	{
		"chart_type" :"pie",
		"data" : data,
		"chart_title" : "Pie Chart ",
		"chart_subtitle" : "clickc to know more"
	}
	]
	report_html_data = frappe.render_template(
	"rasiin_design/templates/Report/report.html",
	{

	  "withsidebar" : int(withsidebar),
	  "charts" : charts,
	  "summaries": summaries,
	  "table": table,
	  "loading": int(loading)
	}
	)
	html = frappe.render_template(
		base_template_path,
		{"body": report_html_data ,"css" : get_print_style() , "title": "Statement For "},
	)
	# if view:
	return report_html_data
	# return get_pdf(report_html_data , {"orientation": "Landscape"})


def get_inpatient_due_total(status,total=1):
	report_gl = frappe.get_doc("Report", "Inpatient Due")
	report_gl_filters = {
			"status": status,
			"range1":"30",
			"range2": "60",
			"range3": "90",
			"range4": "120",            
		   
		}
	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator", filters=report_gl_filters, as_dict=True)
	if data:
		if total:
			return data[-1]
	if data:
		return data[:-1]
@frappe.whitelist()   
def get_inpatient_due(status, from_date =  getdate() , to_date = getdate() ,withsidebar = 1 , loading = 1):

 
	totals = get_inpatient_due_total(status)

	list_inpatient_due = get_inpatient_due_total(status,0)

	data = []
	keys = {'paid_amount' : 'Cash' ,'outstanding_amount' : 'Credit' }
	if totals:
		for k in totals:
			if k in keys:
				data.append({
					"name": keys[k],
					"y":  totals[k]
				})
	

	
	summaries = []
	# discts = {}
	if totals:
		keys = {'invoiced' : 'Total Invoiced' ,'paid' : 'Total Paid','outstanding' : 'Total Balance' }
		for key, value in totals.items():
			if key in keys:
				summaries.append({
				"icon": "fa fa-money",
				"title": keys[key],
				"data": value
				})

	
	table =[
		{
			"columns":[
	{"title":"Patient Name", "field":"party_name"},
	{"title":"Mobile No", "field":"mobile_no"},
	{"title":"Invoiced", "field":"invoiced"},
	{"title":"Paid", "field":"paid"},
	{"title":"Balance", "field":"outstanding"},
	{"title":"Admited Date", "field":"admited_date"},
	{"title":"Discharged Date", "field":"discharged_date"},
	{"title":"Reciept", "field":"receipt","formatter":"html"},
	],
	"data" :list_inpatient_due
		}
	]
   

	yAxis = "Total Sales"

	
 
	
	report_html_data = frappe.render_template(
	"rasiin_design/templates/Report/report.html",
	{

	  "withsidebar" : int(withsidebar),
	  "charts" :[],
	  "summaries": summaries,
	  "table": table,
	  "loading": int(loading)
	}
	)
	html = frappe.render_template(
		base_template_path,
		{"body": report_html_data ,"css" : get_print_style() , "title": "Statement For "},
	)
	# if view:
	return report_html_data
	# return get_pdf(report_html_data , {"orientation": "Landscape"})



@frappe.whitelist()
def get_report_sales_return(from_date =  getdate() , to_date = getdate() ,withsidebar = 1 , loading = 1):
	# from_date = getdate(from_date)
	# to_date = getdate(to_date)
	source_order = frappe.db.get_list("Source Order" , pluck = "name")
   
	data_chart = []
 
	totals = get_total_sales_return(from_date , to_date)
	sales = []
	if source_order:
		for src in source_order:
			source_sales = get_total_sales_by_source_return(src , from_date , to_date)
			if source_sales:
				sales.append({src:source_sales})

	
	

	data = []
	keys = {'paid_amount' : 'Cash' ,'outstanding_amount' : 'Credit' }
	if totals:
		for k in totals:
			if k in keys:
				data.append({
					"name": keys[k],
					"y":  totals[k]
				})
	

	
	summaries = []
	# discts = {}
	# frappe.errprint(data)
	maping_keys = {'net_total' :'Total Sales Return' }
	if totals:
		for key, value in totals.items():
			if key in maping_keys:
				summaries.append({
				"icon": "fa fa-money",
				"title": maping_keys[key],
				"data": value
				})
				for sale in sales:
					
					for k , v in sale.items():
						# if key in v:
					
						summaries.append({
							"icon": "fa fa-money",
							"title": k + ' ' + maping_keys[key].split()[2],
							"data": v[key]
							})
		  
	  
		
		# summaries.append(discts)
	sales_per = sales_return_per_user(from_date , to_date)
	data_chart =[]
	drildown_chart = []
	if sales_per:
		for user in sales_per:
			data_chart.append({
					"name": user.source_order,
					# "name" : user.owner,
					"y": user.net_total ,
					"drilldown": user.source_order
				})
			
			drildown_chart.append({ "name" : user.source_order,
					"id": user.source_order,
					"data":[ [
						'Cash',
						user.paid_amount
					],
					[
						'Credit',
						user.outstanding_amount
					],
					[
						'Discount',
						user.discount_amount
					],
					]
				}
			)

	
	drilldown = {
		"breadcrumbs": {
			"position": {
				"align": 'right'
			}
		},
		"series":drildown_chart
	}


	series = [
		{
			"name": 'User Sales',
			"genderByPoint": "true",
			"data" : data_chart
		}
	],


	table =[
		{
			"columns":[
	# {"title":"Date", "field":"posting_date"},
	{"title":"Patient ID", "field":"customer_id"},
	{"title":"Patient Name", "field":"customer_name"},
	{"title":"Docotr", "field":"refrence_practitioner"},
	{"title":"Total", "field":"total"},
	 {"title":"Discount", "field":"discount"},
	{"title":"Paid", "field":"paid"},
	{"title":"Balance", "field":"balance"},
	  {"title":"User", "field":"user"},
	],
	"data" :get_sales_return_report(from_date , to_date)
		}
	]
   
   

	# frappe.errprint(get_sales_report())
	# frappe.errprint(drildown_chart)
	yAxis = "Total Sales"

	
	
	charts = [
	{
	"chart_type" : "column",
	"series" : series,
	"drilldown" :drilldown,
	"chart_title" : "User Sales ",
	"chart_subtitle" : "clickc to see By Cash and Credit",
	"yAxis" : yAxis 
	},
	{
		"chart_type" :"pie",
		"data" : data,
		"chart_title" : "Cash Vs Credit ",
		"chart_subtitle" : ""
	}
	]
	
	
	report_html_data = frappe.render_template(
	"rasiin_design/templates/Report/report.html",
	{

	  "withsidebar" : int(withsidebar),
	  "charts" :[],
	  "summaries": summaries,
	  "table": table,
	  "loading": int(loading)
	}
	)
	html = frappe.render_template(
		base_template_path,
		{"body": report_html_data ,"css" : get_print_style() , "title": "Statement For "},
	)
	# if view:
	return report_html_data
	# return get_pdf(report_html_data , {"orientation": "Landscape"})



@frappe.whitelist()
def get_report_reciept(from_date =  getdate() , to_date = getdate() ,withsidebar = 1 , loading = 1):
	# from_date = getdate(from_date)
	# to_date = getdate(to_date)
	parsed_date = datetime.strptime(from_date, '%d-%m-%Y')
	from_date = parsed_date.strftime('%Y-%m-%d')
	parsed_to_date = datetime.strptime(to_date, '%d-%m-%Y')
	to_date = parsed_to_date.strftime('%Y-%m-%d')

	report_gl = frappe.get_doc("Report", "Recipt Report")
	report_gl_filters = {
			"from_date": getdate(from_date),
			"to": getdate(to_date),
					 
		   
		}
	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator", filters=report_gl_filters, as_dict=True)
	summaries = [
		{
			"icon" :"fa fa-money",
			"title" :"Total Reciept",
			"data" : data[-1]['paid_amount'] if data else 0
		},
		]
	

	table =[
		{
			"columns":[
	# {"title":"Date", "field":"posting_date"},
	{"title":"Voucher", "field":"voucher"},
	{"title":"Patient Name", "field":"customer_name"},
	{
	  "title": "Paid Amount",
	  "field": "paid_amount",
	  "formatter": "money",
	  "formatterParams": {
		"decimal": ".",
		"thousand": ",",
		"symbol": "Sh ",
		"negativeSign": "true",
		"precision": 2,
	  },
	},
	],
	"data" :data
		}
	]
	
	report_html_data = frappe.render_template(
	"rasiin_design/templates/Report/report.html",
	{

	  "withsidebar" : int(withsidebar),
	  "charts" :[],
	  "summaries": summaries,
	  "table": table,
	  "loading": int(loading)
	}
	)
	html = frappe.render_template(
		base_template_path,
		{"body": report_html_data ,"css" : get_print_style() , "title": "Statement For "},
	)
	# if view:
	return report_html_data
	# return get_pdf(report_html_data , {"orientation": "Landscape"})


def get_commission_due_total(total=1):
	his_settings = frappe.get_doc("HIS Settings", "HIS Settings")
	report_gl = frappe.get_doc("Report", "Account Payable Summary")
	report_gl_filters = {
		
			"party_account": his_settings.doctor_commission_account,
			"range1":"30",
			"range2": "60",
			"range3": "90",
			"range4": "120",            
		   
		}
	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator", filters=report_gl_filters, as_dict=True)
	if data:
		if total:
			return data[-1]
	if data:
		return data[:-1]
@frappe.whitelist()   
def get_commission_due(from_date =  getdate() , to_date = getdate() ,withsidebar = 1 , loading = 1):

 
	totals = get_commission_due_total()
	frappe.errprint(totals)
	list_commission_due = get_commission_due_total(0)
	frappe.errprint(list_commission_due)
	data = []
	keys = {'paid_amount' : 'Cash' ,'outstanding_amount' : 'Credit' }
	if totals:
		for k in totals:
			if k in keys:
				data.append({
					"name": keys[k],
					"y":  totals[k]
				})
	

	
	summaries = []
	# discts = {}
	if totals:
		keys = {'invoiced' : 'Total Invoiced' ,'paid' : 'Total Paid','outstanding' : 'Total Balance' }
		for key, value in totals.items():
			if key in keys:
				summaries.append({
				"icon": "fa fa-money",
				"title": keys[key],
				"data": value
				})

	
	table =[
		{
			"columns":[
	{"title":"Party", "field":"party"},
	{"title":"Party Name", "field":"party_name"},
	{"title":"Mobile No", "field":"mobile_no"},
	{
	  "title": "Invoiced",
	  "field": "invoiced",
	  "formatter": "money",
	  "formatterParams": {
		"decimal": ".",
		"thousand": ",",
		"symbol": "Sh ",
		"negativeSign": "true",
		"precision": 2,
	  },
	},
	{
	  "title": "Paid",
	  "field": "paid",
	  "formatter": "money",
	  "formatterParams": {
		"decimal": ".",
		"thousand": ",",
		"symbol": "Sh ",
		"negativeSign": "true",
		"precision": 2,
	  },
	},
	{
	  "title": "Debit Note",
	  "field": "credit_note",
	  "formatter": "money",
	  "formatterParams": {
		"decimal": ".",
		"thousand": ",",
		"symbol": "Sh",
		"negativeSign": "true",
		"precision": 2,
	  },
	},
	{
	  "title": "Balance",
	  "field": "outstanding",
	  "formatter": "money",
	  "formatterParams": {
		"decimal": ".",
		"thousand": ",",
		"symbol": "Sh ",
		"negativeSign": "true",
		"precision": 2,
	  },
	},
	# {"title":"Invoiced", "field":"invoiced","formatter":"money",},
	# {"title":"Paid", "field":"paid"},
	# {"title":"Debit Note", "field":"credit_note"},
	# {"title":"Balance", "field":"outstanding"}
	],
	"data" :list_commission_due
		}
	]
   

	yAxis = "Total Sales"

	
 
	
	report_html_data = frappe.render_template(
	"rasiin_design/templates/Report/report.html",
	{

	  "withsidebar" : int(withsidebar),
	  "charts" :[],
	  "summaries": summaries,
	  "table": table,
	  "loading": int(loading)
	}
	)
	html = frappe.render_template(
		base_template_path,
		{"body": report_html_data ,"css" : get_print_style() , "title": "Statement For "},
	)
	# if view:
	return report_html_data
	# return get_pdf(report_html_data , {"orientation": "Landscape"})


def get_payable_summary_total(total=1):
	his_settings = frappe.get_doc("HIS Settings", "HIS Settings")
	report_gl = frappe.get_doc("Report", "Account Payable Summary")
	report_gl_filters = {
		
			# "party_account": his_settings.doctor_commission_account,
			"range1":"30",
			"range2": "60",
			"range3": "90",
			"range4": "120",            
		   
		}
	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator", filters=report_gl_filters, as_dict=True)
	if data:
		if total:
			return data[-1]
	if data:
		return data[:-1]
	
@frappe.whitelist()   
def get_payable_summary(from_date =  getdate() , to_date = getdate() ,withsidebar = 1 , loading = 1):

 
	totals = get_payable_summary_total()

	list_commission_due = get_payable_summary_total(0)

	data = []
	keys = {'paid_amount' : 'Cash' ,'outstanding_amount' : 'Credit' }
	if totals:
		for k in totals:
			if k in keys:
				data.append({
					"name": keys[k],
					"y":  totals[k]
				})
	

	
	summaries = []
	# discts = {}
	if totals:
		keys = {'invoiced' : 'Total Invoiced' ,'paid' : 'Total Paid','outstanding' : 'Balance' , 'credit_note' : "Return"}
		for key, value in totals.items():
			if key in keys:
				summaries.append({
				"icon": "fa fa-money",
				"title": keys[key],
				"data": value
				})

	
	table =[
		{
			"columns":[
	{"title":"Party", "field":"party"},
	{"title":"Party Name", "field":"party_name"},
	{"title":"Mobile No", "field":"mobile_no"},
	{
	  "title": "Invoiced",
	  "field": "invoiced",
	  "formatter": "money",
	  "formatterParams": {
		"decimal": ".",
		"thousand": ",",
		"symbol": "Sh ",
		"negativeSign": "true",
		"precision": 2,
	  },
	},
	{
	  "title": "Paid",
	  "field": "paid",
	  "formatter": "money",
	  "formatterParams": {
		"decimal": ".",
		"thousand": ",",
		"symbol": "Sh ",
		"negativeSign": "true",
		"precision": 2,
	  },
	},
	{
	  "title": "Debit Note",
	  "field": "credit_note",
	  "formatter": "money",
	  "formatterParams": {
		"decimal": ".",
		"thousand": ",",
		"symbol": "Sh ",
		"negativeSign": "true",
		"precision": 2,
	  },
	},
	{
	  "title": "Balance",
	  "field": "outstanding",
	  "formatter": "money",
	  "formatterParams": {
		"decimal": ".",
		"thousand": ",",
		"symbol": "Sh ",
		"negativeSign": "true",
		"precision": 2,
	  },
	},
	],
	"data" :list_commission_due
		}
	]
   

	yAxis = "Total Sales"

	
 
	
	report_html_data = frappe.render_template(
	"rasiin_design/templates/Report/report.html",
	{

	  "withsidebar" : int(withsidebar),
	  "charts" :[],
	  "summaries": summaries,
	  "table": table,
	  "loading": int(loading)
	}
	)
	html = frappe.render_template(
		base_template_path,
		{"body": report_html_data ,"css" : get_print_style() , "title": "Statement For "},
	)
	# if view:
	return report_html_data
	# return get_pdf(report_html_data , {"orientation": "Landscape"})




def get_total_sales_return(from_date , to_date):
	parsed_date = datetime.strptime(from_date, '%d-%m-%Y')
	from_date = parsed_date.strftime('%Y-%m-%d')
	parsed_to_date = datetime.strptime(to_date, '%d-%m-%Y')
	to_date = parsed_to_date.strftime('%Y-%m-%d')
	report_gl = frappe.get_doc("Report", "Refund")
	report_gl_filters = {
			"from_date": getdate(from_date),
			"to_date": getdate(to_date),
		   
		}
	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator", filters=report_gl_filters, as_dict=True)
	if data:
		return data[-1]

def get_total_sales_by_source_return(source , from_date , to_date):
	parsed_date = datetime.strptime(from_date, '%d-%m-%Y')
	from_date = parsed_date.strftime('%Y-%m-%d')
	parsed_to_date = datetime.strptime(to_date, '%d-%m-%Y')
	to_date = parsed_to_date.strftime('%Y-%m-%d')
	report_gl = frappe.get_doc("Report", "Refund")
	report_gl_filters = {
			"from_date": getdate(from_date),
			"to_date": getdate(to_date),
			"source" : source
		   
		}
	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator", filters=report_gl_filters, as_dict=True)
	if data:
		return data[-1]
	return None



def get_total_sales_by_source(source , from_date , to_date):
	parsed_date = datetime.strptime(from_date, '%d-%m-%Y')
	from_date = parsed_date.strftime('%Y-%m-%d')
	parsed_to_date = datetime.strptime(to_date, '%d-%m-%Y')
	to_date = parsed_to_date.strftime('%Y-%m-%d')
	report_gl = frappe.get_doc("Report", "Refund")
	totals = report_gl_filters = {
			"from_date": getdate(from_date),
			"to_date": getdate(to_date),
			"source" : source
		   
		}
	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator", filters=report_gl_filters, as_dict=True)
	if data:
		return data[-1]
	return None

def sales_return_per_user(from_date , to_date):
	report_gl = frappe.get_doc("Report", "Refund")
	report_gl_filters = {
			"from_date": getdate(from_date),
			"to_date": getdate(to_date),
		   
		}
	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator", filters=report_gl_filters, as_dict=True)
	if data:
		return data[:-1]


def sales_per_user(from_date , to_date):
	parsed_date = datetime.strptime(from_date, '%d-%m-%Y')
	from_date = parsed_date.strftime('%Y-%m-%d')
	report_gl = frappe.get_doc("Report", "Cash and Credit Sales")
	report_gl_filters = {
			"from_date": getdate(from_date),
			"to_date": getdate(to_date),
		   
		}
	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator", filters=report_gl_filters, as_dict=True)
	if data:
		return data[:-1]


def get_sales_return_report(from_date , to_date):
	parsed_date = datetime.strptime(from_date, '%d-%m-%Y')
	from_date = parsed_date.strftime('%Y-%m-%d')
	parsed_to_date = datetime.strptime(to_date, '%d-%m-%Y')
	to_date = parsed_to_date.strftime('%Y-%m-%d')
	report_gl = frappe.get_doc("Report", "Sales Return Report")
	report_gl_filters = {
			"from_date": getdate(from_date),
			"to_date": getdate(to_date),
		   
		}
	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator", filters=report_gl_filters, as_dict=True)
	frappe.errprint(data)
	if data:
		return data
	



@frappe.whitelist()
def get_report_descount(from_date =  getdate() , to_date = getdate() ,withsidebar = 1 , loading = 1):
	# from_date = getdate(from_date)
	# to_date = getdate(to_date)
	parsed_date = datetime.strptime(from_date, '%d-%m-%Y')
	from_date = parsed_date.strftime('%Y-%m-%d')
	parsed_to_date = datetime.strptime(to_date, '%d-%m-%Y')
	to_date = parsed_to_date.strftime('%Y-%m-%d')
	source_order = frappe.db.get_list("Source Order" , pluck = "name")
	data_chart = []
	serie=[]
	series = []
   
	for sr in source_order:
		report_gl = frappe.get_doc("Report", "Sales Reports")
		report_gl_filters = {
			"from_date": getdate(from_date),
			"to_date": getdate(to_date),
			"source": sr
		}
		columns_gl, data_discount_data = report_gl.get_data(
			limit=500, user="Administrator", filters=report_gl_filters, as_dict=True)

		# Extract discount amount from the last data entry
		if  data_discount_data:
			for key, value in data_discount_data[-1].items():
				if key == "discount_amount":
					data_chart.append({
						"name": sr,
						"y": value,
						"drilldown": sr
					})

		# Create series for drilldown
		drilldown_series_data = []
		for i, val in enumerate(data_discount_data[:-1]):
			series_data = [val['item_group'], val['discount_amount']]
			drilldown_series_data.append(series_data)

		# Append drilldown series to the main series
		serie.append({
			"name": sr,
			"id": sr,
			"data": drilldown_series_data
		})
	 
	

	series = [
		{
			"name": 'Source Income',
			"genderByPoint": "true",
			"data": data_chart
		}
	],
   
	
	
	report_gl = frappe.get_doc("Report", "Cash and Credit Sales")
	report_gl_filters_disc = {
			"from_date": getdate(from_date),
			"to_date": getdate(to_date),
			
		}
	columns_gl, data_gl = report_gl.get_data(
				limit=500, user="Administrator", filters=report_gl_filters_disc, as_dict=True
			) 
	

	discount_data = frappe.db.sql(f"""
			select 
			max(`tabSales Invoice`.discount_amount) as `Max Discount`,
			min(`tabSales Invoice`.discount_amount) as `Min Discount`
		from 
			`tabSales Invoice`   where `tabSales Invoice`.docstatus=1 and 
			`tabSales Invoice`.is_opening!='Yes'  and 
			`tabSales Invoice`.posting_date between '{from_date}'  and '{to_date}'
			and `tabSales Invoice`.discount_amount > 0 """ , as_dict =1 )
	discount_invoices = frappe.db.sql(f"""
			select 
				name,
				patient,
				patient_name,
				total,            
				discount_amount,
				net_total,
				additional_discount_percentage,
				owner
			
		from 
			`tabSales Invoice`   where docstatus=1 and 
			is_opening!='Yes'  and 
			posting_date between '{from_date}'  and '{to_date}'
			and discount_amount > 0 """ , as_dict =1 )
	summaries = [
		{
			"icon" :"fa fa-money",
			"title" :"Total Discount",
			"data" : data_gl[-1]['discount_amount'] if data_gl else 0
		},
		]

	data = []
	# discts = {}
	sales_per = sales_per_discount(from_date , to_date)
	if sales_per:
		for user in sales_per:
			data.append({
			"name":frappe.db.get_value("User" , user.owner , "full_name"),
			"y": user.discount_amount
			})
	if discount_data:
		for key, value in discount_data[-1].items():
			summaries.append({
			"icon": "fa fa-money",
			"title": key,
			"data": value
			})
		
		
		# summaries.append(discts)


	table =[
		{
			"columns":[
	{"title":"Voucher", "field":"name"},
	{"title":"Patient", "field":"patient" },
	{"title":"Patient Name", "field":"patient_name"},
	{"title":"Total", "field":"total" },
	{"title":"Discount Amount", "field":"discount_amount"},
	{"title":"Net Total", "field":"net_total" },
	{"title":"Discount Percentage", "field":"additional_discount_percentage" },
	{"title":"User", "field":"owner"},
	],
	"data" :discount_invoices
		}
	]
	yAxis = "Total market Sheet"
	drilldown = {
		"breadcrumbs": {
			"position": {
				"align": 'right'
			}
		},
		"series": serie
	}
	
	
	charts = [
	{
	"chart_type" : "column",
	"series" : series,
	"drilldown" : drilldown,
	"chart_title" : "Column  Chart ",
	"chart_subtitle" : "clickc to know more",
	"yAxis" : yAxis 
	},
	{
		"chart_type" :"pie",
		"data" : data,
		"chart_title" : "Pie Chart ",
		"chart_subtitle" : "clickc to know more"
	}
	]
	report_html_data = frappe.render_template(
	"rasiin_design/templates/Report/report.html",
	{

	  "withsidebar" : int(withsidebar),
	  "charts" : charts,
	  "summaries": summaries,
	  "table": table,
	  "loading": int(loading)
	}
	)
	html = frappe.render_template(
		base_template_path,
		{"body": report_html_data ,"css" : get_print_style() , "title": "Statement For "},
	)
	# if view:
	return report_html_data
	# return get_pdf(report_html_data , {"orientation": "Landscape"})






@frappe.whitelist()
def get_report_sales(from_date =  getdate() , to_date = getdate() ,withsidebar = 1 , loading = 1):
	# from_date = getdate(from_date)
	# to_date = getdate(to_date)
	source_order = frappe.db.get_list("Source Order" , pluck = "name")
	# source_order = ["OPD" , "IPD" , "Dental" , "WP"]
   
	data_chart = []
 
	totals = get_total_sales(from_date ,to_date)
	sales = []
	for src in source_order:
		source_sales = get_total_sales_by_source(src , from_date , to_date)
		if source_sales:
			sales.append({src:source_sales})

	
	

	data = []
	keys = {'paid_amount' : 'Cash' ,'outstanding_amount' : 'Credit' }
	if totals:
		for k in totals:
			if k in keys:
				data.append({
					"name": keys[k],
					"y":  totals[k]
				})
	

	
	summaries = []
	# discts = {}

	maping_keys = {'net_total' :'Total Sales' ,  'paid_amount' : 'Total Cash' ,'outstanding_amount' : 'Total Credit' }
	if totals:
		for key, value in totals.items():
			if key in maping_keys:
				summaries.append({
				"icon": "fa fa-money",
				"title": maping_keys[key],
				"data": value,
				"new_break" : 1
				})
				for sale in sales:
					
					for k , v in sale.items():
						# if key in v:
					
						summaries.append({
							"icon": "fa fa-money",
							"title": k + ' ' + maping_keys[key].split()[1],
							"data": v[key]
							})
		  
	  
		
		# summaries.append(discts)
	sales_per = sales_per_user(from_date , to_date)
	data_chart =[]
	drildown_chart = []
	if sales_per:
		for user in sales_per:
			data_chart.append({
					"name": user.source_order,
					# "name" : user.owner,
					"y": user.net_total ,
					"drilldown": user.source_order
				})
			
			drildown_chart.append({ "name" : user.source_order,
					"id": user.source_order,
					"data":[ [
						'Cash',
						user.paid_amount
					],
					[
						'Credit',
						user.outstanding_amount
					],
					[
						'Discount',
						user.discount_amount
					],
					]
				}
			)

	
	drilldown = {
		"breadcrumbs": {
			"position": {
				"align": 'right'
			}
		},
		"series":drildown_chart
	}


	series = [
		{
			"name": 'Sales By Source',
			"genderByPoint": "true",
			"data" : data_chart
		}
	],


	table =[
		{
			"columns":[
	# {"title":"Date", "field":"posting_date"},
	{"title":"Patient ID", "field":"customer_id"},
	{"title":"Patient Name", "field":"customer_name"},
	{"title":"Docotr", "field":"refrence_practitioner"},
	{"title":"Total", "field":"total"},
	 {"title":"Discount", "field":"discount"},
	{"title":"Paid", "field":"paid"},
	{"title":"Balance", "field":"balance"},
	  {"title":"User", "field":"user"},
	],
	"data" : get_sales_report(from_date , to_date)
		}
	]
   
   

	yAxis = "Total Sales"

	
	
	charts = [
	{
	"chart_type" : "column",
	"series" : series,
	"drilldown" :drilldown,
	"chart_title" : "Sales By Department",
	"chart_subtitle" : "clickc to see By Cash and Credit",
	"yAxis" : yAxis 
	},
	{
		"chart_type" :"pie",
		"data" : data,
		"chart_title" : "Cash Vs Credit ",
		"chart_subtitle" : ""
	}
	]
	
	
	report_html_data = frappe.render_template(
	"rasiin_design/templates/Report/report.html",
	{

	  "withsidebar" : int(withsidebar),
	  "charts" :charts,
	  "summaries": summaries,
	  "table": table,
	  "loading": int(loading)
	}
	)
	html = frappe.render_template(
		base_template_path,
		{"body": report_html_data ,"css" : get_print_style() , "title": "Statement For "},
	)
	# if view:
	return report_html_data
	# return get_pdf(report_html_data , {"orientation": "Landscape"})



@frappe.whitelist()
def get_opd_sales_report(from_date =  getdate() , to_date = getdate() ,withsidebar = 1 , loading = 1):
	# from_date = getdate(from_date)
	# to_date = getdate(to_date)
	source_order = ["OPD"]
   
	data_chart = []
 
	totals = get_total_sales(from_date , to_date)
	sales = []
	if source_order:
		for src in source_order:
			source_sales = get_total_sales_by_source(src , from_date , to_date)
			if source_sales:
				sales.append({src:source_sales})

	
	

	data = []
	keys = {'outstanding_amount' : 'Credit' }
	if totals:
		for k in totals:
			if k in keys:
				data.append({
					"name": keys[k],
					"y":  totals[k]
				})
	

	
	summaries = []
	# discts = {}

	maping_keys = {'outstanding_amount' : 'Total Credit' }
	if totals:
		for key, value in totals.items():
			if key in maping_keys:
				summaries.append({
				"icon": "fa fa-money",
				"title": maping_keys[key],
				"data": value
				})
				if sales:
					for sale in sales:
						
						for k , v in sale.items():
							# if key in v:
						
							summaries.append({
								"icon": "fa fa-money",
								"title": k + ' ' + maping_keys[key].split()[1],
								"data": v[key]
								})
			
	  
		
		# summaries.append(discts)
	sales_per = sales_per_user(from_date , to_date)
	data_chart =[]
	drildown_chart = []
	if sales_per:
		for user in sales_per:
			if user.source_order == "OPD":
				data_chart.append({
						"name": user.source_order,
						# "name" : user.owner,
						"y": user.net_total ,
						"drilldown": user.source_order
					})
				
				drildown_chart.append({ "name" : user.source_order,
						"id": user.source_order,
						"data":[ 
						[
							'Credit',
							user.outstanding_amount
						],
						[
							'Discount',
							user.discount_amount
						],
						]
					}
				)

	
	drilldown = {
		"breadcrumbs": {
			"position": {
				"align": 'right'
			}
		},
		"series":drildown_chart
	}


	series = [
		{
			"name": 'User Sales',
			"genderByPoint": "true",
			"data" : data_chart
		}
	],


	table =[
		{
			"columns":[
	# {"title":"Date", "field":"posting_date"},
	{"title":"Patient ID", "field":"customer_id"},
	{"title":"Patient Name", "field":"customer_name"},
	{"title":"Docotr", "field":"refrence_practitioner"},
	{"title":"Total", "field":"total", },
	 {"title":"Discount", "field":"discount"},
	{"title":"Paid", "field":"paid"},
	{"title":"Balance", "field":"balance", },
	  {"title":"User", "field":"user"},
	],
	"data" : get_sales_report(from_date , to_date)
		}
	]
   
   

	yAxis = "Total Sales"

	
	
	charts = [
	{
	"chart_type" : "column",
	"series" : series,
	"drilldown" :drilldown,
	"chart_title" : "User Sales ",
	"chart_subtitle" : "clickc to see By Cash and Credit",
	"yAxis" : yAxis 
	},
	{
		"chart_type" :"pie",
		"data" : data,
		"chart_title" : "Cash Vs Credit ",
		"chart_subtitle" : ""
	}
	]
	
	
	report_html_data = frappe.render_template(
	"rasiin_design/templates/Report/report.html",
	{

	  "withsidebar" : int(withsidebar),
	  "charts" :charts,
	  "summaries": summaries,
	  "table": table,
	  "loading": int(loading)
	}
	)
	html = frappe.render_template(
		base_template_path,
		{"body": report_html_data ,"css" : get_print_style() , "title": "Statement For "},
	)
	# if view:
	return report_html_data
	# return get_pdf(report_html_data , {"orientation": "Landscape"})





def get_total_sales(from_date , to_date):
	
	parsed_date = datetime.strptime(from_date, '%d-%m-%Y')
	from_date = parsed_date.strftime('%Y-%m-%d')
	parsed_to_date = datetime.strptime(to_date, '%d-%m-%Y')
	to_date = parsed_to_date.strftime('%Y-%m-%d')
	# frappe.errprint( getdate(str(from_date)))
	
	report_gl = frappe.get_doc("Report", "Cash and Credit Sales")
	report_gl_filters = {
			"from_date": getdate(from_date),
			"to_date": getdate(to_date),
		   
		}
	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator", filters=report_gl_filters, as_dict=True)
	if data:
	
		return data[-1]




def get_total_sales_by_source(source , from_date , to_date):
	parsed_date = datetime.strptime(from_date, '%d-%m-%Y')
	from_date = parsed_date.strftime('%Y-%m-%d')
	parsed_to_date = datetime.strptime(to_date, '%d-%m-%Y')
	to_date = parsed_to_date.strftime('%Y-%m-%d')
	report_gl = frappe.get_doc("Report", "Cash and Credit Sales")
	report_gl_filters = {
			"from_date": getdate(from_date),
			"to_date": getdate(to_date),
			"source" : source
		   
		}
	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator", filters=report_gl_filters, as_dict=True)
	if data:
		return data[-1]
	return None




def sales_per_user(from_date , to_date):
	report_gl = frappe.get_doc("Report", "Cash and Credit Sales")
	report_gl_filters = {
			"from_date": getdate(from_date , to_date),
			"to_date": getdate(),
		   
		}
	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator", filters=report_gl_filters, as_dict=True)
	if data:
		return data[:-1]


def sales_per_discount(from_date , to_date):
	report_gl = frappe.get_doc("Report", "Discount")
	report_gl_filters = {
			"from_date": getdate(from_date),
			"to_date": getdate(to_date),
		   
		}
	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator", filters=report_gl_filters, as_dict=True)
	if data:
		return data[:-1]




def get_sales_report(from_date , to_date):
	parsed_date = datetime.strptime(from_date, '%d-%m-%Y')
	from_date = parsed_date.strftime('%Y-%m-%d')
	parsed_to_date = datetime.strptime(to_date, '%d-%m-%Y')
	to_date = parsed_to_date.strftime('%Y-%m-%d')
	report_gl = frappe.get_doc("Report", "New Sales Report")
	report_gl_filters = {
			"from_date": getdate(from_date),
			"to_date": getdate(to_date),
		   
		}
	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator", filters=report_gl_filters, as_dict=True)
	if data:
		return data
	


@frappe.whitelist()
def get_report_purchase_anaylsis(from_date =  getdate() , to_date = getdate() ,withsidebar = 1 , loading = 1):
	# from_date = getdate(from_date)
	# to_date = getdate(to_date)
	parsed_date = datetime.strptime(from_date, '%d-%m-%Y')
	from_date = parsed_date.strftime('%Y-%m-%d')
	parsed_to_date = datetime.strptime(to_date, '%d-%m-%Y')
	to_date = parsed_to_date.strftime('%Y-%m-%d')
	report_gl = frappe.get_doc("Report", "Purchase Order Analysis")
	report_gl_filters = {
			"from_date": getdate(from_date),
			"to_date": getdate(to_date),
			"company" : company
		   
		}
	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator", filters=report_gl_filters, as_dict=True)
	summaries = []
	columns = [
	   
   		]
	
	for d in data:
		for k in d:
			if k in ['item_code' , 'item_name']:

				d[k] = re.sub(pattern, '', d[k])
			if k in ['date' , 'required_date']:
				d[k] = str(d[k] )

		# new_data.append(d)
	# data = List[data]
	new_data = data[:6]
	table = [
		{
				"columns":[
		{"title":"Voucher No", "field":"purchase_order"},
		{"title":"Supplier", "field":"supplier"},
		{"title":"Item", "field":"item_code"},
		{"title":"Ordered QTY", "field":"qty", "hozAlign":"center"},
		{"title":"Recieved QTY", "field":"received_qty"},
		{"title":"Billed QTY", "field":"billed_qty"},
		# {"title":"Driver", "field":"car", "hozAlign":"center"},
		],
		"data" :data
			}
	]


   
	if data:
	# for d in data[-1]:
		sume = data[-1]
		total_order = sume['qty']
		total_recived = sume['received_qty']
		total_billed = sume['billed_qty']
		summaries = [
			{
			"icon": "fa fa-money",
			"title": f'<strong>Total Order <br> QTY {total_order}</strong>',
			"data":  sume['amount']
			},
			
			  {
			"icon": "fa fa-money",
			"title": f'<strong>Total Received <br> QTY {total_recived}</strong>',
			"data":  sume['received_qty_amount']
			},

			{
			"icon": "fa fa-money",
			"title": f'<strong>Total Billed <br> QTY {total_billed}</strong>',
			"data":  sume['billed_amount']
			}
			
			
			]
		
	report_html_data = frappe.render_template(
		"rasiin_design/templates/Report/report.html",
		{

		"withsidebar" : int(withsidebar),
		"charts" :[],
		"summaries": summaries,
		"table": table,
		"loading": int(loading)
		}
		)
	html = frappe.render_template(
		base_template_path,
		{"body": report_html_data ,"css" : get_print_style() , "title": "Statement For "},
	)
	return report_html_data