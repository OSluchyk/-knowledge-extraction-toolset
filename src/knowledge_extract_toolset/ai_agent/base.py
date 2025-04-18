"""
Base classes for AI agents in the Knowledge Extract Toolset.

This module defines the abstract base classes and interfaces for AI agents.
"""

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Dict, Any, List, Optional, Type

from .config import AiAgentConfig


class AgentType(Enum):
    """Enum for different types of AI agents."""
    KNOWLEDGE_EXTRACTION = auto()
    SUMMARIZATION = auto()
    QUESTION_ANSWERING = auto()
    CUSTOM = auto()

    @classmethod
    def from_string(cls, agent_type_str: str) -> 'AgentType':
        """Convert a string to an AgentType.

        Args:
            agent_type_str (str): The string representation of the agent type

        Returns:
            AgentType: The corresponding AgentType enum value

        Raises:
            ValueError: If the string does not match any AgentType
        """
        type_map = {
            "knowledge_extraction": cls.KNOWLEDGE_EXTRACTION,
            "summarization": cls.SUMMARIZATION,
            "question_answering": cls.QUESTION_ANSWERING,
            "custom": cls.CUSTOM
        }
        
        agent_type_str = agent_type_str.lower()
        if agent_type_str not in type_map:
            raise ValueError(f"Unknown agent type: {agent_type_str}")
        
        return type_map[agent_type_str]


class AiAgent(ABC):
    """Abstract base class for AI agents."""

    def __init__(self, config: AiAgentConfig):
        """Initialize the AI agent with a configuration.

        Args:
            config (AiAgentConfig): The configuration for the agent
        """
        self.config = config

    @abstractmethod
    def process(self, text: str, **kwargs) -> Any:
        """Process text using the AI agent.

        Args:
            text (str): The text to process
            **kwargs: Additional parameters for processing

        Returns:
            Any: The result of processing the text
        """
        pass


class AiAgentFactory:
    """Factory for creating AI agents."""

    _agent_classes: Dict[AgentType, Type[AiAgent]] = {}

    @classmethod
    def register_agent(cls, agent_type: AgentType, agent_class: Type[AiAgent]) -> None:
        """Register an agent class for a specific agent type.

        Args:
            agent_type (AgentType): The type of agent
            agent_class (Type[AiAgent]): The agent class to register
        """
        cls._agent_classes[agent_type] = agent_class

    @classmethod
    def create_agent(cls, agent_type: AgentType, config: AiAgentConfig) -> AiAgent:
        """Create an agent of the specified type with the given configuration.

        Args:
            agent_type (AgentType): The type of agent to create
            config (AiAgentConfig): The configuration for the agent

        Returns:
            AiAgent: The created agent

        Raises:
            ValueError: If the agent type is not registered
        """
        if agent_type not in cls._agent_classes:
            raise ValueError(f"No agent class registered for type: {agent_type}")
        
        agent_class = cls._agent_classes[agent_type]
        return agent_class(config)