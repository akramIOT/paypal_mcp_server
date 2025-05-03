# Un-Official PayPal MCP Server


![PayPal MCP Server](https://github.com/user-attachments/assets/066c1b04-4dfc-41e7-a145-f1764a106dd4)


A Python implementation of a Model Context Protocol (MCP) server for PayPal API integrations. This server enables Large Language Models (LLMs) to interact with PayPal's APIs through function calling.

## Features

- Full implementation of the Model Context Protocol for PayPal APIs
- Support for all major PayPal API endpoints:
  - **Invoices**: Create, list, view, send, remind, cancel, QR codes
  - **Orders**: Create, get, capture
  - **Products**: Create, list, view, update
  - **Subscription Plans**: Create, list, view
  - **Subscriptions**: Create, view, cancel
  - **Shipments**: Create, track
  - **Disputes**: List, view, accept
  - **Transactions**: List and filter

## Installation

### From PyPI

```bash
pip install paypal-mcp-server
```

### From Source

```bash
git clone https://github.com/yourusername/paypal-mcp-server.git
cd paypal-mcp-server
pip install -e .
```

### Using Docker

```bash
docker pull ghcr.io/yourusername/paypal-mcp-server:latest
```

## Usage

### Command Line

```bash
# Using environment variables
export PAYPAL_ACCESS_TOKEN="your_access_token"
export PAYPAL_ENVIRONMENT="SANDBOX"  # or "PRODUCTION"
paypal-mcp --tools=all

# Or with command line arguments
paypal-mcp --tools=all --access-token=your_access_token --paypal-environment=SANDBOX
```

### Enable Specific Tools Only

```bash
paypal-mcp --tools=invoices.create,invoices.list,orders.create --access-token=your_token
```

### With Docker

```bash
docker run -e PAYPAL_ACCESS_TOKEN="your_access_token" -e PAYPAL_ENVIRONMENT="SANDBOX" ghcr.io/yourusername/paypal-mcp-server:latest --tools=all
```

## Integration with Claude Desktop

Add the following to your `~/Claude/claude_desktop_config.json`:

```json
{
   "mcpServers": {
     "paypal": {
       "command": "paypal-mcp",
       "args": [
         "--tools=all"
       ],
       "env": {
         "PAYPAL_ACCESS_TOKEN": "YOUR_PAYPAL_ACCESS_TOKEN",
         "PAYPAL_ENVIRONMENT": "SANDBOX"
       }
     }
   }
}
```

## Obtaining a PayPal Access Token

You can generate a PayPal access token using your client ID and client secret:

```bash
curl -v https://api-m.sandbox.paypal.com/v1/oauth2/token \
  -H "Accept: application/json" \
  -H "Accept-Language: en_US" \
  -u "CLIENT_ID:CLIENT_SECRET" \
  -d "grant_type=client_credentials"
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/paypal-mcp-server.git
cd paypal-mcp-server

# Install dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
pytest -xvs
```

### Building the Package

```bash
python -m build
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on PayPal's [Agent Toolkit](https://github.com/paypal/agent-toolkit)
- Compatible with the [Model Context Protocol](https://modelcontextprotocol.com/) specification
