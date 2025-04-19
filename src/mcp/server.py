"""
MCP Server implementation for PayPal API.

This module provides the PayPalMcpServer class which implements the
Model Context Protocol server for PayPal API integrations.
"""

import json
import logging
import uuid
from typing import Any, Dict, List, Optional, Type, cast

from pydantic import BaseModel, ValidationError

from ..api.client import PayPalClient
from ..tools.definitions import get_tools, Tool

logger = logging.getLogger(__name__)

class McpServer:
    """Base MCP server implementation."""
    
    def __init__(self, name: str, version: str):
        """
        Initialize the MCP server.
        
        Args:
            name: The name of the server
            version: The version of the server
        """
        self.name = name
        self.version = version
        self._transport = None
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._handlers: Dict[str, Any] = {}
        self._validator_models: Dict[str, Type[BaseModel]] = {}
    
    def tool(
        self,
        method: str,
        description: str,
        schema: Dict[str, Any],
        handler: callable,
        validator_model: Optional[Type[BaseModel]] = None,
    ):
        """
        Register a tool with the server.
        
        Args:
            method: The method name for the tool
            description: The description of the tool
            schema: The JSON schema for the tool parameters
            handler: The handler function for the tool
            validator_model: Optional Pydantic model for parameter validation
        """
        self._tools[method] = {
            "description": description,
            "parameters": schema,
        }
        self._handlers[method] = handler
        
        if validator_model:
            self._validator_models[method] = validator_model
    
    def connect(self, transport):
        """
        Connect to a transport.
        
        Args:
            transport: The transport to connect to
        """
        self._transport = transport
        transport.onmessage = self._handle_message
        transport.start()
    
    def _handle_message(self, message: Dict[str, Any]):
        """
        Handle an incoming message from the transport.
        
        Args:
            message: The message to handle
        """
        logger.debug(f"Received message: {message}")
        
        if message.get("type") == "ping":
            # Respond to ping
            self._respond_to_ping(message)
        elif message.get("type") == "request":
            # Handle a request
            self._handle_request(message)
    
    def _respond_to_ping(self, message: Dict[str, Any]):
        """
        Respond to a ping message.
        
        Args:
            message: The ping message
        """
        logger.debug("Responding to ping")
        
        response = {
            "id": message.get("id"),
            "type": "response",
            "status": "success",
            "result": {
                "id": message.get("id"),
                "name": self.name,
                "version": self.version,
                "capabilities": list(self._tools.keys()),
            },
        }
        
        self._transport.send(response)
    
    def _handle_request(self, message: Dict[str, Any]):
        """
        Handle a request message.
        
        Args:
            message: The request message
        """
        request_id = message.get("id")
        method = message.get("method")
        params = message.get("params", {})
        
        logger.debug(f"Handling request {request_id}: {method}")
        
        if method not in self._tools:
            # Method not found
            self._send_error(
                request_id,
                -32601,
                "Method not found",
                f"Method '{method}' not found",
            )
            return
        
        # Validate parameters if we have a validator model
        if method in self._validator_models:
            try:
                # Parse and validate parameters using Pydantic
                validator_model = self._validator_models[method]
                validated_params = validator_model(**params)
                # Convert validated params back to dict
                params = validated_params.model_dump()
            except ValidationError as e:
                # Parameter validation failed
                self._send_error(
                    request_id,
                    -32602,
                    "Invalid params",
                    str(e),
                )
                return
        
        # Call the handler
        try:
            handler = self._handlers[method]
            result = handler(params)
            
            # Send successful response
            response = {
                "id": request_id,
                "type": "response",
                "status": "success",
                "result": result,
            }
            self._transport.send(response)
        except Exception as e:
            # Handler raised an exception
            logger.exception(f"Error handling request: {e}")
            self._send_error(
                request_id,
                -32603,
                "Internal error",
                str(e),
            )
    
    def _send_error(self, request_id: str, code: int, message: str, data: Any = None):
        """
        Send an error response.
        
        Args:
            request_id: The request ID
            code: The error code
            message: The error message
            data: Additional error data
        """
        response = {
            "id": request_id,
            "type": "response",
            "status": "error",
            "error": {
                "code": code,
                "message": message,
            },
        }
        
        if data is not None:
            response["error"]["data"] = data
        
        self._transport.send(response)


class PayPalMcpServer(McpServer):
    """PayPal MCP server implementation."""
    
    def __init__(self, access_token: str, configuration: Dict[str, Any]):
        """
        Initialize the PayPal MCP server.
        
        Args:
            access_token: The PayPal API access token
            configuration: The server configuration
        """
        super().__init__("PayPal", "0.4.0")
        
        # Create PayPal client
        self.client = PayPalClient(access_token, configuration.get("context", {}))
        
        # Register tools based on configuration
        self._register_tools(configuration)
    
    def _register_tools(self, configuration: Dict[str, Any]):
        """
        Register tools based on configuration.
        
        Args:
            configuration: The server configuration
        """
        # Get all available tools
        all_tools = get_tools(configuration.get("context", {}))
        
        # Filter tools based on configuration
        for tool in all_tools:
            if self._is_tool_allowed(tool, configuration):
                # Register the tool
                logger.debug(f"Registering tool: {tool.method}")
                
                self.tool(
                    tool.method,
                    tool.description,
                    tool.parameters.schema(),
                    self._create_handler(tool),
                    validator_model=tool.parameters,
                )
    
    def _is_tool_allowed(self, tool: Tool, configuration: Dict[str, Any]) -> bool:
        """
        Check if a tool is allowed based on configuration.
        
        Args:
            tool: The tool to check
            configuration: The server configuration
            
        Returns:
            True if the tool is allowed, False otherwise
        """
        actions = configuration.get("actions", {})
        
        for product, product_actions in tool.actions.items():
            for action, enabled in product_actions.items():
                if (
                    product in actions
                    and action in actions[product]
                    and actions[product][action]
                ):
                    return True
        
        return False
    
    def _create_handler(self, tool: Tool):
        """
        Create a handler function for a tool.
        
        Args:
            tool: The tool to create a handler for
            
        Returns:
            The handler function
        """
        def handler(params):
            """Handler function for the tool."""
            logger.debug(f"Handling {tool.method} with params: {params}")
            
            # Call the PayPal API
            result = self.client.run(tool.method, params)
            
            # Convert to MCP result format
            return {
                "content": [
                    {
                        "type": "text",
                        "text": result,
                    }
                ]
            }
        
        return handler
