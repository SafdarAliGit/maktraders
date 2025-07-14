
frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        
    }
})
frappe.ui.form.on('Sales Invoice Item', {
    item_code: function(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (!row.item_code) return;

        setTimeout(() => {
            frappe.call({
                method: "maktraders.api.get_item_tp.get_item_tp",
                args: {
                    item_code: row.item_code
                },
                callback: function(r) {
                    if (!r.exc) {
                        frappe.model.set_value(cdt, cdn, 'rate', r.message);
                        if (row.disc_percent) {
                            calculate_rate(frm, cdt, cdn);
                        }
                    }
                }
            });
        }, 500);
    },

    disc_percent: function(frm, cdt, cdn) {
        calculate_rate(frm, cdt, cdn);
    }
});

function calculate_rate(frm, cdt, cdn) {
    let row = locals[cdt][cdn];
    let tp = flt(row.tp) || 0;
    let disc_percent = flt(row.disc_percent);

    if (isNaN(disc_percent) || disc_percent === null || disc_percent === "") {
        frappe.model.set_value(cdt, cdn, 'rate', tp);
        return;
    }

    if (disc_percent < 0 || disc_percent > 100) {
        frappe.msgprint(__('Discount must be between 0-100%'));
        frappe.model.set_value(cdt, cdn, 'disc_percent', 0);
        frappe.model.set_value(cdt, cdn, 'rate', tp);
        return;
    }

    let rate = tp - (tp * disc_percent / 100);
    frappe.model.set_value(cdt, cdn, 'rate', flt(rate));
}