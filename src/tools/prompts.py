"""
Prompt templates for the PayPal MCP server tools.

This module provides prompt templates for all the tools used by the
PayPal MCP server.
"""

from typing import Dict, Any

def create_invoice_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for creating an invoice."""
    return """
    Create a new invoice in the PayPal system.
    
    This tool allows you to create a new invoice with details such as items,
    amounts, recipient information, and more. The invoice can then be sent to
    customers for payment.
    """


def list_invoices_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for listing invoices."""
    return """
    List invoices with optional pagination and filtering.
    
    This tool allows you to retrieve a list of invoices from your PayPal account.
    You can paginate the results and get the total count if needed.
    """


def get_invoice_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for retrieving an invoice."""
    return """
    Retrieve details of a specific invoice.
    
    This tool allows you to get detailed information about a specific invoice
    by providing its ID.
    """


def send_invoice_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for sending an invoice."""
    return """
    Send an invoice to recipients.
    
    This tool allows you to send an existing invoice to its recipients. You can
    include a note and specify additional recipients if needed.
    """


def send_invoice_reminder_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for sending an invoice reminder."""
    return """
    Send a reminder for an existing invoice.
    
    This tool allows you to send a reminder for an invoice that has already been
    sent but not yet paid. You can include a subject, note, and additional recipients.
    """


def cancel_sent_invoice_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for canceling a sent invoice."""
    return """
    Cancel a sent invoice.
    
    This tool allows you to cancel an invoice that has already been sent. You can
    include a note explaining the cancellation and specify whether to notify the
    recipient.
    """


def generate_invoice_qr_code_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for generating an invoice QR code."""
    return """
    Generate a QR code for an invoice.
    
    This tool generates a QR code that customers can scan to view and pay an invoice.
    You can specify the width and height of the QR code.
    """


def create_product_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for creating a product."""
    return """
    Create a new product in the PayPal catalog.
    
    This tool allows you to create a product that can be used in orders, subscriptions,
    and other PayPal services. You can specify details such as name, type, description,
    and more.
    """


def list_products_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for listing products."""
    return """
    List products with optional pagination and filtering.
    
    This tool allows you to retrieve a list of products from your PayPal catalog.
    You can paginate the results and get the total count if needed.
    """


def show_product_details_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for retrieving product details."""
    return """
    Retrieve details of a specific product.
    
    This tool allows you to get detailed information about a specific product
    by providing its ID.
    """


def update_product_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for updating a product."""
    return """
    Update an existing product.
    
    This tool allows you to update the details of an existing product in your
    PayPal catalog. You can specify the operations to perform on the product.
    """


def create_subscription_plan_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for creating a subscription plan."""
    return """
    Create a new subscription plan.
    
    This tool allows you to create a subscription plan that can be used to create
    subscriptions. You can specify details such as billing cycles, pricing, and more.
    """


def list_subscription_plans_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for listing subscription plans."""
    return """
    List subscription plans.
    
    This tool allows you to retrieve a list of subscription plans. You can filter
    by product ID and paginate the results.
    """


def show_subscription_plan_details_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for retrieving subscription plan details."""
    return """
    Retrieve details of a specific subscription plan.
    
    This tool allows you to get detailed information about a specific subscription
    plan by providing its ID.
    """


def create_subscription_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for creating a subscription."""
    return """
    Create a new subscription.
    
    This tool allows you to create a subscription based on a subscription plan.
    You can specify details such as the subscriber, shipping, and application context.
    """


def show_subscription_details_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for retrieving subscription details."""
    return """
    Retrieve details of a specific subscription.
    
    This tool allows you to get detailed information about a specific subscription
    by providing its ID.
    """


def cancel_subscription_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for canceling a subscription."""
    return """
    Cancel an active subscription.
    
    This tool allows you to cancel an active subscription. You can include a reason
    for the cancellation.
    """


def create_shipment_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for creating a shipment."""
    return """
    Create a shipment tracking record.
    
    This tool allows you to create a shipment tracking record for an order.
    You can specify the tracking number, carrier, and status of the shipment.
    """


def get_shipment_tracking_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for retrieving shipment tracking."""
    return """
    Retrieve shipment tracking information.
    
    This tool allows you to get tracking information for a shipment by providing
    either the transaction ID or the order ID.
    """


def create_order_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for creating an order."""
    return """
    Create an order in PayPal system based on provided details.
    
    This tool allows you to create an order with items, amounts, and shipping
    information. The order can then be used to collect payment from a customer.
    """


def get_order_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for retrieving an order."""
    return """
    Retrieve the details of an order.
    
    This tool allows you to get detailed information about a specific order
    by providing its ID.
    """


def capture_order_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for capturing an order."""
    return """
    Capture payment for an authorized order.
    
    This tool allows you to capture payment for an order that has been authorized
    but not yet captured.
    """


def list_disputes_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for listing disputes."""
    return """
    Retrieve a summary of all open disputes.
    
    This tool allows you to get a list of disputes with optional filtering
    and pagination.
    """


def get_dispute_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for retrieving a dispute."""
    return """
    Retrieve detailed information of a specific dispute.
    
    This tool allows you to get detailed information about a specific dispute
    by providing its ID.
    """


def accept_dispute_claim_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for accepting a dispute claim."""
    return """
    Accept a dispute claim.
    
    This tool allows you to accept a claim for a dispute. You can include a note
    explaining why you are accepting the claim.
    """


def list_transactions_prompt(context: Dict[str, Any] = None) -> str:
    """Prompt for listing transactions."""
    return """
    List transactions with optional pagination and filtering.
    
    This tool allows you to retrieve a list of transactions from your PayPal account.
    You can filter by date range, transaction ID, and status.
    """
