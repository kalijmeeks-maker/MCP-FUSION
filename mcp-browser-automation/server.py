#!/usr/bin/env python3
"""
MCP Browser Automation Server

A Model Context Protocol (MCP) server that provides browser automation capabilities
using Playwright. Allows navigation to URLs and extraction of page content.
"""

import asyncio
import json
import logging
import os
import sys
from typing import Any, Dict, Optional

from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeout

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MCPBrowserAutomationServer:
    """MCP Server for browser automation using Playwright."""

    def __init__(self):
        self.browser: Optional[Browser] = None
        self.playwright = None
        # Get configuration from environment variables
        self.headless = os.getenv("BROWSER_HEADLESS", "true").lower() == "true"
        
        # Parse timeout with error handling
        try:
            self.timeout = int(os.getenv("BROWSER_TIMEOUT", "30000"))
        except ValueError:
            logger.warning("Invalid BROWSER_TIMEOUT value, using default 30000ms")
            self.timeout = 30000
            
        self.user_agent = os.getenv("BROWSER_USER_AGENT", "")

    async def initialize(self):
        """Initialize the browser instance."""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            logger.info("Browser initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            raise

    async def cleanup(self):
        """Clean up browser resources."""
        try:
            if self.browser:
                await self.browser.close()
                logger.info("Browser closed")
            if self.playwright:
                await self.playwright.stop()
                logger.info("Playwright stopped")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    async def navigate_and_extract(self, url: str) -> Dict[str, Any]:
        """
        Navigate to a URL and extract page title and content.

        Args:
            url: The URL to navigate to

        Returns:
            Dictionary containing title, content, and metadata

        Raises:
            ValueError: If URL is invalid or empty
            Exception: For browser errors
        """
        if not url or not isinstance(url, str):
            raise ValueError("URL must be a non-empty string")

        if not url.startswith(('http://', 'https://')):
            raise ValueError("URL must start with http:// or https://")

        page: Optional[Page] = None
        try:
            # Create a new page
            page = await self.browser.new_page()

            # Set user agent if configured
            if self.user_agent:
                await page.set_extra_http_headers({"User-Agent": self.user_agent})

            # Navigate to the URL
            logger.info(f"Navigating to {url}")
            response = await page.goto(url, timeout=self.timeout, wait_until="domcontentloaded")

            if not response:
                raise Exception("No response received from page")

            # Extract page information
            title = await page.title()
            content = await page.content()

            # Get text content from body
            text_content = ""
            try:
                body = await page.query_selector("body")
                if body:
                    text_content = await body.inner_text()
            except Exception as e:
                logger.warning(f"Could not extract text content: {e}")

            # Get metadata
            metadata = {
                "url": page.url,
                "status": response.status,
                "status_text": response.status_text,
                "headers": dict(response.headers),
            }

            result = {
                "success": True,
                "title": title,
                "content": content[:10000],  # Limit content size
                "text_content": text_content[:5000],  # Limit text content size
                "metadata": metadata,
            }

            logger.info(f"Successfully extracted content from {url}")
            return result

        except PlaywrightTimeout:
            logger.error(f"Timeout while loading {url}")
            return {
                "success": False,
                "error": "Timeout while loading page",
                "error_type": "timeout",
            }
        except Exception as e:
            logger.error(f"Error navigating to {url}: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__,
            }
        finally:
            if page:
                await page.close()

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming MCP requests.

        Args:
            request: MCP request dictionary

        Returns:
            MCP response dictionary
        """
        try:
            method = request.get("method")
            params = request.get("params", {})

            if method == "navigate_and_extract":
                url = params.get("url")
                if not url:
                    return {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "error": {
                            "code": -32602,
                            "message": "Invalid params: url is required",
                        },
                    }

                result = await self.navigate_and_extract(url)
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": result,
                }

            elif method == "list_capabilities":
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "capabilities": ["navigate_and_extract"],
                        "version": "1.0.0",
                        "description": "MCP Browser Automation Server",
                    },
                }

            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}",
                    },
                }

        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}",
                },
            }

    async def run(self):
        """Run the MCP server (stdio mode)."""
        await self.initialize()

        try:
            logger.info("MCP Browser Automation Server started")

            # Read requests from stdin
            while True:
                try:
                    line = await asyncio.get_event_loop().run_in_executor(
                        None, sys.stdin.readline
                    )

                    if not line:
                        break

                    # Parse JSON-RPC request
                    request = json.loads(line.strip())
                    response = await self.handle_request(request)

                    # Write response to stdout
                    print(json.dumps(response), flush=True)

                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON: {e}")
                    # Send error response to client
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32700,
                            "message": f"Parse error: {str(e)}",
                        },
                    }
                    print(json.dumps(error_response), flush=True)
                except Exception as e:
                    logger.error(f"Error processing request: {e}")

        except KeyboardInterrupt:
            logger.info("Server interrupted")
        finally:
            await self.cleanup()


async def main():
    """Main entry point."""
    server = MCPBrowserAutomationServer()
    await server.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
