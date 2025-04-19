FROM python:3.10-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONPATH=/app

# Install dependencies
COPY pyproject.toml .
COPY README.md .
COPY src ./src

# Install the package
RUN pip install --no-cache-dir -e .

# Set the default command to run the server
ENTRYPOINT ["paypal-mcp"]
CMD ["--tools=all"]

# Expose any necessary ports (MCP uses stdio by default)
# If you need to expose HTTP or other ports, uncomment and modify:
# EXPOSE 8000

# Label the image
LABEL maintainer="MCP Server Team <mcpserver@example.com>" \
      version="0.1.0" \
      description="PayPal MCP Server for LLM function calling integration"
