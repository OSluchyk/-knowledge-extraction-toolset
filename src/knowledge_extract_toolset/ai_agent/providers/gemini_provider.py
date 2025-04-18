"""
Gemini model provider for the Knowledge Extract Toolset.

This module implements the Gemini model provider for generating text and chat responses
using Google's Generative AI API.
"""

from typing import Dict, Any, List, Optional

try:
    import google.generativeai as genai
except ImportError:
    raise ImportError(
        "google-generativeai is required for Gemini model provider support. "
        "Install it with: pip install google-generativeai"
    )

from .base import ModelProvider, ProviderType, ModelProviderFactory


class GeminiProvider(ModelProvider):
    """Gemini model provider implementation."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the Gemini provider with a configuration.

        Args:
            config (Dict[str, Any]): The configuration for the provider
        """
        super().__init__(config)
        
        # Set up the Gemini client
        api_key = config.get("api_key")
        if not api_key:
            raise ValueError("Gemini API key is required")
        
        genai.configure(api_key=api_key)
        self.model = config.get("model", "gemini-pro")
        self.temperature = float(config.get("temperature", 0.7))
        self.max_tokens = config.get("max_tokens")
        
        # Create the model
        generation_config = {
            "temperature": self.temperature,
        }
        if self.max_tokens:
            generation_config["max_output_tokens"] = self.max_tokens
            
        self.genai_model = genai.GenerativeModel(
            model_name=self.model,
            generation_config=generation_config
        )

    def generate_text(self, prompt: str, **kwargs) -> str:
        """Generate text using the Gemini model.

        Args:
            prompt (str): The prompt to generate text from
            **kwargs: Additional parameters for text generation

        Returns:
            str: The generated text
        """
        # Override configuration with kwargs if provided
        temperature = kwargs.get("temperature", self.temperature)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        
        # Update generation config if needed
        generation_config = {"temperature": temperature}
        if max_tokens:
            generation_config["max_output_tokens"] = max_tokens
        
        # Generate text
        response = self.genai_model.generate_content(
            prompt,
            generation_config=generation_config
        )
        
        # Extract and return the generated text
        return response.text

    def generate_chat_response(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a response in a chat context using the Gemini model.

        Args:
            messages (List[Dict[str, str]]): The chat messages, each with 'role' and 'content' keys
            **kwargs: Additional parameters for response generation

        Returns:
            str: The generated response
        """
        # Override configuration with kwargs if provided
        temperature = kwargs.get("temperature", self.temperature)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        
        # Update generation config if needed
        generation_config = {"temperature": temperature}
        if max_tokens:
            generation_config["max_output_tokens"] = max_tokens
        
        # Create a chat session
        chat = self.genai_model.start_chat()
        
        # Convert messages to Gemini format and add them to the chat
        for message in messages:
            role = message["role"]
            content = message["content"]
            
            # Add message to chat history without generating a response
            if role == "user":
                chat.history.append({"role": "user", "parts": [content]})
            elif role == "assistant":
                chat.history.append({"role": "model", "parts": [content]})
            elif role == "system":
                # Gemini doesn't have a system role, so we'll add it as a user message
                # at the beginning of the conversation
                if len(chat.history) == 0:
                    chat.history.append({"role": "user", "parts": [f"System instruction: {content}"]})
        
        # Generate a response to the last user message
        response = chat.send_message(
            messages[-1]["content"] if messages[-1]["role"] == "user" else "",
            generation_config=generation_config
        )
        
        # Extract and return the generated text
        return response.text


# Register the Gemini provider with the factory
ModelProviderFactory.register_provider(ProviderType.GEMINI, GeminiProvider)