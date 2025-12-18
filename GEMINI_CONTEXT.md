CONTEXT: MCP-FUSION repo state as of 2025-12-18

== WHAT WAS FIXED ==

Problem: Python dependencies were being installed into the launcher shell (/bin/zsh) instead of the runtime Python interpreter (.venv/bin/python). Workers fell back to mock coordinator output because `import openai` failed silently.

Root cause: Control plane (shell launchers) and execution plane (Python workers) were conflated. No enforcement existed to prevent wrong-interpreter installs.

== WHAT WAS BUILT ==

1. ARCHITECTURE.md — Canonical system design doc. Defines launcher vs runtime separation.
2. .github/copilot-instructions.md — AI guardrails. Explicit runtime path: /Users/kalimeeks/MCP-FUSION/.venv/bin/python
3. TASKS.md — Single source of truth for tasks. Repo is the shared memory layer (no copy-paste between AIs).
4. scripts/verify.sh — Universal verification entrypoint. Runs locally + in CI. Checks:
   - Runtime discovery via sys.executable
   - Venv enforcement (asserts .venv/bin/python when .venv exists)
   - Dependency imports (json, pathlib, openai)
   - pip check (dependency conflicts)
   - openai version reporting
5. requirements.txt — Canonical deps: openai, redis, pydantic, tenacity, pyyaml, requests, numpy, reportlab
6. .github/workflows/verify.yml — CI automation. Creates venv, installs deps, runs verify.sh.
7. .github/hooks/pre-commit — Local guard against secrets, missing docs, bare python3 refs.
8. .gitignore updated — workspace/memory/ and *.jsonl now ignored (runtime artifacts don't block checkouts).

== CURRENT STATE ==

- main = c032d14 (squashed PR: "MCP-FUSION: runtime enforcement + verify + canonical deps")
- main === origin/main (synced, verified)
- verify.sh passes on main
- Runtime: /Users/kalimeeks/MCP-FUSION/.venv/bin/python (Python 3.13.9)
- openai 2.13.0 installed in runtime

== RULES FOR YOU (GEMINI) ==

1. Never install packages with bare `pip install`. Always use: .venv/bin/python -m pip install <package>
2. Never edit main directly. Create a new branch: git checkout -b wip/$(date +%Y%m%d-%H%M%S)
3. Before any Python work, verify runtime: .venv/bin/python -c "import sys; print(sys.executable)"
4. Read ARCHITECTURE.md and .github/copilot-instructions.md before proposing changes.
5. Use TASKS.md to track work. Update it, don't narrate.
6. Run ./scripts/verify.sh after any dependency or runtime changes.

== NEXT PHASE OPTIONS ==

1. Codex handoff — Make Codex the repo-native copilot (reads docs, follows TASKS.md)
2. MCP server wiring — Wire coordinator → worker → LLM pipeline (stop falling back to mocks)

Awaiting directive.
