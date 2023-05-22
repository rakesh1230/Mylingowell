import frappe
from frappe.auth import LoginManager
from frappe.utils import cstr


@frappe.whitelist()
def generate_key(user):
    user_details = frappe.get_doc("User", user)
    api_secret = api_key = ""
    if not user_details.api_key and not user_details.api_secret:
        api_secret = frappe.generate_hash(length=15)
        # if api key is not set generate api key
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key
        user_details.api_secret = api_secret
        user_details.save(ignore_permissions=True)
    else:
        api_secret = user_details.get_password("api_secret")
        api_key = user_details.get("api_key")
    return {"api_secret": api_secret, "api_key": api_key}


@frappe.whitelist(allow_guest=True)
def login(usr, pwd):
    try:
        login_manager = LoginManager()
        login_manager.authenticate(usr, pwd)
        login_manager.post_login()
        if frappe.response["message"] == "Logged In":
            frappe.response["user"] = login_manager.user
            frappe.response["key_details"] = generate_key(login_manager.user)
        frappe.response["message"]
    except frappe.AuthenticationError:
        (500, frappe.response["message"])
    except Exception as e:
        frappe.log_error(frappe.get_traceback())
        (500, cstr(e))


@frappe.whitelist()
def get_customer_and_sales_orders(financial_year=None):
    try:
        customer_list = frappe.get_all("Customer", ["name", "customer_name"])
        for customer in customer_list:
            filters = [
                ["Dynamic Link", "link_doctype", "=", "Customer"],
                ["Dynamic Link", "link_title", "=", customer.get("customer_name")],
            ]
            contact = frappe.get_all("Contact", filters=filters, fields=["phone"])
            customer["primary_contact_number"] = contact
            state = frappe.db.get_all(
                "Address", filters=filters, fields=["state as customer_state"]
            )
            customer["state"] = state

            if financial_year:
                sales_orders = frappe.get_all(
                    "Sales Order",
                    filters={
                        "customer": customer.get("name"),
                        "transaction_date": (">=", financial_year + "-04-01"),
                        "transaction_date": (
                            "<=",
                            str(int(financial_year) + 1) + "-03-31",
                        ),
                        "status": [
                            "in",
                            ["To Deliver", "To Deliver and Bill", "To Bill"],
                        ],
                    },
                    fields=["name", "grand_total"],
                )
                total_value = sum([order.get("grand_total") for order in sales_orders])
                customer["pending_sales_orders"] = len(sales_orders)
                customer["total_value"] = total_value
            else:
                customer["sales_orders"] = 0
                customer["total_value"] = 0

            unpaid_amount = frappe.get_all(
                "Sales Invoice",
                filters={"customer": customer.get("name"), "status": "Unpaid"},
                fields=["grand_total"],
            )
            amount = sum([invoice.get("grand_total") for invoice in unpaid_amount])
            customer["unpaid_amount"] = amount
        return customer_list
    except Exception as e:
        print(str(e))
