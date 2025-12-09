#!/usr/bin/env python3
"""
Example MCP Browser Automation Client

Demonstrates how to interact with the MCP Browser Automation Server.
"""

import json
import subprocess
import sys


def send_request(method: str, params: dict = None, request_id: int = 1):
    """
    Send a JSON-RPC request to the MCP server.
    
    Args:
        method: The method name to call
        params: Parameters for the method
        request_id: Request ID for tracking
        
    Returns:
        dict: The server response
    """
    request = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method,
        "params": params or {}
    }
    
    print(f"\n📤 Sending request: {method}")
    print(json.dumps(request, indent=2))
    
    try:
        # Start the server process
        process = subprocess.Popen(
            [sys.executable, "server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send request and get response
        stdout, stderr = process.communicate(
            input=json.dumps(request) + "\n",
            timeout=60
        )
        
        if stderr:
            print(f"⚠️  Server stderr: {stderr}")
        
        # Parse response
        response = json.loads(stdout.strip())
        print(f"\n📥 Response received:")
        print(json.dumps(response, indent=2))
        
        return response
        
    except subprocess.TimeoutExpired:
        print("❌ Request timed out")
        process.kill()
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse response: {e}")
        print(f"Raw output: {stdout}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    """Run example requests."""
    print("=" * 60)
    print("MCP Browser Automation Server - Example Client")
    print("=" * 60)
    
    # Example 1: List capabilities
    print("\n" + "=" * 60)
    print("Example 1: List Server Capabilities")
    print("=" * 60)
    response = send_request("list_capabilities")
    
    if response and "result" in response:
        print("\n✅ Success!")
        print(f"Capabilities: {response['result']['capabilities']}")
        print(f"Version: {response['result']['version']}")
    
    # Example 2: Navigate and extract content
    print("\n" + "=" * 60)
    print("Example 2: Navigate to URL and Extract Content")
    print("=" * 60)
    
    test_url = "https://example.com"
    print(f"Target URL: {test_url}")
    
    response = send_request(
        "navigate_and_extract",
        {"url": test_url},
        request_id=2
    )
    
    if response and "result" in response:
        result = response["result"]
        if result.get("success"):
            print("\n✅ Success!")
            print(f"Title: {result.get('title')}")
            print(f"Status: {result['metadata']['status']}")
            print(f"URL: {result['metadata']['url']}")
            print(f"Content length: {len(result.get('content', ''))}")
            print(f"Text content preview: {result.get('text_content', '')[:100]}...")
        else:
            print(f"\n❌ Request failed: {result.get('error')}")
    
    # Example 3: Invalid URL (error handling)
    print("\n" + "=" * 60)
    print("Example 3: Error Handling (Invalid URL)")
    print("=" * 60)
    
    invalid_url = "not-a-valid-url"
    print(f"Target URL: {invalid_url}")
    
    response = send_request(
        "navigate_and_extract",
        {"url": invalid_url},
        request_id=3
    )
    
    if response and "result" in response:
        result = response["result"]
        if not result.get("success"):
            print("\n✅ Error handling working correctly!")
            print(f"Error: {result.get('error')}")
            print(f"Error type: {result.get('error_type')}")
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
