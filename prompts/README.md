# Prompts Directory

This directory contains prompt templates and instructions for AI agents working with the MCP-FUSION system.

## 🎯 Quick Start

**Want to use MCP-FUSION in a chat?** 👉 See **[CHAT_GUIDE.md](CHAT_GUIDE.md)** for step-by-step instructions.

## Files

### `fusion_agent_chat.md` ⭐ NEW

**Chat-optimized version** of the Fusion Agent prompt, ready to copy-paste into:

- GitHub Copilot Chat
- ChatGPT
- Claude
- Any AI chat interface

This is formatted for conversational interaction with clear mode switching, example commands, and quick reference. **Start here if you want to chat with the Fusion Agent!**

### `fusion_agent.md`

The complete mega prompt for GitHub Copilot and other AI agents. This defines:

- Agent identity and responsibilities
- Sub-agent roles (Wealth, Ops, Critic, Judge, Scribe)
- Working styles and behaviors
- Safety guidelines
- Execution modes
- Detailed format templates

**Usage**: Use this for comprehensive reference or when you need all the detailed templates and examples.

### `CHAT_GUIDE.md`

Step-by-step guide for using the chat prompt with examples, tips, and troubleshooting.

## Prompt Categories

### System Prompts

Core identity and behavior prompts for the main Fusion Agent.

### Sub-Agent Prompts

Specialized prompts for each sub-agent role:

- `wealth_agent_prompt.md` - Financial analysis and strategy
- `ops_agent_prompt.md` - Workflow automation
- `critic_agent_prompt.md` - Code review and quality
- `judge_agent_prompt.md` - Multi-model output merging
- `scribe_agent_prompt.md` - Documentation and summaries

### Task Templates

Reusable prompt templates for common tasks:

- Code refactoring
- MCP server integration
- Documentation generation
- Testing workflows

### Workflow Prompts

Multi-step workflow instructions:

- Bug fix workflow
- Feature development workflow
- PR review workflow
- Session planning workflow

## Using Prompts

### For GitHub Copilot

1. Open the prompt file (e.g., `fusion_agent.md`)
2. Copy the entire content
3. Paste into GitHub Copilot Chat
4. Copilot will adopt the agent identity

### For Other AI Systems

Prompts can be adapted for:

- Claude (Anthropic)
- ChatGPT (OpenAI)
- DeepSeek
- Grok (xAI)
- Perplexity

### For Custom Agents

Use prompts as base templates and customize:

1. Copy the base prompt
2. Modify for your specific use case
3. Add domain-specific context
4. Test and iterate

## Prompt Engineering Tips

### Best Practices

- **Be specific**: Clear, detailed instructions
- **Provide examples**: Show desired output format
- **Set constraints**: Define what NOT to do
- **Include context**: Background information
- **Iterate**: Refine based on results

### Prompt Structure

Good prompts typically include:

1. **Identity**: Who the agent is
2. **Mission**: What the agent should do
3. **Context**: Background information
4. **Guidelines**: How to work
5. **Examples**: Concrete examples
6. **Constraints**: Safety and limitations

## Creating New Prompts

When creating a new prompt:

1. **Start with a template**:

   ```markdown
   # Agent Name

   ## Identity

   You are...

   ## Mission

   Your goal is...

   ## Guidelines

   - Guideline 1
   - Guideline 2
   ```

2. **Test thoroughly**: Try the prompt with different inputs

3. **Document usage**: Explain when to use this prompt

4. **Version control**: Track changes and improvements

## Prompt Variables

Use placeholders for dynamic content:

- `{PROJECT_NAME}` - Project name
- `{TASK_DESCRIPTION}` - Task details
- `{CONTEXT}` - Relevant context
- `{CONSTRAINTS}` - Specific constraints

## Multi-Model Fusion

For fusion workflows, combine prompts:

1. Send to multiple models
2. Collect responses
3. Use Judge agent to merge
4. Validate with Critic agent

## Security Considerations

When writing prompts:

- Never include actual API keys
- Use placeholder values
- Remind agents about security
- Include safety guidelines

## Maintenance

Prompts should be:

- **Reviewed regularly**: Update as the system evolves
- **Versioned**: Track significant changes
- **Tested**: Verify effectiveness
- **Documented**: Explain purpose and usage

---

## Examples

### Quick Task Prompt

```markdown
Task: {TASK_DESCRIPTION}
Context: {CONTEXT}
Constraints: {CONSTRAINTS}
Output format: {FORMAT}
```

### Code Review Prompt

```markdown
Review the following code changes:

- Check for security issues
- Verify best practices
- Suggest improvements
- Provide actionable feedback
```

---

For more information, see [/docs/context.md](../docs/context.md) and the main [README.md](../README.md).
