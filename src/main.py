#!/usr/bin/env python3
"""
PayPal MCP Server - Main entry point

This script provides a command-line interface to start the PayPal MCP Server
which implements the Model Context Protocol for PayPal API integrations.
"""

import argparse
import logging
import os
import sys
from typing import Dict, List, Optional

from .mcp.server import PayPalMcpServer
from .mcp.transport import StdioTransport

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger("paypal-mcp")

# List of accepted tools
ACCEPTED_TOOLS = [
    "invoices.create",
    "invoices.list",
    "invoices.get",
    "invoices.send",
    "invoices.sendReminder",
    "invoices.cancel",
    "invoices.generateQRC",
    "orders.create",
    "orders.get",
    "orders.capture",
    "disputes.list",
    "disputes.get",
    "disputes.create",
    "shipment.create",
    "shipment.get",
    "products.create",
    "products.list",
    "products.update",
    "products.show",
    "subscriptionPlans.create",
    "subscriptionPlans.list",
    "subscriptionPlans.show",
    "subscriptions.create",
    "subscriptions.show",
    "subscriptions.cancel",
    "transactions.list",
]


def parse_args() -> Dict:
    """Parse command line arguments and environment variables."""
    parser = argparse.ArgumentParser(description="PayPal MCP Server")
    parser.add_argument(
        "--tools", 
        type=str, 
        required=True,
        help="Comma-separated list of tools to enable, or 'all' for all tools"
    )
    parser.add_argument(
        "--access-token", 
        type=str, 
        help="PayPal API access token"
    )
    parser.add_argument(
        "--paypal-environment",
        type=str,
        choices=["SANDBOX", "PRODUCTION"],
        help="PayPal environment (SANDBOX or PRODUCTION)",
    )
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable debug logging"
    )

    args = parser.parse_args()
    
    # Set debug logging if requested
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    # Get tools
    tools_arg = args.tools
    tools: List[str] = []
    
    if tools_arg == "all":
        tools = ["all"]
    else:
        tools = [tool.strip() for tool in tools_arg.split(",")]
        
        # Validate tools
        for tool in tools:
            if tool != "all" and tool not in ACCEPTED_TOOLS:
                valid_tools = ", ".join(ACCEPTED_TOOLS)
                raise ValueError(
                    f"Invalid tool: {tool}. Accepted tools are: all, {valid_tools}"
                )
    
    # Get access token from args or environment
    access_token = args.access_token or os.environ.get("PAYPAL_ACCESS_TOKEN")
    if not access_token:
        raise ValueError(
            "PayPal access token not provided. Please provide it via the --access-token argument "
            "or set the PAYPAL_ACCESS_TOKEN environment variable."
        )
    
    # Get environment from args or environment variable, default to SANDBOX
    paypal_env = args.paypal_environment or os.environ.get("PAYPAL_ENVIRONMENT", "SANDBOX")
    is_sandbox = paypal_env.upper() != "PRODUCTION"
    
    return {
        "tools": tools,
        "access_token": access_token,
        "is_sandbox": is_sandbox,
    }


def main():
    """Main entry point for the PayPal MCP server."""
    try:
        # Parse command line arguments and environment variables
        config = parse_args()
        
        # Create configuration for server
        server_config = {
            "actions": {},
            "context": {
                "sandbox": config["is_sandbox"],
                "access_token": config["access_token"],
            }
        }
        
        # Configure enabled tools
        if "all" in config["tools"]:
            # Enable all tools
            for tool_id in ACCEPTED_TOOLS:
                product, action = tool_id.split(".")
                if product not in server_config["actions"]:
                    server_config["actions"][product] = {}
                server_config["actions"][product][action] = True
        else:
            # Enable only specified tools
            for tool_id in config["tools"]:
                product, action = tool_id.split(".")
                if product not in server_config["actions"]:
                    server_config["actions"][product] = {}
                server_config["actions"][product][action] = True
        
        # Create and start the server
        server = PayPalMcpServer(
            access_token=config["access_token"],
            configuration=server_config,
        )
        
        # Set up stdio transport
        transport = StdioTransport()
        
        # Connect server to transport and start
        logger.info("Starting PayPal MCP Server...")
        logger.info(f"Mode: {'Sandbox' if config['is_sandbox'] else 'Production'}")
        server.connect(transport)
        
        # Log server running
        logger.info("PayPal MCP Server running on stdio")
        
        # Keep the server running
        try:
            # This will block until the transport is closed
            transport.wait_until_closed()
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received, shutting down...")
        
    except Exception as e:
        logger.error(f"Error initializing PayPal MCP server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
