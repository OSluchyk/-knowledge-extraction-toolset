"""
Base classes for model providers in the Knowledge Extract Toolset.

This module defines the abstract base classes and interfaces for model providers.
"""

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Dict, Any, Optional, Type, List


class ProviderType(Enum):
    """Enum for different types of model providers."""
    OPENAI = auto()
    GEMINI = auto()
    CUSTOM = auto()

    @classmethod
    def from_string(cls, provider_type_str: str) -> 'ProviderType':
        """Convert a string to a ProviderType.

        Args:
            provider_type_str (str): The string representation of the provider type

        Returns:
            ProviderType: The corresponding ProviderType enum value

        Raises:
            ValueError: If the string does not match any ProviderType
        """
        type_map = {
            "openai": cls.OPENAI,
            "gemini": cls.GEMINI,
            "custom": cls.CUSTOM
        }
        
        provider_type_str = provider_type_str.lower()
        if provider_type_str not in type_map:
            raise ValueError(f"Unknown provider type: {provider_type_str}")
        
        return type_map[provider_type_str]


class ModelProvider(ABC):
    """Abstract base class for model providers."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the model provider with a configuration.

        Args:
            config (Dict[str, Any]): The configuration for the provider
        """
        self.config = config

    @abstractmethod
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using the model.

        Args:
            prompt (str): The prompt to generate text from
            **kwargs: Additional parameters for text generation

        Returns:
            str: The generated text
        """
        pass

    @abstractmethod
    def generate_chat_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response in a chat context.

        Args:
            messages (List[Dict[str, str]]): The chat messages, each with 'role' and 'content' keys
            **kwargs: Additional parameters for response generation

        Returns:
            str: The generated response
        """
        pass


class ModelProviderFactory:
    """Factory for creating model providers."""

    _provider_classes: Dict[ProviderType, Type[ModelProvider]] = {}

    @classmethod
    def register_provider(cls, provider_type: ProviderType, provider_class: Type[ModelProvider]) -> None:
        """Register a provider class for a specific provider type.

        Args:
            provider_type (ProviderType): The type of provider
            provider_class (Type[ModelProvider]): The provider class to register
        """
        cls._provider_classes[provider_type] = provider_class

    @classmethod
    def create_provider(cls, provider_type: ProviderType, config: Dict[str, Any]) -> ModelProvider:
        """Create a provider of the specified type with the given configuration.

        Args:
            provider_type (ProviderType): The type of provider to create
            config (Dict[str, Any]): The configuration for the provider

        Returns:
            ModelProvider: The created provider

        Raises:
            ValueError: If the provider type is not registered
        """
        if provider_type not in cls._provider_classes:
            raise ValueError(f"No provider class registered for type: {provider_type}")
        
        provider_class = cls._provider_classes[provider_type]
        return provider_class(config)