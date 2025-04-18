"""
Knowledge extraction agent for the Knowledge Extract Toolset.

This module implements an AI agent for extracting structured knowledge from text.
"""

from typing import Dict, Any, List, Optional

from ..base import AiAgent, AgentType, AiAgentFactory
from ..config import AiAgentConfig
from ..providers import ModelProviderFactory, ProviderType


class KnowledgeExtractionAgent(AiAgent):
    """AI agent for extracting structured knowledge from text."""

    def __init__(self, config: AiAgentConfig):
        """Initialize the knowledge extraction agent.

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
        """Extract structured knowledge from text.

        Args:
            text (str): The text to extract knowledge from
            **kwargs: Additional parameters for knowledge extraction

        Returns:
            Dict[str, Any]: The extracted knowledge as a structured dictionary
        """
        # Get format from kwargs or default to JSON
        output_format = kwargs.get("output_format", "json")
        
        # Create the prompt by replacing variables in the template
        prompt = self._create_prompt(text, output_format)
        
        # Generate the response
        response = self.provider.generate_text(prompt)
        
        # Parse the response based on the output format
        if output_format == "json":
            # Try to parse the response as JSON
            try:
                import json
                # Find JSON content between triple backticks if present
                if "```json" in response and "```" in response.split("```json", 1)[1]:
                    json_str = response.split("```json", 1)[1].split("```", 1)[0].strip()
                    return json.loads(json_str)
                # Otherwise try to parse the whole response
                return json.loads(response)
            except (json.JSONDecodeError, ValueError) as e:
                return {"error": f"Failed to parse JSON response: {str(e)}", "raw_response": response}
        
        # Return the raw response for other formats
        return {"result": response}

    def _create_prompt(self, text: str, output_format: str) -> str:
        """Create a prompt for knowledge extraction.

        Args:
            text (str): The text to extract knowledge from
            output_format (str): The desired output format

        Returns:
            str: The prompt for the model
        """
        # Get the prompt template from the configuration
        template = self.config.prompt_template
        
        # Replace variables in the template
        prompt = template.replace("{text}", text)
        prompt = prompt.replace("{output_format}", output_format)
        
        # Replace any other variables from the configuration
        if self.config.prompt_variables:
            for var in self.config.prompt_variables:
                if var in self.config.provider_config:
                    prompt = prompt.replace(f"{{{var}}}", str(self.config.provider_config[var]))
        
        return prompt


# Register the agent with the factory
AiAgentFactory.register_agent(AgentType.KNOWLEDGE_EXTRACTION, KnowledgeExtractionAgent)