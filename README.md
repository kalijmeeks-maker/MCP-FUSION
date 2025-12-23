# MCP-FUSION

MCP-FUSION is a Model Context Protocol (MCP) "fusion layer" that orchestrates multiple AI agent workers and coordinates them via a Redis broker. This repository is wired for a debugger-first, one-button local development experience.

> 📘 **Architecture & Debugging**: See [ARCHITECTURE.md](ARCHITECTURE.md) for system layer separation, runtime dependencies, and troubleshooting. **AI Assistants**: See [.github/copilot-instructions.md](.github/copilot-instructions.md) for critical directives.

## One-Button Full Stack (Local)

Canonical launcher: `./run_fusion.sh`

1) Prepare once:
```bash
cd /Users/kalimeeks/MCP-FUSION
cp workspace/.env.example workspace/.env   # fill in your keys
./run_fusion.sh bootstrap                  # create .venv + install deps
```

2) Start the stack (redis + workers + orchestrator):
```bash
./run_fusion.sh start
```

3) Submit a job from another terminal:
```bash
./run_fusion.sh submit "Explain Bitcoin like I'm 5."
# or use the sample prompt:
./scripts/submit_sample.sh
```

4) Health + status:
```bash
./run_fusion.sh health
./run_fusion.sh status
./run_fusion.sh stop
```

macOS double-click wrapper still works:
```bash
./start-fusion-stack.command   # wraps ./run_fusion.sh start
```

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

- Start stack: `./run_fusion.sh start` (or double-click `start-fusion-stack.command`)
- Stop stack: `./run_fusion.sh stop`
- Health / status: `./run_fusion.sh health` / `./run_fusion.sh status`
- Submit job: `./run_fusion.sh submit "<prompt>"` or `./scripts/submit_sample.sh`
- Gemini helper: `./scripts/gemini_sync.sh`
- Formatting: `npm run format`

## Contributing & Next Steps

- If you want Docker-based VS Code debugging, I can add `docker exec` attach configurations that mirror the local debug configs.
- We intentionally keep the helper scripts non-destructive and idempotent. If you'd like the Gemini helper to run a specific sync flow or copy assets, tell me the commands and I will wire them.

---

If anything should be adjusted (different Gemini path, alternative CLI, or add more npm scripts), tell me and I'll update the wiring.
