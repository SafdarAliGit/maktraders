frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        
    }
})
frappe.ui.form.on('Sales Invoice Item', {
    item_code: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (!row.item_code) return;

        // Fetch TP from server
        frappe.call({
            method: "maktraders.api.get_item_tp.get_item_tp",
            args: {
                item_code: row.item_code
            },
            callback: function(r) {
                if (!r.exc) {
                    // Set TP value
                    frappe.model.set_value(cdt, cdn, 'tp', r.message);
                    
                    // Set initial rate = TP
                    frappe.model.set_value(cdt, cdn, 'rate', r.message);
                    
                    // If discount exists, calculate discounted rate
                    if (row.disc_percent) {
                        calculate_rate(frm, cdt, cdn);
                    }
                }
            }
        });
    },

    disc_percent: function(frm, cdt, cdn) {
        calculate_rate(frm, cdt, cdn);
    }
});

function calculate_rate(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let tp = flt(row.tp) || 0;
    let disc_percent = flt(row.disc_percent);

    // Case 1: No discount or invalid - set rate = tp
    if (isNaN(disc_percent) || disc_percent === null || disc_percent === "") {
        frappe.model.set_value(cdt, cdn, 'rate', tp);
        return;
    }

    // Case 2: Invalid discount range - reset to 0 and set rate = tp
    if (disc_percent < 0 || disc_percent > 100) {
        frappe.msgprint(__('Discount must be between 0-100%'));
        frappe.model.set_value(cdt, cdn, 'disc_percent', 0);
        frappe.model.set_value(cdt, cdn, 'rate', tp);
        return;
    }

    // Case 3: Valid discount - calculate discounted rate
    let rate = tp - (tp * disc_percent / 100);
    frappe.model.set_value(cdt, cdn, 'rate', flt(rate));
}