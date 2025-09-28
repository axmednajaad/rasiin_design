import frappe
from frappe.utils import getdate
from datetime import datetime # from python std library
from frappe.utils import add_to_date
years = add_to_date(getdate(), years=-1) 

@frappe.whitelist()
def get_history(patient , from_date = "2019-01-01", to_date = getdate()):
    history_config = frappe.get_doc("Patient History Congiration" , "Patient History Congiration")
    p_history = []
    conditions  = ''
  
    for config in history_config.history_document:
        table_header  = []
        if config.condition:
            conditions = f"and {config.condition}"
        join = ''
        fields = ''
        join_fields = ''
        if config.parent_document_fields:
            p_fields = config.parent_document_fields.split(",")
            for f in p_fields:
                fields += "p." + f +','
                he = f.replace("_" , " ").title()
                table_header.append(he)
       

        if config.child_document_fields:
            p_fields = config.child_document_fields.split(",")
            for f in p_fields:
                join_fields += "c." + f +','
                he = f.replace("_" , " ").title()
                table_header.append(he)
        join_fields = join_fields[:-1]
        if not join_fields:
             fields = fields[:-1]
        if config.child_document:
            join = f'left join `tab{config.child_document}`  c on p.name =  c.parent' 

        data = frappe.db.sql(f"""
            select {fields}  {join_fields}
            from `tab{config.parent_document}`p
            {join}
            where patient  = '{patient}'

        
         """ , as_dict = 1)
        p_history.append({"data" : data , "header" : table_header , "heading" : config.heading})
    # frappe.errprint(p_history)
    report_html_data = frappe.render_template(
	"rasiin_design/templates/Report/p_history.html",
        {

        "patient" : patient,
        "table": p_history,

        }
	)
	# html = frappe.render_template(
	# 	base_template_path,
	# 	{"body": report_html_data ,"css" : get_print_style() , "title": "Statement For "},
	# )
    
    return report_html_data

