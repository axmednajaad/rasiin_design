// Copyright (c) 2025, Rasiin and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Custom Notification", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Custom Notification', {
    refresh: function(frm) {
        //
    },
    
    // Validate recipient rules before save
    validate: function(frm) {
        var invalid_rows = [];
        
        $.each(frm.doc.recipients || [], function(i, row) {
            if (!row.recipient_type || !row.recipient_value) {
                invalid_rows.push(i + 1);
            }
        });
        
        if (invalid_rows.length > 0) {
            frappe.msgprint({
                title: __('Validation Error'),
                indicator: 'red',
                message: __('Please set both Recipient Type and Recipient Value for rows: {0}', [invalid_rows.join(', ')])
            });
            frappe.validated = false;
        }
    }
});

frappe.ui.form.on('Custom Notification Recipient', {
    recipient_type: function(frm, cdt, cdn) {
        var row = frappe.get_doc(cdt, cdn);
        
        // Clear recipient value when type changes
        frappe.model.set_value(cdt, cdn, 'recipient_value', '');
        
        // Refresh the field to update dynamic link options
        frm.refresh_field('recipients');
    },
    
    // Optional: Add some validation when form is saved
    form_render: function(frm) {
        frm.fields_dict.recipients.grid.wrapper.on('change', function(e) {
            var $target = $(e.target);
            if ($target.attr('data-fieldname') === 'recipient_value') {
                var row = $target.closest('.grid-row');
                var row_name = row.attr('data-name');
                var row_doc = frappe.get_doc('Custom Notification Recipient', row_name);
                
                // Basic validation
                if (row_doc.recipient_type && row_doc.recipient_value) {
                    // You can add additional validation here if needed
                }
            }
        });
    }
});