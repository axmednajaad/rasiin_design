// Copyright (c) 2023, Rasiin and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daynamic Report', {
	refresh: function(frm) {
		frm.add_custom_button(
			__("Show Report"), 
		function(){
			frappe.route_options = {'reportname': frm.doc.report_name };
			frappe.set_route('reports');
			//perform desired action such as routing to new form or fetching etc.
		
		  }),
		  "fa fa-table"

	}

});
