"""
Tool definitions for the PayPal MCP server.

This module provides definitions for all the tools that can be used with the
PayPal MCP server.
"""

from typing import Any, Dict, List

from .parameters import (
    AcceptDisputeClaimParameters, CancelSentInvoiceParameters, 
    CancelSubscriptionParameters, CaptureOrderParameters, CreateInvoiceParameters,
    CreateOrderParameters, CreateProductParameters, CreateShipmentParameters,
    CreateSubscriptionParameters, CreateSubscriptionPlanParameters,
    GenerateInvoiceQrCodeParameters, GetDisputeParameters, GetInvoiceParameters,
    GetOrderParameters, GetShipmentTrackingParameters, ListDisputesParameters,
    ListInvoicesParameters, ListProductsParameters, ListSubscriptionPlansParameters,
    ListTransactionsParameters, SendInvoiceParameters, SendInvoiceReminderParameters,
    ShowProductDetailsParameters, ShowSubscriptionDetailsParameters,
    ShowSubscriptionPlanDetailsParameters, UpdateProductParameters
)
from .prompts import (
    accept_dispute_claim_prompt, cancel_sent_invoice_prompt, 
    cancel_subscription_prompt, capture_order_prompt, create_invoice_prompt,
    create_order_prompt, create_product_prompt, create_shipment_prompt,
    create_subscription_prompt, create_subscription_plan_prompt,
    generate_invoice_qr_code_prompt, get_dispute_prompt, get_invoice_prompt,
    get_order_prompt, get_shipment_tracking_prompt, list_disputes_prompt,
    list_invoices_prompt, list_products_prompt, list_subscription_plans_prompt,
    list_transactions_prompt, send_invoice_prompt, send_invoice_reminder_prompt,
    show_product_details_prompt, show_subscription_details_prompt,
    show_subscription_plan_details_prompt, update_product_prompt
)


class Tool:
    """Represents a tool that can be used with the MCP server."""
    
    def __init__(
        self,
        method: str,
        name: str,
        description: str,
        parameters: Any,
        actions: Dict[str, Dict[str, bool]]
    ):
        """
        Initialize a tool.
        
        Args:
            method: The method name for the tool
            name: The display name of the tool
            description: The description of the tool
            parameters: The parameters model (Pydantic model)
            actions: The actions that the tool supports
        """
        self.method = method
        self.name = name
        self.description = description
        self.parameters = parameters
        self.actions = actions


def get_tools(context: Dict[str, Any] = None) -> List[Tool]:
    """
    Get all available tools.
    
    Args:
        context: The context for the tools
        
    Returns:
        The list of available tools
    """
    context = context or {}
    
    return [
        # Invoice tools
        Tool(
            method="create_invoice",
            name="Create Invoice",
            description=create_invoice_prompt(context),
            parameters=CreateInvoiceParameters,
            actions={"invoices": {"create": True}}
        ),
        Tool(
            method="list_invoices",
            name="List Invoices",
            description=list_invoices_prompt(context),
            parameters=ListInvoicesParameters,
            actions={"invoices": {"list": True}}
        ),
        Tool(
            method="get_invoice",
            name="Get Invoice",
            description=get_invoice_prompt(context),
            parameters=GetInvoiceParameters,
            actions={"invoices": {"get": True}}
        ),
        Tool(
            method="send_invoice",
            name="Send Invoice",
            description=send_invoice_prompt(context),
            parameters=SendInvoiceParameters,
            actions={"invoices": {"send": True}}
        ),
        Tool(
            method="send_invoice_reminder",
            name="Send Invoice Reminder",
            description=send_invoice_reminder_prompt(context),
            parameters=SendInvoiceReminderParameters,
            actions={"invoices": {"sendReminder": True}}
        ),
        Tool(
            method="cancel_sent_invoice",
            name="Cancel Sent Invoice",
            description=cancel_sent_invoice_prompt(context),
            parameters=CancelSentInvoiceParameters,
            actions={"invoices": {"cancel": True}}
        ),
        Tool(
            method="generate_invoice_qr_code",
            name="Generate Invoice QR Code",
            description=generate_invoice_qr_code_prompt(context),
            parameters=GenerateInvoiceQrCodeParameters,
            actions={"invoices": {"generateQRC": True}}
        ),
        
        # Product tools
        Tool(
            method="create_product",
            name="Create Product",
            description=create_product_prompt(context),
            parameters=CreateProductParameters,
            actions={"products": {"create": True}}
        ),
        Tool(
            method="list_products",
            name="List Products",
            description=list_products_prompt(context),
            parameters=ListProductsParameters,
            actions={"products": {"list": True}}
        ),
        Tool(
            method="update_product",
            name="Update Product",
            description=update_product_prompt(context),
            parameters=UpdateProductParameters,
            actions={"products": {"update": True}}
        ),
        Tool(
            method="show_product_details",
            name="Show Product Details",
            description=show_product_details_prompt(context),
            parameters=ShowProductDetailsParameters,
            actions={"products": {"show": True}}
        ),
        
        # Subscription plan tools
        Tool(
            method="create_subscription_plan",
            name="Create Subscription Plan",
            description=create_subscription_plan_prompt(context),
            parameters=CreateSubscriptionPlanParameters,
            actions={"subscriptionPlans": {"create": True}}
        ),
        Tool(
            method="list_subscription_plans",
            name="List Subscription Plans",
            description=list_subscription_plans_prompt(context),
            parameters=ListSubscriptionPlansParameters,
            actions={"subscriptionPlans": {"list": True}}
        ),
        Tool(
            method="show_subscription_plan_details",
            name="Show Subscription Plan Details",
            description=show_subscription_plan_details_prompt(context),
            parameters=ShowSubscriptionPlanDetailsParameters,
            actions={"subscriptionPlans": {"show": True}}
        ),
        
        # Subscription tools
        Tool(
            method="create_subscription",
            name="Create Subscription",
            description=create_subscription_prompt(context),
            parameters=CreateSubscriptionParameters,
            actions={"subscriptions": {"create": True}}
        ),
        Tool(
            method="show_subscription_details",
            name="Show Subscription Details",
            description=show_subscription_details_prompt(context),
            parameters=ShowSubscriptionDetailsParameters,
            actions={"subscriptions": {"show": True}}
        ),
        Tool(
            method="cancel_subscription",
            name="Cancel Subscription",
            description=cancel_subscription_prompt(context),
            parameters=CancelSubscriptionParameters,
            actions={"subscriptions": {"cancel": True}}
        ),
        
        # Shipment tools
        Tool(
            method="create_shipment",
            name="Create Shipment",
            description=create_shipment_prompt(context),
            parameters=CreateShipmentParameters,
            actions={"shipment": {"create": True}}
        ),
        Tool(
            method="get_shipment_tracking",
            name="Get Shipment Tracking",
            description=get_shipment_tracking_prompt(context),
            parameters=GetShipmentTrackingParameters,
            actions={"shipment": {"get": True}}
        ),
        
        # Order tools
        Tool(
            method="create_order",
            name="Create Order",
            description=create_order_prompt(context),
            parameters=CreateOrderParameters,
            actions={"orders": {"create": True}}
        ),
        Tool(
            method="get_order",
            name="Get Order",
            description=get_order_prompt(context),
            parameters=GetOrderParameters,
            actions={"orders": {"get": True}}
        ),
        Tool(
            method="capture_order",
            name="Capture Order",
            description=capture_order_prompt(context),
            parameters=CaptureOrderParameters,
            actions={"orders": {"capture": True}}
        ),
        
        # Dispute tools
        Tool(
            method="list_disputes",
            name="List Disputes",
            description=list_disputes_prompt(context),
            parameters=ListDisputesParameters,
            actions={"disputes": {"list": True}}
        ),
        Tool(
            method="get_dispute",
            name="Get Dispute",
            description=get_dispute_prompt(context),
            parameters=GetDisputeParameters,
            actions={"disputes": {"get": True}}
        ),
        Tool(
            method="accept_dispute_claim",
            name="Accept Dispute Claim",
            description=accept_dispute_claim_prompt(context),
            parameters=AcceptDisputeClaimParameters,
            actions={"disputes": {"create": True}}
        ),
        
        # Transaction tools
        Tool(
            method="list_transactions",
            name="List Transactions",
            description=list_transactions_prompt(context),
            parameters=ListTransactionsParameters,
            actions={"transactions": {"list": True}}
        ),
    ]


# Get all actions from the tools
def get_all_actions() -> Dict[str, Dict[str, bool]]:
    """
    Get all actions from the tools.
    
    Returns:
        A dictionary of all actions
    """
    all_actions = {}
    
    for tool in get_tools():
        for product, product_actions in tool.actions.items():
            if product not in all_actions:
                all_actions[product] = {}
            
            for action, enabled in product_actions.items():
                all_actions[product][action] = enabled
    
    return all_actions


# All tools enabled configuration
ALL_TOOLS_ENABLED = get_all_actions()
