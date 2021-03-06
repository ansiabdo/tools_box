// Copyright (c) 2017, masonarmani38@gmail.com and contributors
// For license information, please see license.txt

var allowed = {};
// fetch is going to be based on the item type


frappe.ui.form.on('Vehicle Schedule', {
    refresh: function (frm) {
        var status = frm.doc.docstatus;
        var can_create_po = frappe.user_roles.includes("Purchase User");
        if (status && frm.doc.type == "Outbound") {
            cur_frm.add_custom_button(
                __("Make Delivery Tracking"), function () {
                    // do some kind of mapping and create a new purchase order
                    frappe.call({
                        method: "tools_box.logistics.doctype.vehicle_schedule.vehicle_schedule.make_delivery_tracker",
                        args: {
                            docname: cur_frm.doc.name
                        },
                        callback: function (r) {
                            frappe.model.sync(r.message);
                            frappe.set_route('Form', 'Goods Delivery Tracking', r.message.name);
                        }
                    });
                }
                , __("Make"))
        }
        if ((status && can_create_po) || frm.doc.status == "Awaiting Purchase Order") {
            cur_frm.add_custom_button(
                __("Make Purchase Order"), function () {
                    // do some kind of mapping and create a new purchase order
                    frappe.call({
                        method: "tools_box.logistics.doctype.vehicle_schedule.vehicle_schedule.make_purchase_order",
                        args: {
                            docname: cur_frm.doc.name
                        },
                        callback: function (r) {
                            frappe.model.sync(r.message);
                            frappe.set_route('Form', 'Purchase Order', r.message.name);
                        }
                    });
                }
                , __("Make"))
        }
        if (status) {
            cur_frm.add_custom_button(
                __("Make Employee Advance"), function () {
                    frappe.call({
                        method: "tools_box.logistics.doctype.vehicle_schedule.vehicle_schedule.make_employee_advance",
                        args: {
                            docname: cur_frm.doc.name
                        },
                        callback: function (r) {
                            frappe.model.sync(r.message);
                            frappe.set_route('Form', 'Employee Advance', r.message.name);
                        }
                    });
                }
                , __("Make"))
        }


        // Allow it to be editable if there's no value
        if (cur_frm.daily_cost < 1) {
            cur_frm.set_df_property('daily_cost', 'read_only', 0);
            cur_frm.set_df_property('supplier', 'read_only', 0);
        }
        // get setup ratio levels
        frappe.call({
            method: "tools_box.logistics.doctype.vehicle_schedule.vehicle_schedule.get_allowed",
            callback: function (ret) {
                if (ret.message != undefined) {
                    allowed = ret.message
                }
            }
        })

    },
    vehicle: function (frm) {
        // get the daily cost information from
        if (frm.doc.vehicle == "")
            return;

        get_daily_cost();
    },
    type: function (frm) {
        if (cur_frm.doc.__islocal && cur_frm.doc.type == "Operations") {
            // first calc total
            cur_frm.doc.ratio_ok = 1;
            cur_frm.doc.total_amount = 0;
        } else {
            cur_frm.doc.ratio_ok = 0;
        }

        // fetchs daily cost for type
        get_daily_cost();
    }
});

var item_opts = {
    vehicle_schedule_outbound_item_add: calc_total,
    vehicle_schedule_outbound_item_remove: calc_total,
    vehicle_schedule_inbound_item_remove: calc_total,
    vehicle_schedule_inbound_item_add: calc_total,
    ref_name: function (frm, dtype, dname) {
        var dt = frappe.model.get_value(dtype, dname, "ref_type");
        var dn = frappe.model.get_value(dtype, dname, "ref_name");
        validate(dn, dname);
        frappe.call({
            method: "tools_box.logistics.doctype.vehicle_schedule.vehicle_schedule.get_party_and_amount",
            args: {
                doctype: dt,
                docname: dn
            },
            callback: function get_total(ret) {
                frappe.model.set_value(dtype, dname, "party", ret == {} ? 0 : ret.message.party)
                frappe.model.set_value(dtype, dname, "amount", ret == {} ? 0 : ret.message.amount)
                calc_total(frm);
            }
        })


    },
    amount: calc_total

}
// calculate the total of the items  and
function calc_total(frm) {
    let total_amount  = 0;
    let t = 0;

    if (frm.doc.type != "Operations") {
        var items = cur_frm.doc.vehicle_schedule_outbound_item
        if (cur_frm.doc.type == "Inbound")
            items = cur_frm.doc.vehicle_schedule_inbound_item;

        items.forEach(function (_) {
            total_amount += _.amount || 0;
        });

        if (total_amount !== 0) {
            if (cur_frm.doc.type == "Inbound") {
                t = (allowed.inbound / 100 ) * total_amount;
            }
            else {
                t = (allowed.outbound / 100 ) * total_amount;
            }
            // what percentage of total is total cost
            var ratio = (cur_frm.doc.daily_cost / total_amount) * 100;

            // if daily cost is greater than allowed_outbound percentage of the total amount flag it
            var flag = "";
            var remark = "Vehicle's daily cost is " + roundNumber(ratio, 2) + "% of total amount";
            if (cur_frm.doc.daily_cost > t) {
                cur_frm.doc.ratio_ok = 0;
                flag = "Vehicle's daily cost is more than " + allowed[String(cur_frm.doc.type).toLowerCase()] + "% of " + format_currency(total_amount)
            } else {
                cur_frm.doc.ratio_ok = 1;
                flag = "Vehicle's daily cost is " + roundNumber(ratio, 2) + "% of " + format_currency(total_amount)
            }

            frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "total_amount", total_amount)
            frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "remark", remark)
            frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "reason", flag)
        }
    }
}

function validate(ref_name, parent) {
    // Inbound
    var r = frappe.model.get_list("Vehicle Schedule Inbound Item", {ref_name: ref_name});
    if (r.length > 0 && r[0].name != parent) {
        //frappe.model.set_value("Vehicle Schedule Inbound Item",parent,"ref_name", "");
        frappe.throw("Sorry, Reference name " + ref_name + " already in use");
    }

    // Outbound
    r = frappe.model.get_list("Vehicle Schedule Outbound Item", {ref_name: ref_name});
    if (r.length > 0 && r[0].name != parent) {
        //frappe.model.set_value("Vehicle Schedule Outbound Item",parent,"ref_name", "");
        frappe.throw("Sorry, Reference name " + ref_name + " already in use");
    }
}

function get_daily_cost() {
    frappe.call({
        method: "tools_box.logistics.doctype.vehicle_schedule.vehicle_schedule.get_daily_cost_supplier",
        args: {
            vehicle: cur_frm.doc.vehicle
        },
        callback: function get_daily_cost(ret) {
            if (ret.message == undefined) {
                // Reset value for vehicle and throw exception
                // frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "vehicle", "");
                // frappe.throw("Sorry, Vehicle daily cost is not setup for the vehicle.");
                frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "daily_cost", 0);
                cur_frm.set_df_property('daily_cost', 'read_only', 0);
                cur_frm.set_df_property('supplier', 'read_only', 0);
            } else {
                var d = ret.message[0];
                if (cur_frm.doc.type != "Outbound"){
                    frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "daily_cost", d.outbound_daily_cost);
                }
                else{
                    frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "daily_cost", d.inbound_daily_cost);
                }

                frappe.model.set_value(cur_frm.doctype, cur_frm.docname, "supplier", d.supplier);

                // close value up
                cur_frm.set_df_property('daily_cost', 'read_only', 1);
                cur_frm.set_df_property('supplier', 'read_only', 1);

            }
        }
    })
}


frappe.ui.form.on('Vehicle Schedule Outbound Item', item_opts);
frappe.ui.form.on('Vehicle Schedule Inbound Item', item_opts);
