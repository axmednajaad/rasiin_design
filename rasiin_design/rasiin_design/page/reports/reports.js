
frappe.pages['reports'].on_page_load = function(wrapper) {
new Reports(wrapper)
}

Reports = Class.extend(
{
	init:function(wrapper){
		this.reportname = frappe.route_options.reportname
		this.page = frappe.ui.make_app_page({
			parent : wrapper,
			title: this.reportname,
			single_column : true
		});
		$('.page-head').remove()
		$('.container').remove()
		
		this.make()
		
		// this.make_grouping_btn()
		// this.grouping_cols()
	},
	make:function(){
		$('#page-container').empty()
		$('.page-container').append("<div id ='controls'><span id ='report_name' hidden> Patient Visit</span></div>")
		$('.page-container').append("<div id ='controls'><span id ='from_date' hidden> </span></div>")
		$('.page-container').append("<div id ='controls'><span id ='to_date' hidden> </span></div>")

		$('.page-container').append(`
		<div id  = "report_page" > 
		
		<div id = "report_sidebar> test</div>
		<div id ='dyreport'></div>

		</div>
		
		
		`)
	
	
		let from_date = frappe.ui.form.make_control({
			parent: $('#controls'),
			df: {
				label: 'From Date',
				fieldname: 'from_date',
				fieldtype: 'Date',
				
			},
			// on_change:
			value : frappe.datetime.add_months(frappe.datetime.now_date(), -1),
			render_input: true,
			change : function(){
			
				$('#from_date').html(this.datepicker._prevOnSelectValue)

		
			}
		})
		// from_date.value = "2021-2-2"
	


		let to_date =frappe.ui.form.make_control({
			parent: $('#controls'),
			df: {
				label: 'To Date',
				fieldname: 'to_date',
				fieldtype: 'Date',
				// default: "2023-1-20"
			},
			// on_change:
			value : frappe.datetime.now_date(),
			render_input: true,
			change : function(){
				$('#to_date').html(this.datepicker._prevOnSelectValue)
			

						}
		})

		frappe.ui.form.make_control({
			parent: $('#controls'),
			df: {
			label: 'Load Report',
			fieldname: 'print',
			fieldtype: 'Button',
			btn_size: 'lg' // xs, sm, lg,
		},
			// on_change:
			onclick : function(){
			
				let func_name = $('#report_name').html()

				$('#from_date').html(from_date.datepicker._prevOnSelectValue)
				$('#to_date').html(to_date.datepicker._prevOnSelectValue)
			
				window[func_name](); 
			},
			render_input: true
		})
		
		// alert(this.reportname)
		prepare_layout()
		get_report_sales(loading = 1)
	}
})

function get_inpatient_due_admited(loading = 0){
	$('#report_name').html("get_inpatient_due_admited")
	let f_date = $('#from_date').html()
	let t_date = $('#to_date').html()

	frappe.call({
		method: "rasiin_design.api.api.get_inpatient_due", //dotted path to server method

		args : {"loading" : loading , status:"Admitted" , "from_date" : f_date , "to_date" : t_date},
		//  args : {"load_a" : currdate , to_date : to_date},
		callback: function(r) {
			
			
			// var x = window;
			// x.document.open().write(r.message);
			// code snippet
			// $(frappe.render_template(frappe.render_template('dashboard_page' ,{"data" : r.message }), me)).appendTo(me.page.main)
			// tbldata = r.message
			// let html = $('.page-body').html()
			
			$('#dyreport').html(r.message)

			

			


			// Button
			
	
		}})
}

function get_inpatient_due_discharged(loading = 0){
	$('#report_name').html("get_inpatient_due_discharged")
	let f_date = $('#from_date').html()
	let t_date = $('#to_date').html()
	
	frappe.call({
		method: "rasiin_design.api.api.get_inpatient_due", //dotted path to server method
	
		args : {"loading" : loading ,status:"Discharged", "from_date" : f_date , "to_date" : t_date},
		//  args : {"load_a" : currdate , to_date : to_date},
		callback: function(r) {
			
			
			// var x = window;
			// x.document.open().write(r.message);
			// code snippet
			// $(frappe.render_template(frappe.render_template('dashboard_page' ,{"data" : r.message }), me)).appendTo(me.page.main)
			// tbldata = r.message
			// let html = $('.page-body').html()
			
			$('#dyreport').html(r.message)

			

			


			// Button
			
	
		}})
}


function get_report_descount(loading = 0){
	$('#report_name').html("get_report_descount")
	let f_date = $('#from_date').html()
	let t_date = $('#to_date').html()
	
	frappe.call({
		method: "rasiin_design.api.api.get_report_descount", //dotted path to server method
		args : {"loading" : loading , "from_date" : f_date , "to_date" : t_date},
		//  args : {"load_a" : currdate , to_date : to_date},
		callback: function(r) {
			
			
			// var x = window;
			// x.document.open().write(r.message);
			// code snippet
			// $(frappe.render_template(frappe.render_template('dashboard_page' ,{"data" : r.message }), me)).appendTo(me.page.main)
			// tbldata = r.message
			// let html = $('.page-body').html()
			
			$('#dyreport').html(r.message)

			

			


			// Button
			
	
		}})
}

function get_hmtl_sales(loading = 0){
	$('#dyreport').remove()
	$('.page-container').append("<div id ='dyreport'></div>")
	frappe.call({
		method: "rasiin_design.api.api.get_report_sales", //dotted path to server method
		args : {"loading" : 1},
		//  args : {"load_a" : currdate , to_date : to_date},
		callback: function(r) {
			
			
			// var x = window;
			// x.document.open().write(r.message);
			// code snippet
			// $(frappe.render_template(frappe.render_template('dashboard_page' ,{"data" : r.message }), me)).appendTo(me.page.main)
			// tbldata = r.message
			// let html = $('.page-body').html()
			
			$('#dyreport').html(r.message)

			

			


			// Button
			
	
		}})
}

function print_dy_report(loading = 0){
	frappe.call({
		method: "rasiin_design.api.api.get_report_design", //dotted path to server method
		// args : {"from_date" : from_date , "to_date" : to_date},
		 args : {"withsidebar" : 0 },
		callback: function(r) {
			
			
			// var x = window;
			// x.document.open().write(r.message);
			// code snippet
			// $(frappe.render_template(frappe.render_template('dashboard_page' ,{"data" : r.message }), me)).appendTo(me.page.main)
			// tbldata = r.message
			// let html = $('.page-body').html()
			
			var x = window.open();
			x.document.write(r.message);

			

			


			// Button
			
	
		}})
}
// print()



function get_report_sales(loading = 0){
	$('#report_name').html("get_report_sales")
	let f_date = $('#from_date').html()
	let t_date = $('#to_date').html()
	
	frappe.call({
		method: "rasiin_design.api.api.get_report_sales", //dotted path to server method
		args : {"loading" : loading , "from_date" : f_date.toString() , "to_date" : t_date.toString()},
		//  args : {"load_a" : currdate , to_date : to_date},
		callback: function(r) {
			
		
			// var x = window;
			// x.document.open().write(r.message);
			// code snippet
			// $(frappe.render_template(frappe.render_template('dashboard_page' ,{"data" : r.message }), me)).appendTo(me.page.main)
			// tbldata = r.message
			// let html = $('.page-body').html()
			
			$('#dyreport').html(r.message)

			

			


			// Button
			
	
		}})
}

function get_report_sales_return(loading = 0){
	$('#report_name').html("get_report_sales_return")
	let f_date = $('#from_date').html()
	let t_date = $('#to_date').html()

	frappe.call({
		method: "rasiin_design.api.api.get_report_sales_return", //dotted path to server method
		args : {"loading" : loading , "from_date" : f_date , "to_date" : t_date},
		//  args : {"load_a" : currdate , to_date : to_date},
		callback: function(r) {
			
			// var x = window;
			// x.document.open().write(r.message);
			// code snippet
			// $(frappe.render_template(frappe.render_template('dashboard_page' ,{"data" : r.message }), me)).appendTo(me.page.main)
			// tbldata = r.message
			// let html = $('.page-body').html()
			
			$('#dyreport').html(r.message)

			

			


			// Button
			
	
		}})
}


function get_report_reciept(loading = 0){
	$('#report_name').html("get_report_reciept")
	let f_date = $('#from_date').html()
	let t_date = $('#to_date').html()
	
	
	frappe.call({
		method: "rasiin_design.api.api.get_report_reciept", //dotted path to server method
		args : {"loading" : loading , "from_date" : f_date , "to_date" : t_date},
		//  args : {"load_a" : currdate , to_date : to_date},
		callback: function(r) {
			
		
			// var x = window;
			// x.document.open().write(r.message);
			// code snippet
			// $(frappe.render_template(frappe.render_template('dashboard_page' ,{"data" : r.message }), me)).appendTo(me.page.main)
			// tbldata = r.message
			// let html = $('.page-body').html()
			
			$('#dyreport').html(r.message)

			

			


			// Button
			
	
		}})
}


function get_commission_due(loading = 0){
	$('#report_name').html("get_commission_due")
	let f_date = $('#from_date').html()
	let t_date = $('#to_date').html()
	
	frappe.call({
		method: "rasiin_design.api.api.get_commission_due", //dotted path to server method
		args : {"loading" : loading , "from_date" : f_date , "to_date" : t_date},
		//  args : {"load_a" : currdate , to_date : to_date},
		callback: function(r) {
			
			
			// var x = window;
			// x.document.open().write(r.message);
			// code snippet
			// $(frappe.render_template(frappe.render_template('dashboard_page' ,{"data" : r.message }), me)).appendTo(me.page.main)
			// tbldata = r.message
			// let html = $('.page-body').html()
			
			$('#dyreport').html(r.message)

			

			


			// Button
			
	
		}})
}


function get_payable_summary(loading = 0){
	$('#report_name').html("get_payable_summary")
	let f_date = $('#from_date').html()
	let t_date = $('#to_date').html()

	frappe.call({
		method: "rasiin_design.api.api.get_payable_summary", //dotted path to server method
		args : {"loading" : loading , "from_date" : f_date , "to_date" : t_date},
		//  args : {"load_a" : currdate , to_date : to_date},
		callback: function(r) {
			
	
			// var x = window;
			// x.document.open().write(r.message);
			// code snippet
			// $(frappe.render_template(frappe.render_template('dashboard_page' ,{"data" : r.message }), me)).appendTo(me.page.main)
			// tbldata = r.message
			// let html = $('.page-body').html()
			
			$('#dyreport').html(r.message)

			

			


			// Button
			
	
		}})
}



function get_opd_sales_report(loading = 0){
	$('#report_name').html("get_opd_sales_report")
	let f_date = $('#from_date').html()
	let t_date = $('#to_date').html()

	frappe.call({
		method: "rasiin_design.api.api.get_opd_sales_report", //dotted path to server method
		args : {"loading" : loading , "from_date" : f_date , "to_date" : t_date},
		//  args : {"load_a" : currdate , to_date : to_date},
		callback: function(r) {
			
		
			// var x = window;
			// x.document.open().write(r.message);
			// code snippet
			// $(frappe.render_template(frappe.render_template('dashboard_page' ,{"data" : r.message }), me)).appendTo(me.page.main)
			// tbldata = r.message
			// let html = $('.page-body').html()
			
			$('#dyreport').html(r.message)

			

			


			// Button
			
	
		}})
}



function get_report_purchase_anaylsis(loading = 0){
	$('#report_name').html("get_report_purchase_anaylsis")
	let f_date = $('#from_date').html()
	let t_date = $('#to_date').html()
	
	
	frappe.call({
		method: "rasiin_design.api.api.get_report_purchase_anaylsis", //dotted path to server method
		args : {"loading" : loading , "from_date" : f_date , "to_date" : t_date},
		//  args : {"load_a" : currdate , to_date : to_date},
		callback: function(r) {
			
			
			// var x = window;
			// x.document.open().write(r.message);
			// code snippet
			// $(frappe.render_template(frappe.render_template('dashboard_page' ,{"data" : r.message }), me)).appendTo(me.page.main)
			// tbldata = r.message
			// let html = $('.page-body').html()
			
			$('#dyreport').html(r.message)

			

			


			// Button
			
	
		}})
}




function prepare_layout(){
		
	$('.page-container').append(`
	<div id ="report_page" >
	<div> 
	
	<aside class="sidebar">
	<div class="logo">
	  <a href="">Finance Report</a>
	  <span>
		<i class="fa-solid fa-x close_menu"></i>
	  </span>
	</div>
	<div class="links">
	  <a href="#" class="link active_link">
		<span onclick="get_report_sales()">🏢</span>
		<span onclick="get_report_sales()">Sales Report</span>
	  </a>
	  <a href="#" class="link">
		<span onclick="get_report_descount()">🏢</span>
		<span onclick="get_report_descount()">Sales Discount</span>
	  </a>
	  <a href="#" class="link">
		<span onclick="get_inpatient_due_admited()">🏢</span>
		<span onclick="get_inpatient_due_admited()">Admited Patient Balance</span>
	  </a>
	  <a href="#" class="link">
		<span onclick="get_inpatient_due_discharged()">🏢</span>
		<span onclick="get_inpatient_due_discharged()">Discharged Patient Balance</span>
	  </a>
	  <a href="#" class="link">
		<span onclick="get_report_purchase_anaylsis()">🏢</span>
		<span onclick="get_report_purchase_anaylsis()">Purchase Analysis</span>
	  </a>
	  <a href="#" class="link">
		<span onclick="get_report_sales_return()">🏢</span>
		<span onclick="get_report_sales_return()">Refund</span>
	  </a>
	  <a href="#" class="link">
		<span onclick="get_opd_sales_report()">🏢</span>
		<span onclick="get_opd_sales_report()">OPD Credit Sales</span>
	  </a>
	  <a href="#" class="link">
		<span onclick="get_report_reciept()">🏢</span>
		<span onclick="get_report_reciept()">Receipt Report</span>
	  </a>
	  <a href="#" class="link">
		<span onclick="get_payable_summary()">🏢</span>
		<span onclick="get_payable_summary()">Payable Summary</span>
	  </a>
	  <a href="#" class="link">
		<span onclick="get_commission_due()">🏢</span>
		<span onclick="get_commission_due()">Doctors Payable</span>
	  </a>
	  
	</div>
  </aside>
	
	</div>
	<div id ='dyreport'></div>

	</div>
	
	
	`)
}