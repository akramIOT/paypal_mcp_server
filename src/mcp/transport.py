"""
Transport implementation for the Model Context Protocol.

This module provides the StdioTransport class which implements the transport
layer for the MCP protocol over standard input/output.
"""

import json
import logging
import os
import re
import sys
import threading
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)

class StdioTransport:
    """
    Server transport for stdio: this communicates with a MCP client by reading from
    the current process' stdin and writing to stdout.
    """
    
    def __init__(self, stdin=sys.stdin.buffer, stdout=sys.stdout.buffer):
        """
        Initialize the StdioTransport with stdin and stdout.
        
        Args:
            stdin: The input stream (defaults to sys.stdin.buffer)
            stdout: The output stream (defaults to sys.stdout.buffer)
        """
        self._stdin = stdin
        self._stdout = stdout
        self._read_buffer = bytearray()
        self._started = False
        self._read_thread = None
        self._closed = threading.Event()
        
        # Callbacks
        self.onclose: Optional[Callable[[], None]] = None
        self.onerror: Optional[Callable[[Exception], None]] = None
        self.onmessage: Optional[Callable[[Dict[str, Any]], None]] = None
    
    def start(self):
        """Start listening for messages on stdin."""
        if self._started:
            return
        
        self._started = True
        self._closed.clear()
        
        # Start reader thread
        self._read_thread = threading.Thread(target=self._read_loop)
        self._read_thread.daemon = True
        self._read_thread.start()
    
    def _read_loop(self):
        """Background thread that reads from stdin."""
        try:
            while not self._closed.is_set():
                try:
                    # Read a chunk of data
                    chunk = self._stdin.read(4096)
                    if not chunk:  # EOF
                        logger.debug("EOF on stdin, closing transport")
                        self.close()
                        break
                    
                    # Add to buffer and process
                    self._read_buffer.extend(chunk)
                    self._process_buffer()
                except Exception as e:
                    if self.onerror:
                        self.onerror(e)
                    else:
                        logger.error(f"Error reading from stdin: {e}")
        finally:
            # Ensure we call close if the thread exits
            self.close()
    
    def _process_buffer(self):
        """Process the current read buffer looking for complete messages."""
        # Process as many messages as possible from the buffer
        buffer_str = self._read_buffer.decode('utf-8', errors='replace')
        
        # Look for Content-Length header and complete messages
        while True:
            # Find Content-Length header
            match = re.search(r'Content-Length: (\d+)\r\n\r\n', buffer_str)
            if not match:
                break
            
            content_length = int(match.group(1))
            header_end = match.end()
            
            # Check if we have enough data to read the full message
            if len(buffer_str) < header_end + content_length:
                break
            
            # Extract the message
            message_str = buffer_str[header_end:header_end + content_length]
            
            # Remove the processed message from the buffer
            buffer_start = header_end + content_length
            buffer_str = buffer_str[buffer_start:]
            self._read_buffer = bytearray(buffer_str.encode('utf-8'))
            
            # Parse and dispatch the message
            try:
                message = json.loads(message_str)
                if self.onmessage:
                    self.onmessage(message)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse message: {e}")
                if self.onerror:
                    self.onerror(e)
            
            # Process any additional messages in the buffer
            if len(self._read_buffer) > 0:
                self._process_buffer()
    
    def close(self):
        """Close the transport."""
        if not self._started:
            return
        
        self._started = False
        self._closed.set()
        
        if self.onclose:
            self.onclose()
    
    def send(self, message: Dict[str, Any]):
        """
        Send a message to stdout.
        
        Args:
            message: The message to send (will be JSON-encoded)
        """
        if not self._started:
            raise RuntimeError("Transport not started")
        
        # Encode the message
        content = json.dumps(message)
        data = f"Content-Length: {len(content)}\r\n\r\n{content}"
        
        # Write to stdout
        self._stdout.write(data.encode('utf-8'))
        self._stdout.flush()
    
    def wait_until_closed(self):
        """Block until the transport is closed."""
        self._closed.wait()
