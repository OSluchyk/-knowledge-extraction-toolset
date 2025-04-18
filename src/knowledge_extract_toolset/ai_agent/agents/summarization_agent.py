"""
Summarization agent for the Knowledge Extract Toolset.

This module implements an AI agent for summarizing text.
"""

from typing import Dict, Any, List, Optional

from ..base import AiAgent, AgentType, AiAgentFactory
from ..config import AiAgentConfig
from ..providers import ModelProviderFactory, ProviderType


class SummarizationAgent(AiAgent):
    """AI agent for summarizing text."""

    def __init__(self, config: AiAgentConfig):
        """Initialize the summarization agent.

        Args:
            config (AiAgentConfig): The configuration for the agent
        """
        super().__init__(config)
        
        # Create the model provider
        provider_type = ProviderType.from_string(config.model_provider)
        provider_config = {
            "api_key": config.provider_config.get("api_key"),
            "model": config.model_name,
            "temperature": config.temperature,
            "max_tokens": config.max_tokens
        }
        self.provider = ModelProviderFactory.create_provider(provider_type, provider_config)

    def process(self, text: str, **kwargs) -> Dict[str, Any]:
        """Summarize text.

        Args:
            text (str): The text to summarize
            **kwargs: Additional parameters for summarization

        Returns:
            Dict[str, Any]: The summarization result
        """
        # Get parameters from kwargs
        length = kwargs.get("length", "medium")  # short, medium, long
        focus = kwargs.get("focus", "general")  # general, technical, simplified, etc.
        
        # Create the prompt by replacing variables in the template
        prompt = self._create_prompt(text, length, focus)
        
        # Generate the response
        response = self.provider.generate_text(prompt)
        
        # Return the summarization result
        return {
            "summary": response,
            "original_length": len(text),
            "summary_length": len(response),
            "reduction_percentage": round((1 - len(response) / len(text)) * 100, 2) if len(text) > 0 else 0
        }

    def _create_prompt(self, text: str, length: str, focus: str) -> str:
        """Create a prompt for summarization.

        Args:
            text (str): The text to summarize
            length (str): The desired length of the summary (short, medium, long)
            focus (str): The focus of the summary (general, technical, simplified, etc.)

        Returns:
            str: The prompt for the model
        """
        # Get the prompt template from the configuration
        template = self.config.prompt_template
        
        # Replace variables in the template
        prompt = template.replace("{text}", text)
        prompt = prompt.replace("{length}", length)
        prompt = prompt.replace("{focus}", focus)
        
        # Replace any other variables from the configuration
        if self.config.prompt_variables:
            for var in self.config.prompt_variables:
                if var in self.config.provider_config:
                    prompt = prompt.replace(f"{{{var}}}", str(self.config.provider_config[var]))
        
        return prompt


# Register the agent with the factory
AiAgentFactory.register_agent(AgentType.SUMMARIZATION, SummarizationAgent)