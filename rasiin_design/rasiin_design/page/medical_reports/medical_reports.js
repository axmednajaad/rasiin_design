
frappe.pages['medical-reports'].on_page_load = function(wrapper) {
	new MedicalReport(wrapper)
	}
	
	MedicalReport = Class.extend(
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
					console.log(this.datepicker._prevOnSelectValue)
					$('#from_date').html(this.datepicker._prevOnSelectValue)
	
					// console.log(to_date.datepicker._prevOnSelectValue)
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
					// console.log(from_date.datepicker._prevOnSelectValue)	

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
					// console.log(to_date.datepicker._prevOnSelectValue)
					// console.log(from_date.datepicker._prevOnSelectValue)	
					// console.log($('#report_name').html())
					let func_name = $('#report_name').html()

					$('#from_date').html(from_date.datepicker._prevOnSelectValue)
					$('#to_date').html(to_date.datepicker._prevOnSelectValue)
					// console.log(func_name)
					window[func_name](); 
				},
				render_input: true
			})
			
			// alert(this.reportname)
			prepare_layout()
			get_patient_visit(loading = 1)
		}
	})
	
	
	
	function get_patient_visit(loading = 0){
		// $('#dyreport').remove()
		// prepare_layout()
		$('#report_name').html("get_patient_visit")
		let f_date = $('#from_date').html()
		let t_date = $('#to_date').html()
	
		frappe.call({
			method: "rasiin_design.api.medical_report.get_patient_visit", //dotted path to server method
			args : {"loading" : loading , "from_date" : f_date , "to_date" : t_date},
			//  args : {"load_a" : currdate , to_date : to_date},
			callback: function(r) {
				
				// console.log(window.open.document)
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
	

	function get_report_doctor_wise_visit(){
		$('#report_name').html("get_report_doctor_wise_visit")
		let f_date = $('#from_date').html()
		let t_date = $('#to_date').html()
		
		frappe.call({
			method: "rasiin_design.api.medical_report.get_report_doctor_wise_visit", //dotted path to server method
			args : {"loading" : loading , "from_date" : f_date , "to_date" : t_date},
			//  args : {"load_a" : currdate , to_date : to_date},
			callback: function(r) {
				
				// console.log(window.open.document)
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

	function get_report_diagnose(){
		$('#report_name').html("get_report_diagnose")
		let f_date = $('#from_date').html()
		let t_date = $('#to_date').html()
		
		frappe.call({
			method: "rasiin_design.api.medical_report.get_report_diagnose", //dotted path to server method
			args : {"loading" : loading , "from_date" : f_date , "to_date" : t_date},
			//  args : {"load_a" : currdate , to_date : to_date},
			callback: function(r) {
				
				// console.log(window.open.document)
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

	
	function get_report_lab(){
		$('#report_name').html("get_report_lab")
		let f_date = $('#from_date').html()
		let t_date = $('#to_date').html()
	
	
		frappe.call({
			method: "rasiin_design.api.medical_report.get_report_lab", //dotted path to server method
			args : {"loading" : loading , "from_date" : f_date , "to_date" : t_date},
			//  args : {"load_a" : currdate , to_date : to_date},
			callback: function(r) {
				
				// console.log(window.open.document)
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

	function get_report_radiolgy(){
		$('#report_name').html("get_report_radiolgy")
		let f_date = $('#from_date').html()
		let t_date = $('#to_date').html()
		
		frappe.call({
			method: "rasiin_design.api.medical_report.get_report_radiolgy", //dotted path to server method
			args : {"loading" : loading , "from_date" : f_date , "to_date" : t_date},
			//  args : {"load_a" : currdate , to_date : to_date},
			callback: function(r) {
				
				// console.log(window.open.document)
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

	function get_report_inpatient(){
		$('#report_name').html("get_report_inpatient")
		let f_date = $('#from_date').html()
		let t_date = $('#to_date').html()
		
		frappe.call({
			method: "rasiin_design.api.medical_report.get_report_inpatient", //dotted path to server method
			args : {"loading" : loading , "from_date" : f_date , "to_date" : t_date},
			//  args : {"load_a" : currdate , to_date : to_date},
			callback: function(r) {
				
				// console.log(window.open.document)
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

	
	function get_theater(){
		$('#report_name').html("get_theater")
		let f_date = $('#from_date').html()
		let t_date = $('#to_date').html()
		
		frappe.call({
			method: "rasiin_design.api.medical_report.get_theater", //dotted path to server method
			args : {"loading" : loading , "from_date" : f_date , "to_date" : t_date},
			//  args : {"load_a" : currdate , to_date : to_date},
			callback: function(r) {
				
				// console.log(window.open.document)
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
	function get_hmtl_sales(){

		frappe.call({
			method: "rasiin_design.api.medical_report.get_report_design", //dotted path to server method
			args : {"loading" : 1},
			//  args : {"load_a" : currdate , to_date : to_date},
			callback: function(r) {
				
				// console.log(window.open.document)
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
	
	function print_dy_report(){
		frappe.call({
			method: "rasiin_design.api.api.get_report_design", //dotted path to server method
			// args : {"from_date" : from_date , "to_date" : to_date},
			 args : {"withsidebar" : 0 },
			callback: function(r) {
				
				// console.log(window.open.document)
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
	
	
	
	function get_report_sales(){
		$('#dyreport').remove()
		$('.page-container').append("<div id ='dyreport'></div>")
		frappe.call({
			method: "rasiin_design.api.api.get_report_sales", //dotted path to server method
			args : {"loading" : 0},
			//  args : {"load_a" : currdate , to_date : to_date},
			callback: function(r) {
				
				// console.log(window.open.document)
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
		  <a href="">Medical Report</a>
		  <span>
			<i class="fa-solid fa-x close_menu"></i>
		  </span>
		</div>
		<div class="links">
		  <a href="#" class="link active_link">
			<span onclick="get_patient_visit()">🏢</span>
			<span onclick="get_patient_visit()">Patient Visit</span>
		  </a>
		  <a href="#" class="link">
			<span onclick="get_report_doctor_wise_visit()">🏢</span>
			<span onclick="get_report_doctor_wise_visit()">Doctor/Dep wise Visit</span>
		  </a>
		  <a href="#" class="link">
			<span onclick="get_report_diagnose()">🏢</span>
			<span onclick="get_report_diagnose()">Diagnose</span>
		  </a>
		  <a href="#" class="link">
			<span onclick="get_report_lab()">🏢</span>
			<span onclick="get_report_lab()">Lab Reports</span>
		  </a>
		  <a href="#" class="link">
			<span onclick="get_report_radiolgy()">🏢</span>
			<span onclick="get_report_radiolgy()">Radiolgy</span>
		  </a>
		  <a href="#" class="link">
			<span onclick="get_report_inpatient()">🏢</span>
			<span onclick="get_report_inpatient()">Inpatient</span>
		  </a>
		  <a href="#" class="link">
			<span onclick="get_theater()">🏢</span>
			<span onclick="get_theater()">Theater </span>
		  </a>
		
		  
		</div>
	  </aside>
		
		</div>
		<div id ='dyreport'></div>

		</div>
		
		
		`)
	}