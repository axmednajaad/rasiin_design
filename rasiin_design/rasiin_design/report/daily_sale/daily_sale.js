// daily_sale.js
// Copyright (c) 2025, Rasiin and contributors
// For license information, please see license.txt

frappe.query_reports["Daily Sale"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.month_start(),
            "reqd": 1,
            "width": "80px"
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.month_end(),
            "reqd": 1,
            "width": "80px"
        },
        {
            "fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": "80px"
        },
        {
            "fieldname": "sales_person",
            "label": __("Sales Person"),
            "fieldtype": "Link",
            "options": "Sales Person",
            "width": "80px"
        },
        {
            "fieldname": "show_outstanding",
            "label": __("Show Outstanding"),
            "fieldtype": "Check",
            "default": 1,
            "width": "80px"
        }
    ],

    "formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		
		if (!data) return value;
		
		// Color coding for amounts
		if (column.fieldname === "total_amount" && data.total_amount > 10000) {
			value = "<span style='color: green; font-weight: bold;'>" + value + "</span>";
		}
		
		// Color coding for discount
		if (column.fieldname === "discount_amount" && data.discount_amount > 0) {
			value = "<span style='color: #ff5858;'>" + value + "</span>";
		}
		
		// Color coding for paid amount
		if (column.fieldname === "paid_amount") {
			if (data.paid_amount > 0) {
				value = "<span style='color: #28a745; font-weight: bold;'>" + value + "</span>";
			} else {
				value = "<span style='color: #6c757d;'>" + value + "</span>";
			}
		}
		
		// Color coding for outstanding amount
		if (column.fieldname === "outstanding_amount") {
			if (data.outstanding_amount > 0) {
				value = "<span style='color: #dc3545; font-weight: bold;'>" + value + "</span>";
			} else if (data.outstanding_amount < 0) {
				value = "<span style='color: #28a745; font-weight: bold;'>" + value + "</span>";
			} else {
				value = "<span style='color: #6c757d;'>" + value + "</span>";
			}
		}
		
		return value;
	},

    "onload": function(report) {
        // Initialize chart state
        report.chart_rendered = false;
        report.chart_visible = false;
        
        // Add chart toggle button
        report.page.add_inner_button(__("Toggle Charts"), function() {
            toggle_charts(report);
        });
        
        // Add refresh charts button
        report.page.add_inner_button(__("Refresh Charts"), function() {
            refresh_charts(report);
        });
        
        // Add outstanding summary button
        report.page.add_inner_button(__("Outstanding Summary"), function() {
            show_outstanding_summary(report);
        });
    },

    "after_datatable_render": function(datatable) {
        // Add custom styling
        $(datatable.wrapper).find(".dt-cell__content").css("padding", "4px 8px");
    }
};

// --- CHARTING FUNCTIONS ---

function toggle_charts(report) {
    let $chart_container = report.page.body.find(".chart-container");
    
    if ($chart_container.length === 0) {
        // Charts don't exist, render them
        render_charts(report);
        report.chart_visible = true;
    } else if ($chart_container.is(":visible")) {
        // Charts exist and are visible, hide them
        $chart_container.hide();
        report.chart_visible = false;
        frappe.show_alert({ message: __("Charts hidden"), indicator: "gray" });
    } else {
        // Charts exist but are hidden, show them
        $chart_container.show();
        report.chart_visible = true;
        frappe.show_alert({ message: __("Charts shown"), indicator: "green" });
    }
}

function refresh_charts(report) {
    // Remove existing charts
    report.page.body.find(".chart-container").remove();
    report.chart_rendered = false;
    
    // Render fresh charts
    render_charts(report);
    frappe.show_alert({ message: __("Charts refreshed"), indicator: "blue" });
}

function render_charts(report) {
    if (report.chart_rendered) return;
    
    let filters = report.get_values();

    // Create a proper container for charts
    let $chart_container = $(`
        <div class="chart-container" style="margin: 20px 0; padding: 20px; background: #f9f9f9; border-radius: 8px; border: 1px solid #d1d8dd;">
            <div style="display: flex; flex-wrap: wrap; gap: 30px; justify-content: center;">
                <div id="daily-trend-chart" style="flex: 1; min-width: 500px; min-height: 300px;"></div>
                <div id="customer-chart" style="flex: 1; min-width: 500px; min-height: 300px;"></div>
            </div>
        </div>
    `).appendTo(report.page.body);
    
    // Show loading state
    frappe.dom.freeze(__("Loading Charts..."));
    
    report.chart_rendered = true;

    frappe.call({
        method: "rasiin_design.rasiin_design.report.daily_sale.daily_sale.get_chart_data",
        args: {
            filters: filters
        },
        callback: function(r) {
            frappe.dom.unfreeze();
            
            if (r.message) {
                let chart_data = r.message;
                
                // Check if we have data for charts
                let has_daily_data = chart_data.daily_trend && chart_data.daily_trend.length > 0;
                let has_customer_data = chart_data.top_customers && chart_data.top_customers.length > 0;
                let has_outstanding_data = chart_data.outstanding_summary && chart_data.outstanding_summary.length > 0;
                
                if (has_daily_data) {
                    render_daily_trend_chart(chart_data.daily_trend);
                } else {
                    $("#daily-trend-chart").html(`
                        <div class="text-muted" style="text-align: center; padding: 50px;">
                            <i class="fa fa-bar-chart fa-2x" style="margin-bottom: 10px;"></i><br>
                            No daily sales data available
                        </div>
                    `);
                }
                
                if (has_customer_data) {
                    render_customer_chart(chart_data.top_customers);
                } else {
                    $("#customer-chart").html(`
                        <div class="text-muted" style="text-align: center; padding: 50px;">
                            <i class="fa fa-users fa-2x" style="margin-bottom: 10px;"></i><br>
                            No customer data available
                        </div>
                    `);
                }
                
                // Show message if no data at all
                if (!has_daily_data && !has_customer_data && !has_outstanding_data) {
                    $chart_container.html(`
                        <div class="text-muted" style="text-align: center; padding: 50px;">
                            <i class="fa fa-exclamation-triangle fa-2x" style="margin-bottom: 10px;"></i><br>
                            No chart data available for the selected period and filters.
                        </div>
                    `);
                }
            } else {
                // Handle API error
                $chart_container.html(`
                    <div class="text-danger" style="text-align: center; padding: 50px;">
                        <i class="fa fa-exclamation-circle fa-2x" style="margin-bottom: 10px;"></i><br>
                        Error loading chart data
                    </div>
                `);
            }
        },
        error: function() {
            frappe.dom.unfreeze();
            frappe.msgprint(__("Error loading chart data. Please try again."));
        }
    });
}

function render_daily_trend_chart(daily_data) {
    let chart = new frappe.Chart("#daily-trend-chart", {
        title: "Daily Sales Trend",
        data: {
            labels: daily_data.map(d => frappe.datetime.str_to_user(d.date)),
            datasets: [
                {
                    name: "Sales Amount",
                    values: daily_data.map(d => d.amount),
                    chartType: 'line'
                },
                {
                    name: "Discount", 
                    values: daily_data.map(d => d.discount),
                    chartType: 'line'
                }
            ]
        },
        type: 'axis-mixed',
        height: 280,
        colors: ["#5e64ff", "#ff5858"],
        axisOptions: {
            xIsSeries: true
        },
        lineOptions: {
            hideDots: 0,
            regionFill: 0
        }
    });
}

function render_customer_chart(customer_data) {
    let chart = new frappe.Chart("#customer-chart", {
        title: "Top Customers by Sales",
        data: {
            labels: customer_data.map(d => {
                // Truncate long customer names for better display
                let name = d.customer_name || d.customer || 'Unknown';
                return name.length > 20 ? name.substring(0, 20) + '...' : name;
            }),
            datasets: [{
                name: "Total Sales", 
                values: customer_data.map(d => d.total_sales)
            }]
        },
        type: 'bar',
        height: 280,
        colors: ["#743ee2"],
        barOptions: {
            spaceRatio: 0.5
        }
    });
}

function show_outstanding_summary(report) {
    let filters = report.get_values();
    
    frappe.call({
        method: "rasiin_design.rasiin_design.report.daily_sale.daily_sale.get_outstanding_summary",
        args: {
            filters: filters
        },
        callback: function(r) {
            if (r.message) {
                let summary_data = r.message;
                show_outstanding_dialog(summary_data);
            }
        }
    });
}

function show_outstanding_dialog(summary_data) {
    let dialog = new frappe.ui.Dialog({
        title: __('Outstanding Amount Summary'),
        width: 800
    });
    
    let content = '';
    
    // Total outstanding summary
    content += '<div class="alert alert-info" style="margin-bottom: 20px;">';
    content += '<h5>' + __('Total Outstanding: ') + '<strong>' + safe_format_currency(summary_data.total_outstanding || 0) + '</strong></h5>';
    content += '<p class="small text-muted mb-0">' + __('As of selected period') + '</p>';
    content += '</div>';
    
    // Outstanding by customer
    content += '<h5>' + __('Outstanding by Customer') + '</h5>';
    content += '<div class="table-responsive" style="max-height: 400px; overflow-y: auto;">';
    content += '<table class="table table-bordered table-sm">';
    content += '<thead><tr>' +
        '<th>' + __('Customer') + '</th>' +
        '<th>' + __('Total Sales') + '</th>' +
        '<th>' + __('Total Paid') + '</th>' +
        '<th>' + __('Outstanding') + '</th>' +
        '</tr></thead><tbody>';
    
    if (summary_data.customer_outstanding && summary_data.customer_outstanding.length > 0) {
        summary_data.customer_outstanding.forEach(function(row) {
            let outstanding_class = row.outstanding_amount > 0 ? 'text-danger' : (row.outstanding_amount < 0 ? 'text-success' : 'text-muted');
            content += '<tr>' +
                '<td>' + (row.customer_name || row.customer || __('Unknown')) + '</td>' +
                '<td class="text-right">' + safe_format_currency(row.total_sales || 0) + '</td>' +
                '<td class="text-right">' + safe_format_currency(row.total_paid || 0) + '</td>' +
                '<td class="text-right ' + outstanding_class + '"><strong>' + safe_format_currency(row.outstanding_amount || 0) + '</strong></td>' +
                '</tr>';
        });
    } else {
        content += '<tr><td colspan="4" class="text-center text-muted">' + __('No outstanding data found') + '</td></tr>';
    }
    content += '</tbody></table></div>';
    
    // Aging summary if available
    if (summary_data.aging_summary) {
        content += '<h5 class="mt-4">' + __('Aging Summary') + '</h5>';
        content += '<div class="table-responsive">';
        content += '<table class="table table-bordered table-sm">';
        content += '<thead><tr>' +
            '<th>' + __('0-30 Days') + '</th>' +
            '<th>' + __('31-60 Days') + '</th>' +
            '<th>' + __('61-90 Days') + '</th>' +
            '<th>' + __('Over 90 Days') + '</th>' +
            '</tr></thead><tbody><tr>';
        
        content += '<td class="text-right ' + (summary_data.aging_summary.range1 > 0 ? 'text-warning' : 'text-muted') + '">' + 
            safe_format_currency(summary_data.aging_summary.range1 || 0) + '</td>';
        content += '<td class="text-right ' + (summary_data.aging_summary.range2 > 0 ? 'text-warning' : 'text-muted') + '">' + 
            safe_format_currency(summary_data.aging_summary.range2 || 0) + '</td>';
        content += '<td class="text-right ' + (summary_data.aging_summary.range3 > 0 ? 'text-danger' : 'text-muted') + '">' + 
            safe_format_currency(summary_data.aging_summary.range3 || 0) + '</td>';
        content += '<td class="text-right ' + (summary_data.aging_summary.range4 > 0 ? 'text-danger' : 'text-muted') + '">' + 
            safe_format_currency(summary_data.aging_summary.range4 || 0) + '</td>';
        content += '</tr></tbody></table></div>';
    }
    
    dialog.$body.html(content);
    dialog.show();
}

// Safe currency formatting without recursion
function safe_format_currency(amount) {
    if (amount === null || amount === undefined) return '0.00';
    
    // Simple formatting without using frappe.format to avoid recursion
    var formatted = parseFloat(amount).toFixed(2);
    var parts = formatted.split('.');
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    
    // Get currency symbol from system defaults
    var currency_symbol = frappe.boot.sysdefaults.currency_symbol || '$';
    
    return currency_symbol + ' ' + parts.join('.');
}