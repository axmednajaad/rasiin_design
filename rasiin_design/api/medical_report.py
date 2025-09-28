from ast import List
import dis
from hmac import new
# from msilib.text import tables
from xmlrpc.client import Boolean
import frappe
from collections import defaultdict
import frappe
from frappe.utils import getdate
from frappe.desk.query_report import run
import re

from frappe.utils.pdf import get_pdf
from frappe.www.printview import get_print_style
from frappe.utils import getdate
company = frappe.defaults.get_user_default("company")
abbr    = frappe.db.get_value("Company" , company , "abbr")
curren =  frappe.db.get_value("Company" , company , "default_currency")
base_template_path = "frappe/www/printview.html"
pattern = r'[^A-Za-z0-9 ]'
@frappe.whitelist()
def get_report_design(withsidebar = 1,loading=1):
	
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
	"rasiin_design/templates/Report/medical_report.html",
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
def get_patient_visit(from_date =  getdate() , to_date = getdate() ,withsidebar = 1 , loading = 1):

	from_date = getdate(from_date)
	to_date = getdate(to_date)
	que_data = frappe.db.sql(f""" 

		 
		SELECT
        COUNT(CASE WHEN gender = 'Male' THEN 1 END) AS male,
		COUNT(CASE WHEN gender = 'Female' THEN 1 END) AS female,
		COUNT(CASE WHEN que_type = 'New Patient' THEN 1 END) AS new_p,
		COUNT(CASE WHEN que_type = 'Follow Up' THEN 1 END) AS follow_up
		from `tabQue`
		where date between '{from_date}' and '{to_date}'
		
					  


	""", as_dict = 1)

	doctor_chart = frappe.db.sql(f""" 

		 
		SELECT
		practitioner as doctor,
        COUNT(patient) as patients
		from `tabQue`
		where date between '{from_date}' and '{to_date}'
		group by practitioner
		
					  


							  
	""", as_dict = 1)
	summaries = [
				{
				"icon": "fa fa-money",
				"title": "New Patient",
				"data": que_data[0].new_p
				},
				{
				"icon": "fa fa-money",
				"title": "Follow Up",
				"data": que_data[0].follow_up
				}
				
				]
	
	
	data_chart = []
	for doctor in doctor_chart:
		data_chart.append({
				"name": doctor.doctor,
				# "name" : user.owner,
				"y": doctor.patients ,
				# "drilldown": doctor.name
			})
	frappe.errprint(data_chart)

	series = [
		{
			"name": 'Browsers',
			"genderByPoint": "true",
			"data" : data_chart
			# "data": [{'name': 'Dr Abdijabar', 'y': 39}, {'name': 'Dr Abdirashid Abdirahman', 'y': 10}, {'name': 'Dr Abdulkadir Sheikh', 'y': 10}, {'name': 'Dr Allan Mukuzi', 'y': 48}, {'name': 'Dr Dubow Hussein', 'y': 4}, {'name': 'Dr Faiga', 'y': 44}, {'name': 'Dr Farhiya Mohammed', 'y': 147}, {'name': 'Dr M.S. SAROYA', 'y': 15}, {'name': 'Dr Mahad Abdirahman Mohamed', 'y': 65}, {'name': 'DR Timothy Gacani', 'y': 7}, {'name': 'Dr. Abdirahman Salad', 'y': 257}, {'name': 'Dr. Abdisamad Dimbil', 'y': 228}, {'name': 'Dr. Atef Ibrahim', 'y': 19}, {'name': 'Dr. Fahmo', 'y': 130}, {'name': 'Dr. Faiza', 'y': 18}, {'name': 'DR. ISSACK SHEIKH', 'y': 2}, {'name': 'Dr. Karren', 'y': 85}, {'name': 'Dr. Muhanad Hamed', 'y': 1}, {'name': 'Dr. Nasri Mohamed', 'y': 1}, {'name': 'Dr. Raid Alhasan', 'y': 220}, {'name': 'Dr. Yassir Bakheet', 'y': 348}, {'name': 'Drs Atika Dhuhulow', 'y': 8}, {'name': 'Drs Ayan Mohamed Hashi', 'y': 13}, {'name': 'Drs Saadia Hussein', 'y': 40}, {'name': 'Drs Salma Bashir', 'y': 11}, {'name': 'Drs. Hana Abdirahman', 'y': 5}, {'name': 'Emergency', 'y': 19}, {'name': 'Walking Patient', 'y': 6}]
			
		}
	],
   
	
	yAxis = "Total Patient Visited"
	# frappe.errprint(series)
	data =[{
				"name": "Male",
				"y":  que_data[0].male
			},
			{
				"name": "Female",
				"y":  que_data[0].female
			}
			]
	charts = [
	{
	"chart_type" : "column",
	"series" : series,
	"drilldown" :{},
	"chart_title" : "Doctor Wise Patient Visited",
	"chart_subtitle" : "",
	"yAxis" : yAxis 
	},
	{
		"chart_type" :"pie",
		"data" : data,
		"chart_title" : "Male Vs Female ",
		"chart_subtitle" : ""
	}
	]

	table_data = frappe.db.sql(f""" 

		select patient , patient_name ,practitioner , department , que_type , date from `tabQue`
		where date between '{from_date}' and '{to_date}'
	""", as_dict = 1)
	for d in table_data:
		for k in d:
			
			if k  in ['date' , 'creation' , 'modified' ,'time']:
				
				d[k] =str(d[k])
		
	# frappe.errprint(table_data)
	table = [
		{
			"columns":[
	# {"title":"Date", "field":"posting_date"},
	{"title":"Patient ID", "field":"patient"},
	{"title":"Patient Name", "field":"patient_name"},
	{"title":"Docotr", "field":"practitioner"},
	{"title":"Deparment", "field":"department", },
	 {"title":"Visit Type", "field":"que_type"},
	{"title":"Visit Date", "field":"date"}
	],
	"data" : table_data
	}]
	report_html_data = frappe.render_template(
	"rasiin_design/templates/Report/medical_report.html",
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





@frappe.whitelist()
def get_report_doctor_wise_visit(from_date =  getdate() , to_date = getdate() ,withsidebar = 1 , loading = 1):
	from_date = getdate(from_date)
	to_date = getdate(to_date)
	que_data = frappe.db.sql(f""" 

		 
		SELECT
        COUNT(CASE WHEN status = 'Open' THEN 1 END) AS open,
		COUNT(CASE WHEN status = 'Closed' THEN 1 END) AS closed,
		COUNT(CASE WHEN que_type = 'New Patient' THEN 1 END) AS new_p,
		COUNT(CASE WHEN que_type = 'Follow Up' THEN 1 END) AS follow_up
		from `tabQue`
		where date between '{from_date}' and '{to_date}'
					  


	""", as_dict = 1)
	doctor_chart = frappe.db.sql(f""" 

		 
		SELECT
		practitioner as doctor,
        COUNT(patient) as patients
		from `tabQue`
	
		where date between '{from_date}' and '{to_date}'
		group by practitioner
					  


							  
	""", as_dict = 1)
	summaries = [
				{
				"icon": "fa fa-money",
				"title": "New Patient",
				"data": que_data[0].new_p
				},
				{
				"icon": "fa fa-money",
				"title": "Follow Up",
				"data": que_data[0].follow_up
				},
				{
				"icon": "fa fa-money",
				"title": "Closed",
				"data": que_data[0].closed
				},
					{
				"icon": "fa fa-money",
				"title": "Open",
				"data": que_data[0].open
				},

				
				]
	
	
	data_chart = []
	for doctor in doctor_chart:
		data_chart.append({
				"name": doctor.doctor,
				# "name" : user.owner,
				"y": doctor.patients ,
				# "drilldown": doctor.name
			})
	# frappe.errprint(data_chart)

	series = [
		{
			"name": 'Browsers',
			"genderByPoint": "true",
			"data" : data_chart
			# "data": [{'name': 'Dr Abdijabar', 'y': 39}, {'name': 'Dr Abdirashid Abdirahman', 'y': 10}, {'name': 'Dr Abdulkadir Sheikh', 'y': 10}, {'name': 'Dr Allan Mukuzi', 'y': 48}, {'name': 'Dr Dubow Hussein', 'y': 4}, {'name': 'Dr Faiga', 'y': 44}, {'name': 'Dr Farhiya Mohammed', 'y': 147}, {'name': 'Dr M.S. SAROYA', 'y': 15}, {'name': 'Dr Mahad Abdirahman Mohamed', 'y': 65}, {'name': 'DR Timothy Gacani', 'y': 7}, {'name': 'Dr. Abdirahman Salad', 'y': 257}, {'name': 'Dr. Abdisamad Dimbil', 'y': 228}, {'name': 'Dr. Atef Ibrahim', 'y': 19}, {'name': 'Dr. Fahmo', 'y': 130}, {'name': 'Dr. Faiza', 'y': 18}, {'name': 'DR. ISSACK SHEIKH', 'y': 2}, {'name': 'Dr. Karren', 'y': 85}, {'name': 'Dr. Muhanad Hamed', 'y': 1}, {'name': 'Dr. Nasri Mohamed', 'y': 1}, {'name': 'Dr. Raid Alhasan', 'y': 220}, {'name': 'Dr. Yassir Bakheet', 'y': 348}, {'name': 'Drs Atika Dhuhulow', 'y': 8}, {'name': 'Drs Ayan Mohamed Hashi', 'y': 13}, {'name': 'Drs Saadia Hussein', 'y': 40}, {'name': 'Drs Salma Bashir', 'y': 11}, {'name': 'Drs. Hana Abdirahman', 'y': 5}, {'name': 'Emergency', 'y': 19}, {'name': 'Walking Patient', 'y': 6}]
			
		}
	],
   
	
	yAxis = "Total Patient Visited"
	# frappe.errprint(series)
	data =[{
				"name": "Open",
				"y":  que_data[0].open
			},
			{
				"name": "Closed",
				"y":  que_data[0].closed
			}
			]
	charts = [
	{
	"chart_type" : "column",
	"series" : series,
	"drilldown" :{},
	"chart_title" : "Doctor Wise Patient Visited",
	"chart_subtitle" : "",
	"yAxis" : yAxis 
	},
	{
		"chart_type" :"pie",
		"data" : data,
		"chart_title" : "Open vs Closed",
		"chart_subtitle" : ""
	}
	]

	table_data = get_que_report(from_date , to_date)
	# for d in table_data:
	# 	for k in d:
	# 		if d[k] == None:
	# 			d[k] = ""
			
	# 		if k  in ['date' , 'creation' , 'modified' ,'time']:
				
	# 			d[k] =str(d[k])
		
	# frappe.errprint(table_data)
	
	table = [
		{
			"columns":[
	# {"title":"Date", "field":"posting_date"},
	{"title":"Doctor", "field":"practitioner"},
	{"title":"Department", "field":"department"},
	{"title":"New", "field":"new"},
	{"title":"Followup", "field":"followup", },
	{"title":"Refer", "field":"refer"},
	{"title":"Revisit", "field":"revisit"},
	{"title":"Total", "field":"total"},
	{"title":"Open", "field":"open"},
	{"title":"Closed", "field":"closed"},


	
	],
	"data" : table_data
	}]
	report_html_data = frappe.render_template(
	"rasiin_design/templates/Report/medical_report.html",
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





@frappe.whitelist()
def get_report_diagnose(from_date =  getdate() , to_date = getdate() ,withsidebar = 1 , loading = 1):
	from_date = getdate(from_date)
	to_date = getdate(to_date)
	report_gl = frappe.get_doc("Report", "Diasgnose")

	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator",  as_dict=True)
	data_chart = []
	for dia in data[:11]:
		data_chart.append({
				"name": dia.diagnosis,
				# "name" : user.owner,
				"y": dia.number ,
				# "drilldown": doctor.name
			})
	# frappe.errprint(data_chart)

	series = [
		{
			"name": 'Browsers',
			"genderByPoint": "true",
			"data" : data_chart
			# "data": [{'name': 'Dr Abdijabar', 'y': 39}, {'name': 'Dr Abdirashid Abdirahman', 'y': 10}, {'name': 'Dr Abdulkadir Sheikh', 'y': 10}, {'name': 'Dr Allan Mukuzi', 'y': 48}, {'name': 'Dr Dubow Hussein', 'y': 4}, {'name': 'Dr Faiga', 'y': 44}, {'name': 'Dr Farhiya Mohammed', 'y': 147}, {'name': 'Dr M.S. SAROYA', 'y': 15}, {'name': 'Dr Mahad Abdirahman Mohamed', 'y': 65}, {'name': 'DR Timothy Gacani', 'y': 7}, {'name': 'Dr. Abdirahman Salad', 'y': 257}, {'name': 'Dr. Abdisamad Dimbil', 'y': 228}, {'name': 'Dr. Atef Ibrahim', 'y': 19}, {'name': 'Dr. Fahmo', 'y': 130}, {'name': 'Dr. Faiza', 'y': 18}, {'name': 'DR. ISSACK SHEIKH', 'y': 2}, {'name': 'Dr. Karren', 'y': 85}, {'name': 'Dr. Muhanad Hamed', 'y': 1}, {'name': 'Dr. Nasri Mohamed', 'y': 1}, {'name': 'Dr. Raid Alhasan', 'y': 220}, {'name': 'Dr. Yassir Bakheet', 'y': 348}, {'name': 'Drs Atika Dhuhulow', 'y': 8}, {'name': 'Drs Ayan Mohamed Hashi', 'y': 13}, {'name': 'Drs Saadia Hussein', 'y': 40}, {'name': 'Drs Salma Bashir', 'y': 11}, {'name': 'Drs. Hana Abdirahman', 'y': 5}, {'name': 'Emergency', 'y': 19}, {'name': 'Walking Patient', 'y': 6}]
			
		}
	],
	yAxis = ""
	charts = [
	{
	"chart_type" : "column",
	"series" : series,
	"drilldown" :{},
	"chart_title" : "Top 10 Most Diagnoses",
	"chart_subtitle" : "",
	"yAxis" : yAxis 
	},
	# {
	# 	"chart_type" :"pie",
	# 	"data" : data,
	# 	"chart_title" : "Open vs Closed",
	# 	"chart_subtitle" : ""
	# }
	]
	table = [
		{
			"columns":[
	# {"title":"Date", "field":"posting_date"},
	{"title":"Diagnosis", "field":"diagnosis"},
	{"title":"Number", "field":"number"},


	
	],
	"data" : data
	}]
	report_html_data = frappe.render_template(
	"rasiin_design/templates/Report/medical_report.html",
	{

	  "withsidebar" : int(withsidebar),
	  "charts" :charts,
	  "summaries": [],
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



@frappe.whitelist()
def get_report_diagnose(from_date =  getdate() , to_date = getdate() ,withsidebar = 1 , loading = 1):
	from_date = getdate(from_date)
	to_date = getdate(to_date)
	report_gl = frappe.get_doc("Report", "Diasgnose")

	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator",  as_dict=True)
	data_chart = []
	for dia in data[:11]:
		data_chart.append({
				"name": dia.diagnosis,
				# "name" : user.owner,
				"y": dia.number ,
				# "drilldown": doctor.name
			})
	# frappe.errprint(data_chart)

	series = [
		{
			"name": 'Diagnose',
			"genderByPoint": "true",
			"data" : data_chart
					
		}
	],
	yAxis = ""
	charts = [
	{
	"chart_type" : "column",
	"series" : series,
	"drilldown" :{},
	"chart_title" : "Top 10 Most Diagnoses",
	"chart_subtitle" : "",
	"yAxis" : yAxis 
	},
	# {
	# 	"chart_type" :"pie",
	# 	"data" : data,
	# 	"chart_title" : "Open vs Closed",
	# 	"chart_subtitle" : ""
	# }
	]
	table = [
		{
			"columns":[
	# {"title":"Date", "field":"posting_date"},
	{"title":"Diagnosis", "field":"diagnosis"},
	{"title":"Number", "field":"number"},


	
	],
	"data" : data
	}]
	report_html_data = frappe.render_template(
	"rasiin_design/templates/Report/medical_report.html",
	{

	  "withsidebar" : int(withsidebar),
	  "charts" :charts,
	  "summaries": [],
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






@frappe.whitelist()
def get_report_lab(from_date =  getdate() , to_date = getdate() ,withsidebar = 1 , loading = 1):
	
	from_date = getdate(from_date)
	to_date = getdate(to_date)
	# ordered_collected = frappe.db.sql(f"""


	# 	select 
	# 	 COUNT(CASE WHEN docstatus = 0 THEN 1 END) AS ordered,
	# 	 COUNT(CASE WHEN docstatus = 1 THEN 1 END) AS collected,					   


	# """, as_dict =1)

	report_gl = frappe.get_doc("Report", "Lab Report")
	report_gl_filters = {
			"Start_date": getdate(from_date),
			"End_date": getdate(to_date),
		   
		}

	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator",  filters=report_gl_filters, as_dict=True)
	
	data_chart = []
	for test in data[:11]:
		data_chart.append({
				"name": test.test_name,
				# "name" : user.owner,
				"y": test.number ,
				# "drilldown": doctor.name
			})
	# frappe.errprint(data_chart)

	series = [
		{
			"name": 'Test',
			"genderByPoint": "true",
			"data" : data_chart
					
		}
	],
	yAxis = ""
	charts = [
	{
	"chart_type" : "column",
	"series" : series,
	"drilldown" :{},
	"chart_title" : "Top 10 Most Lab Tests",
	"chart_subtitle" : "",
	"yAxis" : yAxis 
	},
	# {
	# 	"chart_type" :"pie",
	# 	"data" : data,
	# 	"chart_title" : "Open vs Closed",
	# 	"chart_subtitle" : ""
	# }
	]
	table = [
		{
			"columns":[
	# {"title":"Date", "field":"posting_date"},
	{"title":"Test Name", "field":"test_name"},
	{"title":"Number", "field":"number"},


	
	],
	"data" : data
	}]
	report_html_data = frappe.render_template(
	"rasiin_design/templates/Report/medical_report.html",
	{

	  "withsidebar" : int(withsidebar),
	  "charts" :charts,
	  "summaries": [],
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




@frappe.whitelist()
def get_report_radiolgy(from_date =  getdate() , to_date = getdate() ,withsidebar = 1 , loading = 1):
	from_date = getdate(from_date)
	to_date = getdate(to_date)
	rad_info = frappe.db.sql(f"""


		select 
		 COUNT(CASE WHEN docstatus = 0 THEN 1 END) AS draf,
		 COUNT(CASE WHEN docstatus = 1 THEN 1 END) AS completed
		 from `tabRadiology`
		where date between '{from_date}' and '{to_date}'					   


	""", as_dict =1)


	summaries = [
				{
				"icon": "fa fa-money",
				"title": "Draft",
				"data": rad_info[0].draf
				},
				{
				"icon": "fa fa-money",
				"title": "Completed",
				"data": rad_info[0].completed
				},
			

				
				]
	data = frappe.db.sql(f""" 


			select eximination as eximination ,  count(name) as number from `tabRadiology` 
					  
			where date between '{from_date}' and '{to_date}'		  
			group by eximination ORDER BY count(name) DESC;
			
		""", as_dict =1)
	
	# # data_chart = []
	# # for test in data[:11]:
	# # 	data_chart.append({
	# # 			"name": test.test_name,
	# # 			# "name" : user.owner,
	# # 			"y": test.number ,
	# # 			# "drilldown": doctor.name
	# # 		})
	# # frappe.errprint(data_chart)

	# series = [
	# 	{
	# 		"name": 'Test',
	# 		"genderByPoint": "true",
	# 		"data" : data_chart
					
	# 	}
	# ],
	# yAxis = ""
	# charts = [
	# {
	# "chart_type" : "column",
	# "series" : series,
	# "drilldown" :{},
	# "chart_title" : "Top 10 Most Lab Tests",
	# "chart_subtitle" : "",
	# "yAxis" : yAxis 
	# },
	# {
	# 	"chart_type" :"pie",
	# 	"data" : data,
	# 	"chart_title" : "Open vs Closed",
	# 	"chart_subtitle" : ""
	# }
	# ]
	table = [
		{
			"columns":[
	# {"title":"Date", "field":"posting_date"},
	{"title":"Imaging", "field":"eximination"},
	{"title":"Number", "field":"number"},


	
	],
	"data" : data
	}]
	report_html_data = frappe.render_template(
	"rasiin_design/templates/Report/medical_report.html",
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


@frappe.whitelist()
def get_report_inpatient(from_date =  getdate() , to_date = getdate() ,withsidebar = 1 , loading = 1):
	from_date = getdate(from_date)
	to_date = getdate(to_date)
	inp_reco = frappe.db.sql(f"""


		select 
						  
		 COUNT(CASE WHEN status = "Admission Scheduled" THEN 1 END) AS sch,
		 COUNT(CASE WHEN status = "Admitted" THEN 1 END) AS admitted,
		 COUNT(CASE WHEN status = "Discharge Scheduled" THEN 1 END) AS dis_sch,
		 COUNT(CASE WHEN status = "Discharged" THEN 1 END) AS discharged,
		COUNT(CASE WHEN status = "Cancelled" THEN 1 END) AS cancel,
		 COUNT(CASE WHEN gender = "Male" THEN 1 END) AS male,
		 COUNT(CASE WHEN gender = "Female" THEN 1 END) AS female
		 from `tabInpatient Record`
		where admitted_datetime between '{from_date}' and '{to_date}'				   


	""", as_dict =1)


	summaries = [
				{
				"icon": "fa fa-money",
				"title": "Admission Scheduled",
				"data": inp_reco[0].sch
				},
				{
				"icon": "fa fa-money",
				"title": "Admitted",
				"data": inp_reco[0].admitted
				},
					{
				"icon": "fa fa-money",
				"title": "Discharge Scheduled",
				"data": inp_reco[0].dis_sch
				},
				{
				"icon": "fa fa-money",
				"title": "Discharged",
				"data": inp_reco[0].discharged
				},
					{
				"icon": "fa fa-money",
				"title": "Cancelled",
				"data": inp_reco[0].cancel
				},
			

				
				]
	data = frappe.db.sql(f""" 


			select patient  ,  patient_name , gender ,admission_practitioner ,medical_department, admitted_datetime  from `tabInpatient Record`
					  
					  
			where admitted_datetime between '{from_date}' and '{to_date}'			  
		 ;
			
		""", as_dict =1)
	data_pia_chart =[{
				"name": "Male",
				"y":  inp_reco[0].male
			},
			{
				"name": "Female",
				"y":  inp_reco[0].female
			}
			]
	# # data_chart = []
	# # for test in data[:11]:
	# # 	data_chart.append({
	# # 			"name": test.test_name,
	# # 			# "name" : user.owner,
	# # 			"y": test.number ,
	# # 			# "drilldown": doctor.name
	# # 		})
	# # frappe.errprint(data_chart)

	# series = [
	# 	{
	# 		"name": 'Test',
	# 		"genderByPoint": "true",
	# 		"data" : data_chart
					
	# 	}
	# ],
	# yAxis = ""
	charts = [
	# {
	# "chart_type" : "column",
	# "series" : series,
	# "drilldown" :{},
	# "chart_title" : "Top 10 Most Lab Tests",
	# "chart_subtitle" : "",
	# "yAxis" : yAxis 
	# },
	{
		"chart_type" :"pie",
		"data" : data_pia_chart,
		"chart_title" : "Female vs Male",
		"chart_subtitle" : ""
	}
	]
	for d in data:
		for k in d:
			
			if k  in ['admitted_datetime' , 'creation' , 'modified' ,'time']:
				
				d[k] =str(frappe.format(d[k]))
	
	table = [
		{
			"columns":[
	# {"title":"Date", "field":"posting_date"},
	{"title":"Patient", "field":"patient"},
	{"title":"Patient Name", "field":"patient_name"},
	{"title":"Sex", "field":"gender"},
	{"title":"Doctor", "field":"admission_practitioner"},
	{"title":"Department", "field":"medical_department"},
	{"title":"Admision Date", "field":"admitted_datetime"},


	
	],
	"data" : data
	}]
	report_html_data = frappe.render_template(
	"rasiin_design/templates/Report/medical_report.html",
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




@frappe.whitelist()
def get_theater(from_date =  getdate() , to_date = getdate() ,withsidebar = 1 , loading = 1):
	from_date = getdate(from_date)
	to_date = getdate(to_date)
	clin_pro = frappe.db.sql(f"""


		select COUNT(name) AS total from `tabClinical Procedure` 
		where creation between '{from_date}' and '{to_date}'					   


	""", as_dict =1)


	summaries = [
				{
				"icon": "fa fa-money",
				"title": "Total Procedures",
				"data": clin_pro[0].total
				},
				
			

				
				]
	data = frappe.db.sql(f""" 


			select procedure_type , COUNT(name ) AS number from `tabClinical Procedure` 
					  
			where creation between '{from_date}' and '{to_date}'	
			group by procedure_type
					  
				 ;
			
		""", as_dict =1)
	# data_pia_chart =[{
	# 			"name": "Male",
	# 			"y":  inp_reco[0].male
	# 		},
	# 		{
	# 			"name": "Female",
	# 			"y":  inp_reco[0].female
	# 		}
	# 		]
	
	data_chart = []
	for pro in data:
		data_chart.append({
				"name": pro.procedure_type,
				# "name" : user.owner,
				"y": pro.number ,
				# "drilldown": doctor.name
			})
	# # frappe.errprint(data_chart)

	series = [
		{
			"name": 'Test',
			"genderByPoint": "true",
			"data" : data_chart
					
		}
	],
	yAxis = "Number of Procedures"
	charts = [
	{
	"chart_type" : "column",
	"series" : series,
	"drilldown" :{},
	"chart_title" : "Procedure Types",
	"chart_subtitle" : "",
	"yAxis" : yAxis 
	},
	# {
	# 	"chart_type" :"pie",
	# 	"data" : data_pia_chart,
	# 	"chart_title" : "Female vs Male",
	# 	"chart_subtitle" : ""
	# }
	]
	pro_data = frappe.db.sql(f"""

		select 
		procedure_type,
		patient,
		patient_name,
		patient_sex,
		patient_age,
		procedure_type,
		procedure_template,
						  
		practitioner,
		medical_department,
		start_date,
		start_time,
		end_time,
		custom_circulating_nurse
		from `tabClinical Procedure` 	
	 """, as_dict =1)
	for d in pro_data:
		for k in d:
			
			if k  in ['start_date' , 'start_time' , 'end_time' ]:
				
				d[k] =str(frappe.format(d[k]))
	
	table = [
		{
			"columns":[
	# {"title":"Date", "field":"posting_date"},
	{"title":"Patient", "field":"patient"},
	{"title":"Patient Name", "field":"patient_name"},
	{"title":"Sex", "field":"patient_sex"},
	{"title":"Procedure Type", "field":"procedure_type"},
	{"title":"Procedure Name", "field":"procedure_template"},
	{"title":"Doctor", "field":"practitioner"},
	{"title":"Department", "field":"medical_department"},
	{"title":"Date", "field":"start_date"},
	{"title":"Start Time", "field":"start_time"},
	{"title":"End Time", "field":"end_time"},
	{"title":"Circulating Nurse", "field":"custom_circulating_nurse"},


	
	],
	"data" : pro_data
	}]
	report_html_data = frappe.render_template(
	"rasiin_design/templates/Report/medical_report.html",
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






def get_que_report(from_date , to_date):
	report_gl = frappe.get_doc("Report", "Que Reports")
	report_gl_filters = {
			"from_date": getdate(from_date),
			"to_date": getdate(to_date),
		   
		}
	columns_gl, data = report_gl.get_data(
			limit=500, user="Administrator", filters=report_gl_filters, as_dict=True)
	frappe.errprint(data)
	if data:
		return data