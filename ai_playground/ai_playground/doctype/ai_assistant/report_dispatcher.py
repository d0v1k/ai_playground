import re
from .item_lookup_handler import process_item_lookup

# Define patterns that identify different types of reports:
handler_patterns = {
    "item_lookup": r'\b\d+-\d+\b',  # Example pattern for item code
    "sales_report": r'\bsales report for customer \b',  # Placeholder pattern for sales report
}

def handle_report_request(user_input):
    # Map handlers to their corresponding report types
    handlers = {
        "item_lookup": handle_item_lookup,
        "sales_report": handle_sales_report,
    }

    for handler_key, handler in handlers.items():
        if re.search(handler_patterns[handler_key], user_input):
            return handler(user_input)

    return "Report type not recognized."

def handle_item_lookup(user_input):
    return process_item_lookup(user_input)

def handle_sales_report(user_input):
    # Placeholder function; will implement next
    return "Sales report functionality coming soon."
