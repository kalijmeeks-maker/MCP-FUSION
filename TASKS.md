# MCP-FUSION TASKS

## Canon (authoritative)
- ARCHITECTURE.md
- .github/copilot-instructions.md
- README.md

## Current Objective
Standardize runtime Python and verification flow so "wrong interpreter" failures are impossible to reintroduce unnoticed.

## Tasks
- [ ] TASK-001: Standardize runtime Python & verification
  - Goal:
    - Runtime Python is explicit and verifiable
    - One command verifies the environment + imports
    - CI enforces the rule
  - Acceptance tests:
    - `./scripts/verify.sh` exits 0 in a correct dev environment
    - `./scripts/verify.sh` fails in CI if the runtime rules are violated
    - Runtime discovery uses `sys.executable` (never launcher shebang)
  - Notes:
- [ ] TASK-002: Implement MCP server wiring
  - Goal:
    - Replace mock outputs in coordinator_worker.py with real multi-LLM pipeline calls.
    - Use tenacity for retries in llm_clients.py.
    - Create replay_diff.py for debugging.
  - Acceptance tests:
    - coordinator_worker.py successfully calls llm_clients.py.
    - llm_clients.py returns completions from multiple LLMs.
    - replay_diff.py can compare two jsonl files.

## Decisions Log
- 2025-12-17: Repo is the shared memory layer (no manual relay). Runtime Python must be verified via `sys.executable`.

## Runbook
- Verify locally:
  - `cd /Users/kalimeeks/MCP-FUSION && ./scripts/verify.sh`
- Rollback:
  - `git revert <sha>`
