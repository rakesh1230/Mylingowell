import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    return columns, data, chart


def get_columns():
    return [
        {
            "fieldname": "customer_name",
            "label": "ID",
            "fieldtype": "Data",
            "width": 120,
        },
    ]


def get_chart(data):
    customer_names = [d.customer_name for d in data]
    unique_names = list(set(customer_names))
    print(unique_names)
    counts = [customer_names.count(name) for name in unique_names]

    return {
        "data": {
            "labels": unique_names,
            "datasets": [
                {"name": _("Customer Name"), "values": counts},
            ],
        },
        "type": "pie",
        "colors": ["#fc4f51", "#78d6ff", "#7575ff"],
    }


def get_data(filters=None):
    frappe_filter = filters or {}
    territory = frappe_filter.get("territory")
    if territory:
        data = frappe.get_all(
            "Customer",
            filters={"territory": territory},
            fields=["customer_name"],
            order_by="territory",
        )
    else:
        data = frappe.get_all(
            "Customer",
            fields=["customer_name"],
            order_by="territory",
        )
    return data
