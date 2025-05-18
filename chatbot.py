from typing import Any, Dict, List, Optional

class Chatbot:
    """
    Encapsulates agent logic, manages conversation history, and interfaces with memory modules and prompt templates.
    All state is instance-based. Supports async message sending.
    """

    def __init__(
        self,
        openai_client: Any,
        memory_modules: Dict[str, Any],
        prompt_template: Any,
    ):
        """
        Args:
            openai_client: Instance of OpenAIClient or compatible async client.
            memory_modules: Dict of memory modules (e.g., buffer, vector).
            prompt_template: Prompt template object with a .format(**kwargs) method.
        """
        self.openai_client = openai_client
        self.memory_modules = memory_modules
        self.prompt_template = prompt_template
        self.history: Optional[List[Any]] = []

    async def send_message(self, user: str, message: str) -> Any:
        """
        Sends a message as the agent, updates memory and history, and returns the response.
        Args:
            user: The user sending the message.
            message: The message content.
        Returns:
            The response from the agent (e.g., OpenAI completion).
        """
        if self.history is None:
            raise TypeError("Conversation history is corrupted (None).")
        prompt = self.prompt_template.format(user=user)
        response = await self.openai_client.complete_prompt(prompt)
        self.memory_modules["buffer"].add_message(message)
        self.history.append((user, message, response))
        return response