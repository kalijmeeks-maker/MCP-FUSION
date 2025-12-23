# Tests Directory

This directory contains test files for the MCP-FUSION system.

## Structure

```
/tests
  /unit           - Unit tests for individual components
  /integration    - Integration tests for MCP servers and workflows
  /e2e            - End-to-end tests for complete workflows
  /fixtures       - Test data and fixtures
```

## Running Tests

```bash
# Run all tests
npm test

# Run unit tests only
npm run test:unit

# Run integration tests
npm run test:integration

# Run with coverage
npm run test:coverage

# Watch mode for development
npm run test:watch
```

## Writing Tests

### Unit Tests

Test individual functions and modules in isolation:

```javascript
// Example: tests/unit/agents/wealth-agent.test.js
describe("WealthAgent", () => {
  it("should analyze stock data", () => {
    // Test implementation
  });
});
```

### Integration Tests

Test interactions between components:

```javascript
// Example: tests/integration/mcp-servers/puppeteer.test.js
describe("Puppeteer MCP Integration", () => {
  it("should capture screenshot", async () => {
    // Test implementation
  });
});
```

### End-to-End Tests

Test complete user workflows:

```javascript
// Example: tests/e2e/fusion-workflow.test.js
describe("Multi-Model Fusion Workflow", () => {
  it("should complete fusion cycle", async () => {
    // Test implementation
  });
});
```

## Test Guidelines

1. **Descriptive names**: Use clear, descriptive test names
2. **Arrange-Act-Assert**: Follow AAA pattern
3. **Isolated tests**: Each test should be independent
4. **Mock external services**: Don't call real APIs in tests
5. **Fast execution**: Keep tests fast
6. **Coverage goals**: Aim for 80%+ coverage on critical paths

## Test Utilities

Common test utilities and helpers:

```javascript
// tests/utils/mocks.js
export const mockMCPServer = () => {
  /* ... */
};
export const mockAgentResponse = () => {
  /* ... */
};
```

## Fixtures

Test data should be placed in `/fixtures`:

```
/tests/fixtures
  /sample-responses
  /mock-data
  /test-configs
```

## Continuous Integration

Tests run automatically on:

- Every push to feature branches
- Pull request creation
- Before merging to main

## Debugging Tests

```bash
# Run single test file
npm test -- path/to/test.js

# Run tests matching pattern
npm test -- --grep "pattern"

# Debug mode (with Node inspector)
npm run test:debug
```

## Mock MCP Servers

For testing MCP server integrations, use mock servers:

```javascript
import { createMockMCPServer } from "./utils/mocks";

const mockServer = createMockMCPServer({
  name: "test-server",
  tools: [
    /* mock tools */
  ],
});
```

## Security Testing

Security-related tests should verify:

- No secrets in logs
- Input validation
- Permission checks
- API key handling

## Performance Testing

Performance benchmarks should be in `/tests/performance`:

```javascript
// tests/performance/orchestration-benchmark.js
describe("Orchestration Performance", () => {
  it("should handle 100 concurrent requests", async () => {
    // Benchmark implementation
  });
});
```

---

## Resources

- Testing framework documentation
- [Jest](https://jestjs.io/) or [Mocha](https://mochajs.org/)
- [Testing Best Practices](../docs/testing-guidelines.md)

---

For more information, see [/docs/context.md](../docs/context.md).
