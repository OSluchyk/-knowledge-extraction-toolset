"""
OpenAI model provider for the Knowledge Extract Toolset.

This module implements the OpenAI model provider for generating text and chat responses.
"""

from typing import Dict, Any, List, Optional

try:
    import openai
except ImportError:
    raise ImportError(
        "openai is required for OpenAI model provider support. "
        "Install it with: pip install openai"
    )

from .base import ModelProvider, ProviderType, ModelProviderFactory


class OpenAIProvider(ModelProvider):
    """OpenAI model provider implementation."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the OpenAI provider with a configuration.

        Args:
            config (Dict[str, Any]): The configuration for the provider
        """
        super().__init__(config)
        
        # Set up the OpenAI client
        api_key = config.get("api_key")
        if not api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = openai.OpenAI(api_key=api_key)
        self.model = config.get("model", "gpt-3.5-turbo")
        self.temperature = float(config.get("temperature", 0.7))
        self.max_tokens = config.get("max_tokens")

    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using the OpenAI model.

        Args:
            prompt (str): The prompt to generate text from
            **kwargs: Additional parameters for text generation

        Returns:
            str: The generated text
        """
        # Override configuration with kwargs if provided
        model = kwargs.get("model", self.model)
        temperature = kwargs.get("temperature", self.temperature)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        
        # Create a chat completion with a system message and user prompt
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Extract and return the generated text
        return response.choices[0].message.content

    def generate_chat_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response in a chat context using the OpenAI model.

        Args:
            messages (List[Dict[str, str]]): The chat messages, each with 'role' and 'content' keys
            **kwargs: Additional parameters for response generation

        Returns:
            str: The generated response
        """
        # Override configuration with kwargs if provided
        model = kwargs.get("model", self.model)
        temperature = kwargs.get("temperature", self.temperature)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        
        # Create a chat completion with the provided messages
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # Extract and return the generated text
        return response.choices[0].message.content


# Register the OpenAI provider with the factory
ModelProviderFactory.register_provider(ProviderType.OPENAI, OpenAIProvider)