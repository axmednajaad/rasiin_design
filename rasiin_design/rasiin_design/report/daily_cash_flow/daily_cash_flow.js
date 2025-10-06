// daily_cash_flow.js
// Copyright (c) 2025, Rasiin and contributors
// For license information, please see license.txt

frappe.query_reports["Daily Cash Flow"] = {
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
            "fieldname": "account",
            "label": __("Cash/Bank Account"),
            "fieldtype": "Link",
            "options": "Account",
            "width": "80px",
            "get_query": function() {
                return {
                    "filters": {
                        "account_type": ["in", ["Cash", "Bank"]],
                        "is_group": 0
                    }
                };
            }
        },
        {
            "fieldname": "voucher_type",
            "label": __("Voucher Type"),
            "fieldtype": "Select",
            "options": "\nPayment Entry\nJournal Entry\nExpense Claim\nCash Entry\nBank Entry",
            "width": "80px"
        },
        {
            "fieldname": "party",
            "label": __("Party"),
            "fieldtype": "Data",
            "width": "80px"
        },
        {
            "fieldname": "mode_of_payment",
            "label": __("Payment Mode"),
            "fieldtype": "Link",
            "options": "Mode of Payment",
            "width": "80px"
        }
    ],

    "formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
        
        if (!data) return value;
        
        // Highlight opening/closing balance rows
        if (data.voucher_type === "Opening Balance" || data.voucher_type === "Closing Balance") {
            value = "<span style='font-weight: bold; background-color: #f8f9fa; padding: 2px 5px; border-radius: 3px;'>" + value + "</span>";
        }
        
        // Color coding for amounts
        if (column.fieldname === "debit" && data && data.debit > 0) {
            value = "<span style='color: #28a745; font-weight: bold;'>" + value + "</span>";
        }
        
        if (column.fieldname === "credit" && data && data.credit > 0) {
            value = "<span style='color: #dc3545; font-weight: bold;'>" + value + "</span>";
        }
        
        // Highlight negative balance
        if (column.fieldname === "balance" && data && data.balance < 0) {
            value = "<span style='color: #dc3545; font-weight: bold;'>" + value + "</span>";
        }
        
        // Highlight positive balance
        if (column.fieldname === "balance" && data && data.balance > 0) {
            value = "<span style='color: #28a745; font-weight: bold;'>" + value + "</span>";
        }
        
        // Style reference field for Sales Invoice (though excluded, keeping for other cases)
        if (column.fieldname === "custom_refrence" && data && data.voucher_type === "Sales Invoice" && data.custom_refrence) {
            value = "<span style='font-style: italic; color: #6c757d;'>" + value + "</span>";
        }
        
        return value;
    },

    "onload": function(report) {
        // Add custom button for cash flow summary
        report.page.add_inner_button(__("Cash Flow Summary"), function() {
            show_cash_flow_summary(report);
        });
        
        // Add custom button to toggle chart
        report.page.add_inner_button(__("Toggle Chart"), function() {
            var $chart = $(".chart-container, .widget-chart, [data-fieldname='chart']");
            
            if ($chart.length === 0) {
                frappe.msgprint(__("Chart not available"));
                return;
            }
            
            $chart.toggle();
            
            var state = $chart.is(":visible") ? "shown" : "hidden";
            frappe.show_alert({
                message: __("Chart {0}", [state]),
                indicator: state === "shown" ? "green" : "gray"
            });
        });
        
        // Add info about excluded vouchers
        report.page.add_inner_button(__("Report Info"), function() {
            frappe.msgprint({
                title: __("Cash Flow Report Information"),
                message: __(`
                    <div style="padding: 10px;">
                        <p><strong>This report shows only actual cash movements:</strong></p>
                        <ul>
                            <li>✅ <strong>Included:</strong> Payment Entries, Journal Entries, Expense Claims</li>
                            <li>❌ <strong>Excluded:</strong> Sales Invoices, Purchase Invoices (they represent accruals, not cash)</li>
                        </ul>
                        <p><em>Note: Cash impact occurs when payment is made/received, not when invoice is created.</em></p>
                    </div>
                `)
            });
        });
    },

    "after_datatable_render": function(datatable_obj) {
        // Add custom styling to datatable
        if (datatable_obj && datatable_obj.wrapper) {
            $(datatable_obj.wrapper).find(".dt-cell__content").css("padding", "4px 8px");
        }
    }
};

function show_cash_flow_summary(report) {
    var filters = report.get_values();
    
    frappe.call({
        method: "rasiin_design.rasiin_design.report.daily_cash_flow.daily_cash_flow.get_cash_flow_summary",
        args: {
            filters: filters
        },
        callback: function(r) {
            if (r.message) {
                var summary_data = r.message;
                show_summary_dialog(summary_data);
            }
        }
    });
}

function show_summary_dialog(summary_data) {
    var dialog = new frappe.ui.Dialog({
        title: __('Cash Flow Summary'),
        width: 800
    });
    
    var content = '';
    
    // Voucher Type Summary
    content += '<h5>' + __('Transaction Summary by Voucher Type') + '</h5>';
    content += '<div class="table-responsive" style="max-height: 300px; overflow-y: auto;">';
    content += '<table class="table table-bordered table-sm">';
    content += '<thead><tr>' +
        '<th>' + __('Voucher Type') + '</th>' +
        '<th>' + __('Transactions') + '</th>' +
        '<th>' + __('Cash In') + '</th>' +
        '<th>' + __('Cash Out') + '</th>' +
        '<th>' + __('Net Flow') + '</th>' +
        '</tr></thead><tbody>';
    
    if (summary_data.voucher_summary && summary_data.voucher_summary.length > 0) {
        summary_data.voucher_summary.forEach(function(row) {
            var net_flow_class = row.net_cash_flow >= 0 ? 'text-success' : 'text-danger';
            content += '<tr>' +
                '<td>' + (row.voucher_type || __('Unknown')) + '</td>' +
                '<td class="text-center">' + (row.total_transactions || 0) + '</td>' +
                '<td class="text-success">' + safe_format_currency(row.total_cash_in || 0) + '</td>' +
                '<td class="text-danger">' + safe_format_currency(row.total_cash_out || 0) + '</td>' +
                '<td class="' + net_flow_class + '">' + safe_format_currency(row.net_cash_flow || 0) + '</td>' +
                '</tr>';
        });
    } else {
        content += '<tr><td colspan="5" class="text-center text-muted">' + __('No transactions found') + '</td></tr>';
    }
    content += '</tbody></table></div>';
    
    // Top Cash Sources
    content += '<h5 class="mt-4">' + __('Top Cash Sources') + '</h5>';
    content += '<div class="table-responsive" style="max-height: 250px; overflow-y: auto;">';
    content += '<table class="table table-bordered table-sm">';
    content += '<thead><tr>' +
        '<th>' + __('Party') + '</th>' +
        '<th>' + __('Total Received') + '</th>' +
        '</tr></thead><tbody>';
    
    if (summary_data.top_cash_sources && summary_data.top_cash_sources.length > 0) {
        summary_data.top_cash_sources.forEach(function(row) {
            content += '<tr>' +
                '<td>' + (row.party || __('Unknown')) + '</td>' +
                '<td class="text-success">' + safe_format_currency(row.total_received || 0) + '</td>' +
                '</tr>';
        });
    } else {
        content += '<tr><td colspan="2" class="text-center text-muted">' + __('No cash receipts found') + '</td></tr>';
    }
    content += '</tbody></table></div>';
    
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