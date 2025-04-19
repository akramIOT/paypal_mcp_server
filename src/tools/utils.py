"""
Utility functions for tools.

This module provides utility functions used by the tools.
"""

import logging
from typing import Any, Dict
from urllib.parse import urlencode

import requests

logger = logging.getLogger(__name__)

def to_query_string(params: Dict[str, Any]) -> str:
    """
    Convert a dictionary of parameters to a URL query string.
    
    Args:
        params: The parameters to convert
        
    Returns:
        The URL query string
    """
    # Filter out None values
    filtered_params = {k: v for k, v in params.items() if v is not None}
    
    # Convert booleans to lowercase strings
    for key, value in filtered_params.items():
        if isinstance(value, bool):
            filtered_params[key] = str(value).lower()
    
    return urlencode(filtered_params)


def handle_api_error(error: requests.exceptions.RequestException) -> Dict[str, Any]:
    """
    Handle an API error and return an appropriate error response.
    
    Args:
        error: The request exception
        
    Returns:
        The error response
    """
    logger.error(f"API error: {error}")
    
    if hasattr(error, "response") and error.response is not None:
        status_code = error.response.status_code
        
        try:
            error_data = error.response.json()
            error_message = error_data.get("message", "Unknown error")
            
            # Check for detailed error information
            if "details" in error_data and isinstance(error_data["details"], list):
                detail_descriptions = [
                    detail.get("description", "")
                    for detail in error_data["details"]
                    if detail.get("description")
                ]
                
                if detail_descriptions:
                    error_message += ": " + "; ".join(detail_descriptions)
            
            return {
                "error": {
                    "type": "paypal_api_error",
                    "code": status_code,
                    "message": error_message,
                    "details": error_data
                }
            }
        except (ValueError, AttributeError):
            # Failed to parse response as JSON
            return {
                "error": {
                    "type": "paypal_api_error",
                    "code": status_code,
                    "message": f"API error: {error.response.text}"
                }
            }
    else:
        # Connection error
        return {
            "error": {
                "type": "connection_error",
                "message": f"Connection error: {error}"
            }
        }
