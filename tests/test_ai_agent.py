"""
Tests for the AI Agent functionality in the Knowledge Extract Toolset.

This module contains tests for the AI Agent classes and functionality.
"""

import unittest
import os
from unittest.mock import patch, MagicMock

from knowledge_extract_toolset.ai_agent import (
    AiAgent, AiAgentFactory, AgentType, AiAgentConfig, load_agent_config
)
from knowledge_extract_toolset.ai_agent.providers import (
    ModelProvider, ModelProviderFactory, ProviderType
)


class TestAiAgentConfig(unittest.TestCase):
    """Tests for the AiAgentConfig class."""

    def test_from_dict(self):
        """Test creating an AiAgentConfig from a dictionary."""
        config_dict = {
            "name": "Test Agent",
            "description": "A test agent",
            "agent_type": "knowledge_extraction",
            "model_provider": "openai",
            "model_name": "gpt-3.5-turbo",
            "temperature": 0.5,
            "max_tokens": 1000,
            "prompt_template": "Test template",
            "prompt_variables": ["var1", "var2"],
            "provider_config": {
                "api_key": "test_key"
            }
        }
        
        config = AiAgentConfig.from_dict(config_dict)
        
        self.assertEqual(config.name, "Test Agent")
        self.assertEqual(config.description, "A test agent")
        self.assertEqual(config.agent_type, "knowledge_extraction")
        self.assertEqual(config.model_provider, "openai")
        self.assertEqual(config.model_name, "gpt-3.5-turbo")
        self.assertEqual(config.temperature, 0.5)
        self.assertEqual(config.max_tokens, 1000)
        self.assertEqual(config.prompt_template, "Test template")
        self.assertEqual(config.prompt_variables, ["var1", "var2"])
        self.assertEqual(config.provider_config, {"api_key": "test_key"})


class TestAgentType(unittest.TestCase):
    """Tests for the AgentType enum."""

    def test_from_string(self):
        """Test converting a string to an AgentType."""
        self.assertEqual(AgentType.from_string("knowledge_extraction"), AgentType.KNOWLEDGE_EXTRACTION)
        self.assertEqual(AgentType.from_string("summarization"), AgentType.SUMMARIZATION)
        self.assertEqual(AgentType.from_string("question_answering"), AgentType.QUESTION_ANSWERING)
        self.assertEqual(AgentType.from_string("custom"), AgentType.CUSTOM)
        
        with self.assertRaises(ValueError):
            AgentType.from_string("invalid_type")


class TestProviderType(unittest.TestCase):
    """Tests for the ProviderType enum."""

    def test_from_string(self):
        """Test converting a string to a ProviderType."""
        self.assertEqual(ProviderType.from_string("openai"), ProviderType.OPENAI)
        self.assertEqual(ProviderType.from_string("gemini"), ProviderType.GEMINI)
        self.assertEqual(ProviderType.from_string("custom"), ProviderType.CUSTOM)
        
        with self.assertRaises(ValueError):
            ProviderType.from_string("invalid_type")


class MockModelProvider(ModelProvider):
    """Mock model provider for testing."""
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using the model."""
        return f"Generated text for prompt: {prompt}"
    
    def generate_chat_response(self, messages, **kwargs) -> str:
        """Generate a response in a chat context."""
        return f"Generated response for {len(messages)} messages"


class MockAiAgent(AiAgent):
    """Mock AI agent for testing."""
    
    def __init__(self, config: AiAgentConfig):
        """Initialize the mock agent."""
        super().__init__(config)
        self.provider = MockModelProvider({"api_key": "test_key"})
    
    def process(self, text: str, **kwargs):
        """Process text using the AI agent."""
        return {"result": f"Processed: {text[:20]}..."}


class TestAiAgentFactory(unittest.TestCase):
    """Tests for the AiAgentFactory class."""
    
    def setUp(self):
        """Set up the test."""
        # Register the mock agent
        AiAgentFactory.register_agent(AgentType.CUSTOM, MockAiAgent)
    
    def test_create_agent(self):
        """Test creating an agent using the factory."""
        config = AiAgentConfig(
            name="Test Agent",
            description="A test agent",
            agent_type="custom",
            model_provider="openai",
            model_name="gpt-3.5-turbo",
            temperature=0.5,
            max_tokens=1000,
            prompt_template="Test template",
            prompt_variables=["var1", "var2"],
            provider_config={"api_key": "test_key"}
        )
        
        agent = AiAgentFactory.create_agent(AgentType.CUSTOM, config)
        
        self.assertIsInstance(agent, MockAiAgent)
        self.assertEqual(agent.config, config)
        
        # Test processing
        result = agent.process("This is a test text")
        self.assertEqual(result, {"result": "Processed: This is a test text..."})


class TestModelProviderFactory(unittest.TestCase):
    """Tests for the ModelProviderFactory class."""
    
    def setUp(self):
        """Set up the test."""
        # Register the mock provider
        ModelProviderFactory.register_provider(ProviderType.CUSTOM, MockModelProvider)
    
    def test_create_provider(self):
        """Test creating a provider using the factory."""
        config = {"api_key": "test_key"}
        
        provider = ModelProviderFactory.create_provider(ProviderType.CUSTOM, config)
        
        self.assertIsInstance(provider, MockModelProvider)
        self.assertEqual(provider.config, config)
        
        # Test generating text
        text = provider.generate_text("Test prompt")
        self.assertEqual(text, "Generated text for prompt: Test prompt")
        
        # Test generating chat response
        response = provider.generate_chat_response([{"role": "user", "content": "Hello"}])
        self.assertEqual(response, "Generated response for 1 messages")


if __name__ == "__main__":
    unittest.main()