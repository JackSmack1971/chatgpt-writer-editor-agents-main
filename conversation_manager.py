from typing import Any, List, Dict

class ConversationManager:
    """
    Orchestrates multi-agent conversations, manages conversation flows, sessions, and persistent logging.
    All state is instance-based.
    """

    def __init__(self, chatbots: List[Any]):
        """
        Args:
            chatbots: List of Chatbot instances.
        """
        self.chatbots = chatbots
        self.sessions: Dict[str, Any] = {}
        self.log: List[Any] = []

    async def start_conversation(self, session_id: str, user: str, message: str) -> Any:
        """
        Starts a conversation session, routes messages to chatbots, and logs responses.
        Args:
            session_id: Unique identifier for the conversation session.
            user: The user initiating the conversation.
            message: The message content.
        Returns:
            The session's conversation data.
        """
        pass

    def get_log(self) -> Any:
        """
        Returns the persistent conversation log.
        Returns:
            The log data.
        """
        return self.log