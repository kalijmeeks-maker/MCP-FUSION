# Source Code Directory

This directory contains the main source code for the MCP-FUSION system.

## Structure

### `/agents`

Contains agent implementations and logic for the various sub-agents:

- Wealth Agent - Financial analysis and data structuring
- Ops Agent - Workflow automation and integrations
- Critic Agent - Code review and quality assessment
- Judge Agent - Multi-model output merging and conflict resolution
- Scribe Agent - Documentation and session summaries

### `/core`

Core orchestration logic and fusion system:

- Model orchestration
- MCP server integrations
- Message routing and coordination
- State management

### `/utils`

Utility functions and helpers:

- Configuration management
- Logging and debugging
- Common helpers
- Type definitions

## Development Guidelines

1. **Keep it modular**: Each agent should be self-contained
2. **Use MCP servers**: All external integrations through MCP
3. **Environment variables**: No hardcoded secrets
4. **Document as you go**: Include docstrings and comments
5. **Test coverage**: Write tests for new functionality

## Getting Started

```bash
# Install dependencies
npm install

# Run in development mode
npm start

# Run tests (when available)
npm test
```

## Architecture Principles

- **Safety First**: Never expose secrets or credentials
- **Small Changes**: Prefer incremental, surgical modifications
- **Clear Intent**: Explain why changes are made
- **Functional Design**: Use functional architecture patterns
- **Multi-Model**: Design for parallel model execution

## Adding New Agents

When adding a new agent:

1. Create a new file in `/agents`
2. Implement the agent interface
3. Add to the orchestrator
4. Document in `/docs`
5. Update tests

## MCP Server Integration

To integrate a new MCP server:

1. Define the server configuration in `/mcp_servers`
2. Add catalog YAML if needed
3. Create wrapper in `/core`
4. Test the integration
5. Document usage

---

For more information, see the main [README.md](../README.md) and [docs/context.md](../docs/context.md).
