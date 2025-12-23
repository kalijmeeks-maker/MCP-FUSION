# Using MCP-FUSION in Chat - Quick Start Guide

## 🎯 Overview

This guide shows you how to use the MCP-FUSION agent prompts in various chat interfaces.

## 📋 Choose Your Chat Interface

### Option 1: GitHub Copilot Chat (Recommended)

**Step 1: Open the Chat Prompt**

```bash
cat prompts/fusion_agent_chat.md
```

**Step 2: Copy Everything**

- Select all text from the file
- Copy to clipboard (Ctrl+C / Cmd+C)

**Step 3: Paste into Copilot Chat**

1. Open GitHub Copilot Chat in VS Code or GitHub.com
2. Paste the entire prompt
3. Press Enter

**Step 4: Start Working**

```
You: "I'm the Kali Fusion Agent now. Let's review the codebase as Critic Agent."
```

---

### Option 2: ChatGPT / Claude / Other AI

**Step 1: Copy the Prompt**

```bash
cat prompts/fusion_agent_chat.md
```

**Step 2: Start a New Chat**

- Open ChatGPT, Claude, or your preferred AI
- Start a new conversation

**Step 3: Paste as First Message**

- Paste the entire `fusion_agent_chat.md` content
- The AI will adopt the Fusion Agent identity

**Step 4: Continue the Conversation**

```
You: "Switch to Architect Mode and help me design an MCP server for Puppeteer"
```

---

### Option 3: Using with the Full Mega Prompt

For more comprehensive behavior, use the original mega prompt:

```bash
cat prompts/fusion_agent.md
```

This is more detailed and includes all formatting templates. Use when you need complete reference.

---

## 🎨 Example Conversations

### Example 1: Code Review

```
You: "I just wrote a new agent in src/agents/wealth_agent.py.
      Switch to Critic Agent mode and review it for security and style."

Fusion Agent: *[Switches to Critic Mode]*
Let me review src/agents/wealth_agent.py...

[Reviews code, checks for API key exposure, validates patterns]

Here are my findings:
1. ✅ Good: Uses environment variables for API keys
2. ⚠️ Issue: Missing error handling on line 45
3. 💡 Suggestion: Add docstrings following project conventions
...
```

### Example 2: Architecture Design

```
You: "Switch to Architect Mode. I want to add GGWave support for
      ultrasonic data transfer. Design the MCP server structure."

Fusion Agent: *[Switches to Architect Mode]*
Let me design the GGWave MCP server integration...

Directory: /mcp_servers/ggwave/
Files needed:
- config.json (server configuration)
- catalog.yaml (tool definitions)
- README.md (usage docs)
...
```

### Example 3: Multi-Model Fusion

```
You: "Switch to Fusion Mode. Get opinions from GPT-4, Claude, and
      DeepSeek on the best architecture for our orchestration layer."

Fusion Agent: *[Switches to Fusion Mode]*
I'll conceptually query multiple models and merge insights...

GPT-4 suggests: Event-driven architecture with async message passing
Claude suggests: Actor model with supervision trees
DeepSeek suggests: Functional pipeline with immutable state

Judge Agent synthesis: Combine event-driven foundation with
functional pipelines for data flow and actor-style agents for
stateful operations...
```

### Example 4: Documentation

```
You: "Switch to Scribe Mode. Document the session where we added
      Notion integration. Update docs/context.md."

Fusion Agent: *[Switches to Scribe Mode]*
Creating session summary...

## Session: Notion MCP Integration
Date: [date]
Mode: Coder + Scribe
Outcome: Successfully integrated Notion API via MCP server
...
```

---

## 🔄 Switching Modes Mid-Conversation

You can switch agent modes anytime:

```
"Switch to Critic Mode"
"Use Architect Mode now"
"Become Scribe Agent"
"Enter Fusion Mode"
"Switch back to Coder Mode"
```

The agent will adapt its behavior accordingly.

---

## 📊 Mode-Specific Commands

### Architect Mode Commands

- "Design the architecture for [feature]"
- "Propose a structure for [component]"
- "Plan the integration of [tool]"
- "Sketch a workflow for [process]"

### Coder Mode Commands

- "Implement [feature] in [file]"
- "Write a function that [does X]"
- "Refactor [code] to use [pattern]"
- "Add error handling to [module]"

### Critic Mode Commands

- "Review [file] for security issues"
- "Check [code] against project conventions"
- "Audit [component] for best practices"
- "Find potential bugs in [module]"

### Scribe Mode Commands

- "Document [feature] in [location]"
- "Summarize this session"
- "Update the ADR for [decision]"
- "Write a README for [directory]"

### Fusion Mode Commands

- "Compare all models on [question]"
- "Get diverse opinions on [topic]"
- "Merge ideas from different approaches"
- "Find consensus on [decision]"

---

## 🎓 Pro Tips

### Tip 1: Be Specific About Context

❌ Bad: "Fix the bug"
✅ Good: "In src/agents/ops_agent.py, fix the null pointer error on line 67"

### Tip 2: Specify the Mode

❌ Bad: "Look at this code"
✅ Good: "Switch to Critic Mode and review src/core/orchestrator.py for security"

### Tip 3: Reference Sub-Agents

❌ Bad: "Help with financial stuff"
✅ Good: "As Wealth Agent, analyze this stock data structure"

### Tip 4: Use Action Categories

✅ "This is a Repo Action - create directory structure"
✅ "This is an MCP Action - configure Puppeteer server"
✅ "This is Orchestration Logic - design fusion workflow"

### Tip 5: Chain Operations

```
"First, as Architect, design the API.
Then switch to Coder and implement it.
Finally, as Critic, review for security."
```

---

## 🔧 Troubleshooting

### Issue: Agent Not Following Fusion Patterns

**Solution:** Re-paste the prompt or remind it:

```
"Remember, you're the Kali Fusion Agent. Use MCP-FUSION conventions."
```

### Issue: Too Verbose

**Solution:** Request concise output:

```
"Be more concise. Just the key points."
```

### Issue: Not Using Correct Mode

**Solution:** Explicitly state the mode:

```
"I need you in Critic Mode specifically, not general advice."
```

---

## 📚 Quick Reference Card

```
┌─────────────────────────────────────────┐
│  MCP-FUSION AGENT QUICK REFERENCE       │
├─────────────────────────────────────────┤
│ MODES:                                  │
│  🏗️ Architect  - Design & plan          │
│  💻 Coder      - Implement & build      │
│  🔍 Critic     - Review & audit         │
│  📝 Scribe     - Document & record      │
│  🔮 Fusion     - Multi-model synthesis  │
│                                         │
│ SUB-AGENTS:                             │
│  🤑 Wealth     - Financial analysis     │
│  ⚙️ Ops        - Workflow automation    │
│  🔍 Critic     - Quality review         │
│  ⚖️ Judge      - Output merging         │
│  📝 Scribe     - Documentation          │
│                                         │
│ CATEGORIES:                             │
│  📁 Repo       - Files & docs           │
│  🔌 MCP        - Server configs         │
│  🎭 Orchestr.  - Agent logic            │
│  🔬 Research   - Analysis & design      │
└─────────────────────────────────────────┘
```

---

## 🚀 Ready to Use

1. Copy `prompts/fusion_agent_chat.md`
2. Paste into your AI chat interface
3. Start with: "What should I work on next?"
4. Specify modes as needed
5. Build amazing things!

---

_For the complete mega prompt with all details, see [fusion_agent.md](fusion_agent.md)_
