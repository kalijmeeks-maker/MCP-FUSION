# MCP-FUSION

MCP-FUSION is a Model Context Protocol (MCP) "fusion layer" that orchestrates multiple AI agent workers and coordinates them via a Redis broker. This repository is wired for a debugger-first, one-button local development experience.

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

## Contributing & Next Steps

- If you want Docker-based VS Code debugging, I can add `docker exec` attach configurations that mirror the local debug configs.
- We intentionally keep the helper scripts non-destructive and idempotent. If you'd like the Gemini helper to run a specific sync flow or copy assets, tell me the commands and I will wire them.

---

If anything should be adjusted (different Gemini path, alternative CLI, or add more npm scripts), tell me and I'll update the wiring.
