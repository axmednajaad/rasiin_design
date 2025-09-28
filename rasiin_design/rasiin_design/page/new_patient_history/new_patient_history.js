
frappe.pages['new-patient-history'].on_page_load = function(wrapper) {
	new newPatientHistory(wrapper)
	}
	
	newPatientHistory = Class.extend(
	{
		init:function(wrapper){
			this.reportname = frappe.route_options.reportname
			this.page = frappe.ui.make_app_page({
				parent : wrapper,
				title: "Patient History",
				single_column : true
			});
			this.make()
		},
		make:function(){
			frappe.call({
				method: "rasiin_design.api.p_history.get_history", //dotted path to server method
				args : {"patient" : "PID-00023"},
				//  args : {"load_a" : currdate , to_date : to_date},
				callback: function(r) {
					
					// console.log(window.open.document)
					var x = window;
					x.document.open().write(r.message);
					
					
			
				}})
		}
	})