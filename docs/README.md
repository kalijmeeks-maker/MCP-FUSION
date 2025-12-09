# Documentation

This directory contains documentation for the MCP-FUSION project.

## Quick Links

- [Context & Session History](context.md) - Track decisions, sessions, and key learnings
- [Architecture Overview](architecture.md) - System design and components (to be created)
- [MCP Server Guide](mcp-server-guide.md) - How to use and create MCP servers (to be created)
- [Agent Development](agent-development.md) - Building and extending agents (to be created)

## Documentation Structure

### Core Documentation
- **context.md** - Living document tracking decisions, sessions, and context
- **architecture.md** - System architecture and design patterns
- **getting-started.md** - Onboarding guide for new contributors

### Technical Documentation
- **mcp-server-guide.md** - MCP server integration guide
- **agent-development.md** - Agent development guide
- **api-reference.md** - API documentation
- **configuration.md** - Configuration options

### Guides & Tutorials
- **workflow-guide.md** - Common workflows and processes
- **testing-guide.md** - Testing strategies
- **deployment-guide.md** - Deployment instructions
- **troubleshooting.md** - Common issues and solutions

### Design Documents
- **adr/** - Architecture Decision Records
- **rfcs/** - Request for Comments
- **design-docs/** - Detailed design documents

## Contributing to Documentation

### Style Guide
- Use Markdown format
- Include code examples where helpful
- Keep language clear and concise
- Update table of contents
- Link to related documents

### Documentation Standards
1. **Headers**: Use ## for main sections, ### for subsections
2. **Code blocks**: Always specify language for syntax highlighting
3. **Links**: Use relative links for internal documents
4. **Images**: Store in `/docs/images` directory
5. **Examples**: Provide working examples

### Document Template

```markdown
# Document Title

Brief description of what this document covers.

## Table of Contents
- [Section 1](#section-1)
- [Section 2](#section-2)

## Section 1

Content here...

### Subsection

More details...

## Examples

\`\`\`javascript
// Code example
\`\`\`

## See Also
- [Related Doc](link.md)
```

## Documentation Types

### Architecture Decision Records (ADRs)
Track important architectural decisions:
- **Status**: Proposed, Accepted, Deprecated, Superseded
- **Context**: Why the decision was needed
- **Decision**: What was decided
- **Consequences**: Impact of the decision

### RFCs (Request for Comments)
Propose significant changes:
- **Summary**: Brief overview
- **Motivation**: Why this change
- **Detailed Design**: How it will work
- **Alternatives**: Other options considered
- **Open Questions**: Unresolved issues

### Design Documents
Detailed technical designs:
- **Overview**: High-level description
- **Goals**: What we're trying to achieve
- **Non-Goals**: What's out of scope
- **Design**: Detailed design
- **Implementation**: Implementation notes

## Maintaining Documentation

### Regular Updates
- Review documentation quarterly
- Update after major changes
- Archive obsolete documents
- Track version changes

### Documentation Checklist
When updating code:
- [ ] Update relevant documentation
- [ ] Add/update code examples
- [ ] Update API references
- [ ] Check for broken links
- [ ] Update context.md if needed

## Tools

### Documentation Generation
- JSDoc for code documentation
- Markdown for manual docs
- Diagrams using Mermaid or PlantUML

### Documentation Testing
- Link checking: `markdown-link-check`
- Spell checking: `cspell`
- Linting: `markdownlint`

## Documentation Organization

```
/docs
  README.md                 - This file
  context.md               - Living context document
  architecture.md          - System architecture
  getting-started.md       - Onboarding guide
  /guides                  - How-to guides
  /reference               - API and technical reference
  /adr                     - Architecture Decision Records
  /rfcs                    - Request for Comments
  /images                  - Screenshots and diagrams
  /examples                - Code examples
```

## Resources

### External Resources
- [MCP Documentation](https://modelcontextprotocol.io/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [n8n Documentation](https://docs.n8n.io/)

### Related Projects
- [Puppeteer MCP Server](https://github.com/modelcontextprotocol/servers)
- [GGWave](https://github.com/ggerganov/ggwave)

---

## Getting Help

- Check existing documentation first
- Search GitHub issues
- Ask in GitHub Discussions
- Review context.md for historical decisions

---

*For contribution guidelines, see the main [README.md](../README.md).*
