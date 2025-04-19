"""
PayPal API function implementations.

This module provides implementations for all the PayPal API functions
that can be used with the MCP server.
"""

import logging
from typing import Any, Dict
from datetime import datetime, timedelta

import requests

from ..tools.utils import handle_api_error, to_query_string

logger = logging.getLogger(__name__)

# === INVOICE FUNCTIONS ===

async def create_invoice(client, context: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new invoice in the PayPal system.
    
    Args:
        client: The PayPal client
        context: The context for the request
        params: The parameters for the request
        
    Returns:
        The created invoice data
    """
    logger.info("Starting invoice creation process")
    logger.debug(f"Invoice details: {params}")
    
    headers = await client.get_headers()
    url = f"{client.get_base_url()}/v2/invoicing/invoices"
    
    try:
        response = requests.post(url, json=params, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"Invoice created successfully. Status: {response.status_code}")
        
        # Check if response matches the expected format for a successful invoice creation
        if (
            result.get("rel") == "self"
            and result.get("href")
            and "/v2/invoicing/invoices/" in result.get("href", "")
            and result.get("method") == "GET"
        ):
            # Extract invoice ID from the href URL
            href_parts = result["href"].split("/")
            invoice_id = href_parts[-1]
            logger.info(f"Invoice ID extracted from href: {invoice_id}")
            
            # Automatically send the invoice with specific parameters
            try:
                send_params = {
                    "invoice_id": invoice_id,
                    "note": "Thank you for choosing us. If there are any issues, feel free to contact us",
                    "send_to_recipient": True
                }
                
                send_result = await send_invoice(client, context, send_params)
                logger.info(f"Auto-send invoice result: {send_result}")
                
                # Return both the create and send results
                return {
                    "createResult": result,
                    "sendResult": send_result
                }
            except Exception as e:
                logger.error(f"Error in auto-send invoice: {str(e)}")
                # Still return the original creation result even if sending fails
                return result
        else:
            return result
    except requests.exceptions.RequestException as e:
        return handle_api_error(e)


async def list_invoices(client, context: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    List invoices with optional pagination and filtering.
    
    Args:
        client: The PayPal client
        context: The context for the request
        params: The parameters for the request
        
    Returns:
        The invoice list data
    """
    logger.info("Starting to list invoices")
    logger.debug(f"Query parameters: {params}")
    
    headers = await client.get_headers()
    url = f"{client.get_base_url()}/v2/invoicing/invoices"
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"Invoices retrieved successfully. Status: {response.status_code}")
        
        if "total_items" in result:
            logger.info(f"Total items: {result['total_items']}")
        
        if "items" in result and isinstance(result["items"], list):
            logger.info(f"Retrieved {len(result['items'])} invoices")
        
        return result
    except requests.exceptions.RequestException as e:
        return handle_api_error(e)


async def get_invoice(client, context: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieve details of a specific invoice.
    
    Args:
        client: The PayPal client
        context: The context for the request
        params: The parameters for the request
        
    Returns:
        The invoice data
    """
    logger.info("Starting to get invoice")
    logger.debug(f"Query parameters: {params}")
    
    invoice_id = params["invoice_id"]
    headers = await client.get_headers()
    url = f"{client.get_base_url()}/v2/invoicing/invoices/{invoice_id}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"Invoice retrieved successfully. Status: {response.status_code}")
        return result
    except requests.exceptions.RequestException as e:
        return handle_api_error(e)


async def send_invoice(client, context: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send an invoice to recipients.
    
    Args:
        client: The PayPal client
        context: The context for the request
        params: The parameters for the request
        
    Returns:
        The result of the send operation
    """
    logger.info("Starting to send invoice")
    
    invoice_id = params["invoice_id"]
    logger.info(f"Invoice ID: {invoice_id}")
    
    if params.get("note"):
        logger.info(f"Note: {params['note']}")
    
    logger.info(f"Send to recipient: {params.get('send_to_recipient', False)}")
    
    if params.get("additional_recipients"):
        recipients = params["additional_recipients"]
        logger.info(f"Additional recipients: {', '.join(recipients)}")
    
    headers = await client.get_headers()
    url = f"{client.get_base_url()}/v2/invoicing/invoices/{invoice_id}/send"
    
    try:
        response = requests.post(url, json=params, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"Invoice sent successfully. Status: {response.status_code}")
        return result
    except requests.exceptions.RequestException as e:
        return handle_api_error(e)
