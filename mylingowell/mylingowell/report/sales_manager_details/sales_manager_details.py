# Copyright (c) 2023, rakesh and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {
            "label": _("User Name"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "User",
            "width": 200,
        },
        {
            "label": _("First Name"),
            "fieldname": "first_name",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": _("Last Name"),
            "fieldname": "last_name",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": _("Role"),
            "fieldname": "role_profile_name",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": _("Gender"),
            "fieldname": "gender",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("Birth Date"),
            "fieldname": "birth_date",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("Phone"),
            "fieldname": "phone",
            "fieldtype": "Data",
            "width": 100,
        },
    ]
    data = get_data()
    return columns, data


def get_data():
    data = frappe.get_all(
        "User",
        filters={"role_profile_name": "Sales Manager"},
        fields=[
            "name",
            "first_name",
            "last_name",
            "role_profile_name",
            "gender",
            "birth_date",
            "phone",
        ],
    )
    return data
