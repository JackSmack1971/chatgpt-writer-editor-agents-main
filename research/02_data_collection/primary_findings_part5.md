# Primary Findings (Part 5)
**Source:** Context7 MCP, official LangChain documentation ([/langchain-ai/langchain](https://github.com/langchain-ai/langchain))

## Best Practices for Robust and Portable Async Testing with API Mocks

### 1. Async Test Patterns

- **Async Test Functions:** Use `async def` test functions and `await` for testing asynchronous LLM and tool calls.
  ```python
  async def test_async_llm():
      result = await llm.ainvoke("test input")
      assert "expected" in result
  ```

- **Async Streaming and Batch:** Test async streaming (`astream`) and batch processing (`abatch`) for LLMs and tools.
  ```python
  async for token in llm.astream("hello"):
      print(token)
  await llm.abatch(["input1", "input2"])
  ```

### 2. Mocking and Simulating API Errors

- **Mocking with `unittest.mock`:** Use `patch` to simulate API errors (e.g., rate limits) and test error handling logic.
  ```python
  from unittest.mock import patch
  from openai import RateLimitError

  with patch("openai.ChatCompletion.create", side_effect=RateLimitError("rate limit")):
      # Test code that should handle the rate limit error
  ```

- **Fake LLMs:** Use fake or mock LLM classes (e.g., `FakeListLLM`) for deterministic, offline testing.
  ```python
  from langchain_community.llms.fake import FakeListLLM
  ```

### 3. Mocking Time and Environment

- **Mocking Time:** Use utilities like `mock_now` to simulate time-dependent behavior in tests.
  ```python
  from langchain_core.utils import mock_now

  with mock_now(tomorrow):
      # Test code that depends on the current time
  ```

- **Mocking Environment Variables:** Set environment variables in test setup for API keys and configuration.
  ```python
  import os
  os.environ["OPENAI_API_KEY"] = "test-key"
  ```

### 4. Integration with Pytest

- **Standard and Integration Tests:** Use `pytest` for both unit and integration tests. Mark tests that require external APIs as integration tests.
  ```bash
  make tests           # Run unit tests
  make integration_tests  # Run integration tests
  ```

- **Async Fixtures:** Use pytest-asyncio for async fixtures and test functions.

### 5. Testing Custom and Async Tools

- **Async Tool Testing:** Test custom async tools with `@tool` decorator and async implementations.
  ```python
  from langchain_core.tools import tool

  @tool
  async def amultiply(a: int, b: int) -> int:
      return a * b
  ```

- **Async Document Loaders:** Test async document loaders and other async components in isolation.

### 6. Practical Recommendations

- **Use async test functions and pytest-asyncio for all async code.**
- **Mock API calls and errors for robust, offline, and deterministic tests.**
- **Test both streaming and batch async behaviors.**
- **Mock time and environment for reproducible tests.**
- **Separate unit and integration tests for maintainability and CI/CD.**

---

**References:**
- LangChain official documentation and code examples ([/langchain-ai/langchain](https://github.com/langchain-ai/langchain))
- See code snippets in this file for implementation details.