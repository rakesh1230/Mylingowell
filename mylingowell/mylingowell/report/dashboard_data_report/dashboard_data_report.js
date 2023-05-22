// Copyright (c) 2023, rakesh and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Dashboard Data report"] = {
	"filters": [
		{
            "fieldname":"territory",
            "label": __("Based_on"),
            "fieldtype": "Link",
            "options":"Territory"
        },
	]
};
