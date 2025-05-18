# Primary Findings (Part 3)
**Source:** Context7 MCP, official LangChain documentation ([/langchain-ai/langchain](https://github.com/langchain-ai/langchain))

## Best Practices for Abstraction of Agent Prompts for Reuse and Experimentation

### 1. Modular Prompt Templates

- **PromptTemplate and ChatPromptTemplate:** Use these classes to define modular, parameterized prompts. Templates can include placeholders for dynamic variables (e.g., `{question}`, `{input}`, `{history}`), supporting easy reuse and adaptation.
  ```python
  from langchain_core.prompts import PromptTemplate
  template = "Question: {question}\nAnswer: Let's think step by step."
  prompt = PromptTemplate.from_template(template)
  ```

- **ChatPromptTemplate:** Supports multi-message prompts (system, human, AI), enabling richer conversational context and role separation.
  ```python
  from langchain_core.prompts import ChatPromptTemplate
  prompt = ChatPromptTemplate.from_messages([
      ("system", "You are a helpful assistant."),
      ("human", "{input}"),
  ])
  ```

### 2. Partial Formatting and Dynamic Variables

- **Partial Variables:** Templates can be partially formatted with fixed or function-based values, allowing for flexible prompt composition and reuse.
  ```python
  prompt = PromptTemplate(
      template="{foo}{bar}", input_variables=["bar"], partial_variables={"foo": "foo"}
  )
  print(prompt.format(bar="baz"))  # Output: "foobaz"
  ```

- **Function-Based Partials:** Use functions (e.g., for timestamps) as partial variables for dynamic prompt content.

### 3. Few-Shot and Example-Based Prompts

- **FewShotPromptTemplate:** Assemble prompts with dynamic or static few-shot examples, supporting experimentation with different prompt strategies.
  ```python
  from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
  example_prompt = PromptTemplate.from_template("Input: {input} -> Output: {output}")
  prompt = FewShotPromptTemplate(
      examples=examples,
      example_prompt=example_prompt,
      prefix="Translate the following words from English to Italian:",
      suffix="Input: {input} -> Output:",
      input_variables=["input"],
  )
  ```

- **Semantic Example Selection:** Use semantic similarity selectors to dynamically choose relevant examples for each prompt invocation.

### 4. Pipeline and Composite Prompts

- **PipelinePromptTemplate:** Compose complex prompts from multiple modular sub-templates, supporting advanced experimentation and reuse.
  ```python
  from langchain_core.prompts import PipelinePromptTemplate, PromptTemplate
  # Define sub-templates and assemble into a pipeline
  ```

### 5. Custom and Extensible Prompt Classes

- **CustomPromptTemplate:** Implement custom prompt classes for advanced use cases (e.g., tool retrieval, memory integration, agent scratchpads).
  ```python
  class CustomPromptTemplate(StringPromptTemplate):
      ...
      def format(self, **kwargs) -> str:
          # Custom formatting logic
          ...
  ```

### 6. Chaining and Experimentation

- **Prompt Chaining:** Chain prompt templates with models or other components for flexible experimentation and rapid prototyping.
  ```python
  chain = prompt | llm
  response = chain.invoke({"input": "Translate this to German."})
  ```

### 7. Practical Recommendations

- **Define all agent prompts as modular templates with clear variable names.**
- **Use partial formatting and function-based variables for flexibility.**
- **Leverage few-shot and pipeline templates for experimentation.**
- **Keep prompt logic decoupled from agent logic for maximum reusability.**
- **Document prompt templates and their intended use cases for maintainability.**

---

**References:**
- LangChain official documentation and code examples ([/langchain-ai/langchain](https://github.com/langchain-ai/langchain))
- See code snippets in this file for implementation details.