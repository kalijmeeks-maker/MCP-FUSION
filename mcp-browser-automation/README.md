# MCP Browser Automation Server

A Model Context Protocol (MCP) server that provides browser automation capabilities using Playwright. This server enables web navigation, content extraction, and metadata retrieval through a standardized MCP interface.

## Features

- **URL Navigation**: Navigate to any web page and extract content
- **Content Extraction**: Retrieve page title, HTML content, and plain text
- **Metadata Collection**: Capture response status, headers, and URL information
- **Error Handling**: Robust error handling with detailed error messages
- **Security**: Environment variable-based configuration, non-root execution
- **Containerized**: Docker support for easy deployment
- **MCP Compliant**: Follows Model Context Protocol standards

## Prerequisites

- Python 3.10 or higher
- Docker (for containerized deployment)
- Internet connection (for browser automation)

## Installation

### Local Installation

1. **Clone the repository** (if not already cloned):
   ```bash
   git clone https://github.com/kalijmeeks-maker/MCP-FUSION.git
   cd MCP-FUSION/mcp-browser-automation
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**:
   ```bash
   playwright install chromium
   ```

### Docker Installation

1. **Build the Docker image**:
   ```bash
   docker build -t mcp-browser-automation:latest .
   ```

2. **Run the container**:
   ```bash
   docker run -i mcp-browser-automation:latest
   ```

## Configuration

The server is configured using environment variables. All settings are optional with secure defaults.

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `BROWSER_HEADLESS` | Run browser in headless mode | `true` | No |
| `BROWSER_TIMEOUT` | Page load timeout (milliseconds) | `30000` | No |
| `BROWSER_USER_AGENT` | Custom user agent string | (empty) | No |

### Setting Environment Variables

**Linux/macOS**:
```bash
export BROWSER_HEADLESS=true
export BROWSER_TIMEOUT=60000
export BROWSER_USER_AGENT="Mozilla/5.0 Custom"
```

**Windows (PowerShell)**:
```powershell
$env:BROWSER_HEADLESS="true"
$env:BROWSER_TIMEOUT="60000"
$env:BROWSER_USER_AGENT="Mozilla/5.0 Custom"
```

**Docker**:
```bash
docker run -i \
  -e BROWSER_HEADLESS=true \
  -e BROWSER_TIMEOUT=60000 \
  mcp-browser-automation:latest
```

## Usage

### Running the Server

**Local**:
```bash
python server.py
```

**Docker**:
```bash
docker run -i mcp-browser-automation:latest
```

### MCP Communication

The server uses JSON-RPC 2.0 over stdio. Send requests to stdin and receive responses from stdout.

#### Navigate and Extract Content

**Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "navigate_and_extract",
  "params": {
    "url": "https://example.com"
  }
}
```

**Response (Success)**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "success": true,
    "title": "Example Domain",
    "content": "<!DOCTYPE html><html>...",
    "text_content": "Example Domain This domain is for use in...",
    "metadata": {
      "url": "https://example.com/",
      "status": 200,
      "status_text": "OK",
      "headers": {
        "content-type": "text/html; charset=UTF-8"
      }
    }
  }
}
```

**Response (Error)**:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "success": false,
    "error": "Timeout while loading page",
    "error_type": "timeout"
  }
}
```

#### List Capabilities

**Request**:
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "list_capabilities",
  "params": {}
}
```

**Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "capabilities": ["navigate_and_extract"],
    "version": "1.0.0",
    "description": "MCP Browser Automation Server"
  }
}
```

## Testing

### Manual Testing

You can test the server using a simple Python script or shell commands:

**Using echo and pipes**:
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"list_capabilities","params":{}}' | python server.py
```

**Using Python client**:
```python
import json
import subprocess

request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "navigate_and_extract",
    "params": {"url": "https://example.com"}
}

process = subprocess.Popen(
    ["python", "server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

stdout, stderr = process.communicate(
    input=json.dumps(request).encode() + b"\n",
    timeout=60
)

response = json.loads(stdout.decode())
print(json.dumps(response, indent=2))
```

## Security Considerations

### Best Practices

1. **Environment Variables**: Never hardcode sensitive information. Always use environment variables for configuration.

2. **Network Security**:
   - Only navigate to trusted URLs
   - Be cautious with user-supplied URLs
   - Consider implementing URL whitelisting for production use
   - Use HTTPS URLs when possible

3. **Container Security**:
   - The container runs as a non-root user (`mcpuser`)
   - Minimal system privileges
   - No unnecessary capabilities

4. **Resource Limits**:
   - Content is limited to 10,000 characters (HTML)
   - Text content is limited to 5,000 characters
   - Timeout prevents indefinite hangs
   - Consider setting Docker memory/CPU limits

5. **Input Validation**:
   - URLs are validated before navigation
   - Only HTTP/HTTPS protocols are allowed
   - JSON-RPC requests are validated

6. **Secrets Management**:
   - Use environment variables for secrets
   - Never log sensitive information
   - Consider using secrets managers (Vault, AWS Secrets Manager, etc.)

### Security Recommendations for Production

1. **Use a secrets manager** instead of environment variables for sensitive data
2. **Implement rate limiting** to prevent abuse
3. **Add URL filtering** to restrict navigation to approved domains
4. **Enable audit logging** for compliance
5. **Run in isolated network** with restricted internet access
6. **Keep dependencies updated** to patch security vulnerabilities
7. **Use read-only root filesystem** where possible
8. **Implement request authentication** for MCP clients

### Known Limitations

- The server accepts any valid HTTP/HTTPS URL
- No built-in authentication mechanism
- Limited to Chromium browser
- Content size limits may truncate large pages
- No built-in rate limiting

## Troubleshooting

### Browser Installation Issues

If Playwright browser installation fails:
```bash
# Try installing system dependencies first
playwright install-deps chromium
playwright install chromium
```

### Docker Build Issues

If Docker build fails, ensure you have enough disk space and memory:
```bash
docker system prune -a  # Clean up old images
docker build --no-cache -t mcp-browser-automation:latest .
```

### Timeout Errors

If pages timeout frequently:
- Increase `BROWSER_TIMEOUT` environment variable
- Check internet connection
- Verify the target URL is accessible

### Permission Errors

If you get permission errors in Docker:
```bash
# Ensure proper permissions on mounted volumes
docker run -i --user $(id -u):$(id -g) mcp-browser-automation:latest
```

## MCP Registry Integration

The server includes a catalog definition file (`mcp-catalog.yaml`) that can be used to register this server in an MCP registry. The catalog includes:

- Server metadata and versioning
- Capability definitions with parameters and return types
- Configuration options
- Security constraints
- Resource limits
- Usage examples

To register with an MCP registry, submit the `mcp-catalog.yaml` file according to your registry's submission process.

## Development

### Project Structure

```
mcp-browser-automation/
├── server.py              # Main server implementation
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container definition
├── mcp-catalog.yaml      # MCP registry catalog
└── README.md             # This file
```

### Contributing

When contributing to this server:

1. Follow PEP 8 style guidelines
2. Add docstrings to all functions
3. Include error handling for all external calls
4. Update the README with new features
5. Test both local and containerized deployments
6. Update the catalog definition for capability changes

### Future Enhancements

Potential improvements for future versions:

- Multiple browser support (Firefox, WebKit)
- Screenshot capture capability
- Cookie management
- Form filling and interaction
- JavaScript execution
- PDF generation
- Network request interception
- Response caching

## License

This project is part of the MCP-FUSION stack. See the main repository for license information.

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Refer to the main MCP-FUSION documentation
- Check the MCP specification at https://modelcontextprotocol.io

## Changelog

### Version 1.0.0
- Initial release
- Basic URL navigation and content extraction
- Docker containerization
- MCP catalog definition
- Comprehensive documentation
