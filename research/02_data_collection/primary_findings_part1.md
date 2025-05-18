# Primary Findings (Part 1)
**Source:** Context7 MCP, official LangChain documentation ([/langchain-ai/langchain](https://github.com/langchain-ai/langchain))

## Best Practices for Modeling AI Agents with Behavior and Memory in Python

### 1. Modular Object-Oriented Design

- **Agent as a State Graph:** Modern agent systems (e.g., LangChain) use a modular state graph, where each node represents a functional component (e.g., memory loading, agent reasoning, tool execution). This enables clear separation of concerns and extensibility.
- **Class Structure:** Core classes include `Agent`, `AgentExecutor`, `State`, and memory-related classes (e.g., `MemorySaver`, `InMemoryVectorStore`, `ConversationBufferMemory`). Each class has a single responsibility, supporting the SRP principle.
- **Tool Integration:** Tools (e.g., search, summarization) are modular and can be bound to agents via a tools list, supporting flexible agent capabilities.

### 2. Memory Modeling Patterns

- **Buffer Memory:** Use `ConversationBufferMemory` or `InMemoryChatMessageHistory` to store recent conversation history for context-aware responses.
- **Vector Store Memory:** For long-term or semantic memory, use vector stores (e.g., `InMemoryVectorStore` with OpenAI embeddings) to persist and retrieve relevant memories based on similarity search.
- **Knowledge Triples:** Store structured memories as (subject, predicate, object) triples for richer context and reasoning.
- **Memory Checkpointing:** Use `MemorySaver` or similar checkpointing to persist agent state across sessions or threads.

### 3. Prompt Abstraction and Extensibility

- **Prompt Templates:** Define prompt templates that include explicit memory usage instructions and placeholders for dynamic content (e.g., `{recall_memories}`, `{messages}`).
- **Memory Usage Guidelines:** Prompts should instruct the agent to actively use memory tools, reflect on past interactions, and update its mental model of the user.
- **Separation of Prompts and Logic:** Keep prompt templates and agent logic decoupled to enable easy experimentation and reuse.

### 4. Key Code Patterns

- **Agent Initialization:**
  ```python
  from langchain_openai import ChatOpenAI
  model = ChatOpenAI(model="gpt-4")
  agent = create_react_agent(model, tools, prompt)
  agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory)
  ```
- **State Graph Construction:**
  ```python
  builder = StateGraph(State)
  builder.add_node(load_memories)
  builder.add_node(agent)
  builder.add_node("tools", ToolNode(tools))
  builder.add_edge(START, "load_memories")
  builder.add_edge("load_memories", "agent")
  builder.add_conditional_edges("agent", route_tools, ["tools", END])
  builder.add_edge("tools", "agent")
  memory = MemorySaver()
  graph = builder.compile(checkpointer=memory)
  ```
- **Memory Tool Example:**
  ```python
  @tool
  def save_recall_memory(memory: str, config: RunnableConfig) -> str:
      # Save memory to vectorstore for later semantic retrieval
      ...
  ```

### 5. Extensibility and Multi-Agent Support

- **Session/Thread Config:** Use session or thread IDs in memory and agent configuration to support multiple concurrent conversations.
- **Graph-Based Topologies:** The state graph approach allows for non-linear conversation flows and easy extension to multi-agent or group conversations.

### 6. Visualization and Debugging

- **Graph Visualization:** Use tools like `networkx` and `matplotlib` to visualize agent memory graphs for debugging and analysis.

---

**References:**
- LangChain official documentation and code examples ([/langchain-ai/langchain](https://github.com/langchain-ai/langchain))
- See code snippets in this file for implementation details.