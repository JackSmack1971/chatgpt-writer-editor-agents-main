# Primary Findings (Part 4)
**Source:** Context7 MCP, official LangChain documentation ([/langchain-ai/langchain](https://github.com/langchain-ai/langchain))

## Recommended Libraries and Patterns for GPT API Retries and Fallbacks

### 1. Retry Logic with `tenacity` and LangChain

- **Automatic Retries:** Use the `tenacity` library to automatically retry failed API calls on specific exceptions (e.g., rate limits, network errors, parsing errors).
  ```python
  import tenacity

  @tenacity.retry(
      stop=tenacity.stop_after_attempt(2),
      wait=tenacity.wait_none(),
      retry=tenacity.retry_if_exception_type(ValueError),
      before_sleep=lambda retry_state: print(
          f"ValueError occurred: {retry_state.outcome.exception()}, retrying..."
      ),
      retry_error_callback=lambda retry_state: 0,
  )
  def ask_for_bid(agent) -> str:
      bid_string = agent.bid()
      bid = int(bid_parser.parse(bid_string)["bid"])
      return bid
  ```

- **LangChain `with_retry`:** Use `.with_retry()` on runnables for built-in retry support.
  ```python
  from langchain_core.runnables import RunnableLambda

  chain = RunnableLambda(func).with_retry(stop_after_attempt=2)
  chain.invoke(2)
  ```

### 2. Fallback Chains and Model Fallbacks

- **Fallback Chains:** Use `.with_fallbacks()` to specify alternative chains or models to use if the primary chain fails.
  ```python
  chain_with_fallback = chain.with_fallbacks([better_chain])
  ```

- **Model Fallbacks:** Configure multiple models (e.g., GPT-3.5, GPT-4) with fallbacks for improved reliability and output quality.
  ```python
  openai_llm = ChatOpenAI(model="gpt-4o-mini", max_retries=0)
  anthropic_llm = ChatAnthropic(model="claude-3-haiku-20240307")
  llm = openai_llm.with_fallbacks([anthropic_llm])
  ```

### 3. Exception Handling and Self-Correcting Chains

- **Custom Exception Handling:** Implement custom exception classes and error handlers to provide informative error messages and guide self-correction.
  ```python
  class CustomToolException(Exception):
      ...
  def tool_custom_exception(msg, config):
      try:
          return complex_tool.invoke(msg.tool_calls[0]["args"], config=config)
      except Exception as e:
          raise CustomToolException(msg.tool_calls[0], e)
  ```

- **Self-Correcting Chains:** Retry failed tool calls with error context, allowing the model to correct its behavior.
  ```python
  self_correcting_chain = chain.with_fallbacks(
      [exception_to_messages | chain], exception_key="exception"
  )
  ```

### 4. Error Handling in Testing

- **Mocking Errors:** Use `unittest.mock` and custom error classes to simulate API errors (e.g., rate limits) for robust testing.
  ```python
  from unittest.mock import patch
  from openai import RateLimitError
  ```

### 5. Try/Except Patterns

- **Synchronous and Asynchronous Error Handling:** Use try/except blocks to catch and handle errors in both sync and async API calls.
  ```python
  try:
      response = llm.invoke(prompt)
  except Exception as e:
      print(f"Error invoking LLM: {e}")
  ```

### 6. Practical Recommendations

- **Use `tenacity` or LangChain's built-in retry/fallbacks for all OpenAI API calls.**
- **Implement custom exception handling for tool and output parsing errors.**
- **Test error handling logic with mocks and simulated failures.**
- **Document retry and fallback strategies for maintainability and compliance.**

---

**References:**
- LangChain official documentation and code examples ([/langchain-ai/langchain](https://github.com/langchain-ai/langchain))
- See code snippets in this file for implementation details.