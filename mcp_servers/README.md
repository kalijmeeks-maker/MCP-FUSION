# MCP Servers Directory

This directory contains MCP (Model Context Protocol) server configurations and catalogs.

## Purpose

MCP servers provide standardized interfaces for AI agents to interact with external tools and systems. This directory organizes server definitions, configurations, and catalogs.

## Structure

```
/mcp_servers
  /puppeteer      - Headless browser automation
  /filesystem     - File system operations
  /git            - Git repository operations
  /ggwave         - Audio-based data transfer
  /notion         - Notion API integration
  /custom         - Custom MCP server implementations
```

## Available MCP Servers

### Puppeteer Browser
Provides headless browser capabilities for:
- Web scraping
- Screenshot capture
- Form automation
- Navigation tasks

### Filesystem
Safe file system operations:
- Read/write files
- Directory traversal
- File metadata

### Git/GitHub
Git repository operations:
- Commit and push
- Branch management
- PR operations
- Issue tracking

### GGWave
Audio-based communication:
- Encode data to ultrasonic audio
- Decode audio to data
- Air-gapped device communication

### Notion
Notion API integration:
- Database queries
- Page creation
- Content updates

## Adding a New MCP Server

1. **Create directory structure**:
   ```bash
   mkdir -p mcp_servers/server_name
   cd mcp_servers/server_name
   ```

2. **Define server configuration**:
   Create `config.json` or `config.yaml` with server settings

3. **Create catalog** (if needed):
   Create `catalog.yaml` defining available tools and endpoints

4. **Document usage**:
   Add `README.md` explaining how to use the server

5. **Integrate**:
   Wire the server into the core orchestration layer

## Server Configuration Format

### Basic config.json example:
```json
{
  "name": "server-name",
  "version": "1.0.0",
  "description": "Server description",
  "transport": "stdio",
  "capabilities": [
    "tool-calling",
    "resource-access"
  ],
  "env": {
    "API_KEY": "${SERVER_API_KEY}"
  }
}
```

### Catalog YAML example:
```yaml
name: Server Name
version: 1.0.0
tools:
  - name: tool_name
    description: Tool description
    parameters:
      - name: param1
        type: string
        required: true
```

## Security Considerations

- **Never hardcode API keys**: Use environment variables
- **Validate inputs**: All MCP server inputs should be validated
- **Limit permissions**: Grant minimum necessary permissions
- **Review configurations**: Regular security audits

## Testing MCP Servers

```bash
# Test server connectivity
npm run test:mcp -- server-name

# Validate catalog
npm run validate:catalog -- server-name/catalog.yaml
```

## Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [MCP Server Examples](https://github.com/modelcontextprotocol/servers)
- [Building Custom Servers](../docs/building-mcp-servers.md)

---

For integration details, see [/src/core](../src/README.md) and [/docs/context.md](../docs/context.md).
