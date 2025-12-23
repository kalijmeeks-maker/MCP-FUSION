# MCP-FUSION

MCP-FUSION is a Model Context Protocol (MCP) "fusion layer" that orchestrates multiple AI agent workers and coordinates them via a Redis broker. This repository is wired for a debugger-first, one-button local development experience.

## 🚀 Quick Start: Interactive REPL

Launch the interactive command-line interface:

```bash
./scripts/start_fusion_repl.sh
```

This starts the Fusion REPL where you can submit tasks and get real-time responses from the orchestration system. See **[REPL_GUIDE.md](docs/REPL_GUIDE.md)** for complete documentation.

## One-Button Full Stack (Local)

From the project root (`/Users/kalimeeks/MCP-FUSION`) you can start the full local stack using the macOS-friendly wrapper or the script directly.

- macOS double-click / command wrapper (recommended):

```bash
cd /Users/kalimeeks/MCP-FUSION
./start-fusion-stack.command
```

- Script (terminal):

```bash
cd /Users/kalimeeks/MCP-FUSION
./scripts/start_fusion_stack.sh
```

The above brings up the Docker stack (Redis + fusion container) and opens a `tmux` session with the usual panes used for development.

## Gemini CLI Integration

This project expects the Gemini management hub to live at:

`/Users/kalimeeks/GEMINI-STACK/workspace`

A safe helper script is provided to inspect or forward commands to your local `gemini` CLI. It is non-destructive and will not modify either repository.

From the MCP-FUSION root run:

```bash
cd /Users/kalimeeks/MCP-FUSION
./scripts/gemini_sync.sh
```

Notes:

- The helper verifies the hub path exists and `cd`s into it.
- If the `gemini` CLI is on your `PATH`, the helper forwards all provided arguments to it, e.g.:

```bash
./scripts/gemini_sync.sh mcp list
```

- If `gemini` is not installed, the script prints a friendly warning and exits without making changes.

## NPM scripts (developer convenience)

We include minimal npm tooling so you can run common actions from the terminal or VS Code tasks.

From the repo root (`/Users/kalimeeks/MCP-FUSION`):

- Start the stack (wrapper):

```bash
npm run start
# -> runs ./run_fusion.sh start
```

- Stop the stack:

```bash
npm run stop
```

- Bring up Docker services:

```bash
npm run docker:up
npm run docker:logs
```

- Run the Gemini helper:

```bash
npm run gemini:sync -- <args>
# e.g. npm run gemini:sync -- mcp list
```

- Format the repository (Prettier):

```bash
npm run format
```

Prettier is installed as a dev dependency. If you need to update or re-install node modules:

```bash
cd /Users/kalimeeks/MCP-FUSION
npm install
```

## VS Code Tasks

Developer-friendly tasks are available in `.vscode/tasks.json` to run the npm scripts from the Command Palette or to bind keyboard shortcuts. Use the `MCP-FUSION: Full Stack (Local)` debug compound in `.vscode/launch.json` for one-button debugging.

## Day-to-day Commands (Summary)

- One-button full stack launcher (macOS):

```bash
cd /Users/kalimeeks/MCP-FUSION
./start-fusion-stack.command
```

- Gemini sync / helper script:

```bash
cd /Users/kalimeeks/MCP-FUSION
./scripts/gemini_sync.sh  # forwards args to gemini CLI if available
```

- NPM format (Prettier):

```bash
cd /Users/kalimeeks/MCP-FUSION
npm run format
```

## Repository Structure

The MCP-FUSION project follows a modular architecture:

```
/src                    - Source code
  /agents              - Agent implementations (Wealth, Ops, Critic, Judge, Scribe)
  /core                - Core orchestration and fusion logic
  /utils               - Utility functions and helpers
/mcp_servers           - MCP server configurations and catalogs
  /puppeteer           - Browser automation
  /filesystem          - File operations
  /git                 - Git/GitHub integration
  /ggwave              - Audio-based communication
  /notion              - Notion API integration
/docs                  - Documentation and architecture decisions
  context.md           - Living document for session tracking
  architecture.md      - System architecture
/prompts               - AI agent prompts and templates
  fusion_agent.md      - Main Copilot mega prompt
/tests                 - Test suites
  /unit                - Unit tests
  /integration         - Integration tests
  /e2e                 - End-to-end tests
/scripts               - Utility scripts
/.github               - GitHub templates and workflows
  /ISSUE_TEMPLATE      - Issue templates (bug, feature, task, session)
  PULL_REQUEST_TEMPLATE.md - PR template
```

## AI Agent System

This repository is designed to work with AI agents following the **Fusion Agent** paradigm:

### Main Fusion Agent

Located at `/prompts/fusion_agent.md`, this is the primary prompt for GitHub Copilot and other AI assistants. It defines:

- Agent identity and mission
- Sub-agent roles and capabilities
- Working styles and safety guidelines
- Execution modes (Architect, Coder, Critic, Scribe, Fusion)

### Sub-Agents (Conceptual Roles)

1. **Wealth Agent** - Financial analysis and data structuring
2. **Ops Agent** - Workflow automation with Notion/Slack/n8n
3. **Critic Agent** - Code review and quality assessment
4. **Judge Agent** - Multi-model output merging
5. **Scribe Agent** - Documentation and session summaries

### Using the Fusion Agent

```bash
# View the mega prompt
cat prompts/fusion_agent.md

# Copy it into GitHub Copilot Chat or your AI assistant
# The agent will adopt the Fusion Agent identity and behaviors
```

## GitHub Templates

### Issue Templates

- **Bug Report** (`.github/ISSUE_TEMPLATE/bug_report.yml`) - Report bugs with structured format
- **Feature Request** (`.github/ISSUE_TEMPLATE/feature_request.yml`) - Suggest new features
- **Task** (`.github/ISSUE_TEMPLATE/task.yml`) - Create executable tasks with plans
- **Agent Session** (`.github/ISSUE_TEMPLATE/session.yml`) - Track AI agent work sessions

### Pull Request Template

Located at `.github/PULL_REQUEST_TEMPLATE.md`, includes:

- Summary and changes made
- Category classification
- Testing steps and checklist
- Agent mode tracking
- Security notes

## Documentation

All documentation lives in `/docs`:

- **[context.md](docs/context.md)** - Track decisions, sessions, and key learnings (living document)
- **[README.md](docs/README.md)** - Documentation hub with links to all guides
- Architecture Decision Records (ADRs)
- Technical guides and tutorials

Key documentation sections:

- Architecture and design patterns
- MCP server integration guide
- Agent development guide
- Testing strategies
- Troubleshooting

## MCP Server Integration

MCP (Model Context Protocol) servers provide standardized interfaces for AI agents. This project uses:

- **Puppeteer** - Headless browser automation
- **Filesystem** - Safe file operations
- **Git/GitHub** - Repository management
- **GGWave** - Ultrasonic audio data transfer
- **Notion** - Notion API integration

See [mcp_servers/README.md](mcp_servers/README.md) for details on using and creating MCP servers.

## Development Workflow

### Starting a Work Session

1. Create an Agent Session issue (use template)
2. Adopt the appropriate agent mode (Architect, Coder, Critic, etc.)
3. Reference the Fusion Agent prompt
4. Track progress in the session issue

### Making Changes

1. Create a feature branch
2. Make small, incremental changes
3. Commit with clear messages
4. Open PR using the template
5. Request reviews

### Code Review

- Use Critic Agent mode for reviews
- Check for security issues
- Verify no hardcoded secrets
- Ensure documentation is updated

## Contributing & Next Steps

### Contributing Guidelines

- Follow the [Fusion Agent principles](prompts/fusion_agent.md)
- Make small, surgical changes
- Use environment variables for secrets
- Write clear commit messages
- Update documentation as needed
- Add tests for new functionality

### Future Enhancements

- Docker-based VS Code debugging configurations
- Additional MCP server integrations
- Enhanced multi-model fusion logic
- Automated testing workflows
- CI/CD pipeline improvements

---

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [n8n Workflows](https://docs.n8n.io/)
- [GGWave](https://github.com/ggerganov/ggwave)

---

If anything should be adjusted (different Gemini path, alternative CLI, or add more npm scripts), tell me and I'll update the wiring.
