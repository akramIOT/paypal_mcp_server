"""
PayPal API client implementation.

This module provides the PayPalClient class which handles communication
with the PayPal API.
"""

import base64
import json
import logging
from typing import Any, Dict, Optional

import requests

from .functions import (
    accept_dispute_claim, cancel_sent_invoice, cancel_subscription, 
    capture_order, create_invoice, create_order, create_product, 
    create_shipment, create_subscription, create_subscription_plan, 
    generate_invoice_qr_code, get_dispute, get_invoice, get_order, 
    get_shipment_tracking, list_disputes, list_invoices, list_products, 
    list_subscription_plans, list_transactions, send_invoice, 
    send_invoice_reminder, show_product_details, show_subscription_details, 
    show_subscription_plan_details, update_product
)

logger = logging.getLogger(__name__)

class PayPalClient:
    """Client for interacting with the PayPal API."""
    
    def __init__(self, access_token: str, context: Dict[str, Any] = None):
        """
        Initialize the PayPal client.
        
        Args:
            access_token: The PayPal API access token
            context: Additional context for the client
        """
        self.access_token = access_token
        self.context = context or {}
        
        # Set default sandbox mode if not provided
        self.context["sandbox"] = self.context.get("sandbox", True)
        
        # Set base URL based on sandbox mode
        self.base_url = (
            "https://api-m.sandbox.paypal.com" 
            if self.context["sandbox"] 
            else "https://api-m.paypal.com"
        )
    
    def get_base_url(self) -> str:
        """Get the base URL for API requests."""
        return self.base_url
    
    async def get_headers(self) -> Dict[str, str]:
        """Get the headers for API requests."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        
        # Add additional headers if needed
        if self.context.get("request_id"):
            headers["PayPal-Request-Id"] = self.context["request_id"]
        
        if self.context.get("tenant_context"):
            headers["PayPal-Tenant-Context"] = json.dumps(self.context["tenant_context"])
        
        return headers
    
    def run(self, method: str, params: Dict[str, Any]) -> str:
        """
        Run a method with the given parameters.
        
        Args:
            method: The method to run
            params: The parameters for the method
            
        Returns:
            The result as a JSON string
        """
        try:
            result = self._execute_method(method, params)
            return json.dumps(result)
        except Exception as e:
            logger.exception(f"Error executing method {method}: {e}")
            return json.dumps({
                "error": {
                    "message": str(e),
                    "type": "paypal_error",
                }
            })
    
    def _execute_method(self, method: str, params: Dict[str, Any]) -> Any:
        """
        Execute a method with the given parameters.
        
        Args:
            method: The method to execute
            params: The parameters for the method
            
        Returns:
            The result object
        """
        # Map method names to functions
        method_map = {
            "create_invoice": create_invoice,
            "list_invoices": list_invoices,
            "get_invoice": get_invoice,
            "send_invoice": send_invoice,
            "send_invoice_reminder": send_invoice_reminder,
            "cancel_sent_invoice": cancel_sent_invoice,
            "generate_invoice_qr_code": generate_invoice_qr_code,
            "create_product": create_product,
            "list_products": list_products,
            "show_product_details": show_product_details,
            "update_product": update_product,
            "create_subscription_plan": create_subscription_plan,
            "list_subscription_plans": list_subscription_plans,
            "show_subscription_plan_details": show_subscription_plan_details,
            "create_subscription": create_subscription,
            "show_subscription_details": show_subscription_details,
            "cancel_subscription": cancel_subscription,
            "create_shipment": create_shipment,
            "get_shipment_tracking": get_shipment_tracking,
            "create_order": create_order,
            "get_order": get_order,
            "capture_order": capture_order,
            "list_disputes": list_disputes,
            "get_dispute": get_dispute,
            "accept_dispute_claim": accept_dispute_claim,
            "list_transactions": list_transactions,
        }
        
        if method not in method_map:
            raise ValueError(f"Invalid method: {method}")
        
        # Call the appropriate function
        return method_map[method](self, self.context, params)
