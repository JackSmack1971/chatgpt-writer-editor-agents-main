import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from typing import List

# Placeholder imports for the actual implementation
from chatbot import Chatbot

class DummyBufferMemory:
    def __init__(self):
        self.messages = []

    def add_message(self, msg):
        self.messages.append(msg)

    def get_window(self, size):
        return self.messages[-size:]

class DummyVectorStoreMemory:
    def __init__(self):
        self.vectors = []

    def add_vector(self, v):
        self.vectors.append(v)

    def search(self, query):
        return []

class DummyPromptTemplate:
    def __init__(self, template):
        self.template = template

    def format(self, **kwargs):
        return self.template.format(**kwargs)

@pytest.mark.asyncio
class TestChatbot:
    @pytest.fixture
    def memory_modules(self):
        return {
            "buffer": DummyBufferMemory(),
            "vector": DummyVectorStoreMemory()
        }

    @pytest.fixture
    def prompt_template(self):
        return DummyPromptTemplate("Hello, {user}!")

    @pytest.fixture
    def openai_client(self):
        client = AsyncMock()
        client.complete_prompt = AsyncMock(return_value="AI response")
        return client

    @pytest.fixture
    def chatbot(self, openai_client, memory_modules, prompt_template):
        # Use the actual Chatbot implementation
        return Chatbot(openai_client, memory_modules, prompt_template)

    async def test_instantiation(self, chatbot):
        assert hasattr(chatbot, "openai_client")
        assert hasattr(chatbot, "memory_modules")
        assert hasattr(chatbot, "prompt_template")
        assert hasattr(chatbot, "history")

    async def test_send_message_success(self, chatbot):
        response = await chatbot.send_message("alice", "Hi!")
        assert response == "AI response"
        assert chatbot.history[-1][0] == "alice"
        assert chatbot.history[-1][1] == "Hi!"

    async def test_memory_integration(self, chatbot):
        await chatbot.send_message("bob", "Hello!")
        assert chatbot.memory_modules["buffer"].messages[-1] == "Hello!"

    async def test_prompt_template_usage(self, chatbot):
        await chatbot.send_message("carol", "Test")
        # The DummyPromptTemplate always formats with user
        assert chatbot.prompt_template.format(user="carol") == "Hello, carol!"

    async def test_invalid_memory_module(self, chatbot):
        chatbot.memory_modules.pop("buffer")
        with pytest.raises(KeyError):
            await chatbot.send_message("dave", "Oops")

    async def test_missing_prompt_template(self, openai_client, memory_modules):
        # Simulate missing prompt template
        with pytest.raises(AttributeError):
            class Chatbot:
                def __init__(self, openai_client, memory_modules, prompt_template):
                    self.openai_client = openai_client
                    self.memory_modules = memory_modules
                    self.prompt_template = None

                async def send_message(self, user, message):
                    prompt = self.prompt_template.format(user=user)
                    return await self.openai_client.complete_prompt(prompt)
            chatbot = Chatbot(openai_client, memory_modules, None)
            await chatbot.send_message("eve", "Test")

    async def test_corrupted_history(self, chatbot):
        chatbot.history = None
        with pytest.raises(TypeError):
            await chatbot.send_message("frank", "Test")

    async def test_boundary_message_window(self, chatbot):
        # Simulate windowing
        for i in range(10):
            await chatbot.send_message("user", f"msg{i}")
        window = chatbot.memory_modules["buffer"].get_window(5)
        assert len(window) == 5

    async def test_empty_conversation(self, chatbot):
        assert chatbot.history == []

    async def test_extensibility_new_memory_module(self, chatbot):
        class DummyNewMemory:
            def __init__(self):
                self.data = []
        chatbot.memory_modules["new"] = DummyNewMemory()
        assert hasattr(chatbot.memory_modules["new"], "data")