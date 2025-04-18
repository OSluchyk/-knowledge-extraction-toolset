"""
Configuration management for AI agents in the Knowledge Extract Toolset.

This module defines the configuration structure for AI agents and provides
functionality for loading agent configurations from HOCON files.
"""

import os
from dataclasses import dataclass
from typing import Dict, Any, Optional, List

try:
    from pyhocon import ConfigFactory, ConfigTree
except ImportError:
    raise ImportError(
        "pyhocon is required for HOCON configuration support. "
        "Install it with: pip install pyhocon"
    )


@dataclass
class AiAgentConfig:
    """Configuration for an AI agent."""

    # Agent identification
    name: str
    description: str
    agent_type: str

    # Model configuration
    model_provider: str  # 'openai', 'gemini', etc.
    model_name: str  # 'gpt-4', 'gemini-pro', etc.
    temperature: float = 0.7
    max_tokens: Optional[int] = None

    # Prompt configuration
    prompt_template: str = ""
    prompt_variables: List[str] = None

    # Additional provider-specific configuration
    provider_config: Dict[str, Any] = None

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'AiAgentConfig':
        """Create an AiAgentConfig from a dictionary.

        Args:
            config_dict (Dict[str, Any]): The configuration dictionary

        Returns:
            AiAgentConfig: The created configuration
        """
        # Extract known fields
        name = config_dict.get('name', 'Unnamed Agent')
        description = config_dict.get('description', '')
        agent_type = config_dict.get('agent_type', 'custom')

        model_provider = config_dict.get('model_provider', 'openai')
        model_name = config_dict.get('model_name', 'gpt-3.5-turbo')
        temperature = float(config_dict.get('temperature', 0.7))
        max_tokens = config_dict.get('max_tokens')

        prompt_template = config_dict.get('prompt_template', '')
        prompt_variables = config_dict.get('prompt_variables', [])

        # Extract provider-specific configuration
        provider_config = {}
        if 'provider_config' in config_dict:
            provider_config = dict(config_dict['provider_config'])

        return cls(
            name=name,
            description=description,
            agent_type=agent_type,
            model_provider=model_provider,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
            prompt_template=prompt_template,
            prompt_variables=prompt_variables,
            provider_config=provider_config
        )


def load_agent_config(config_path: str) -> AiAgentConfig:
    """Load an agent configuration from a HOCON file.

    Args:
        config_path (str): Path to the HOCON configuration file

    Returns:
        AiAgentConfig: The loaded configuration

    Raises:
        FileNotFoundError: If the configuration file does not exist
        ValueError: If the configuration is invalid
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    try:
        # Load the HOCON configuration
        config = ConfigFactory.parse_file(config_path)

        # Convert to a dictionary
        config_dict = {}
        for key in config:
            if isinstance(config[key], ConfigTree):
                config_dict[key] = dict(config[key])
            else:
                config_dict[key] = config[key]

        # Create the configuration object
        return AiAgentConfig.from_dict(config_dict)
    except Exception as e:
        raise ValueError(f"Failed to load configuration from {config_path}: {str(e)}")


def load_all_agent_configs(config_dir: str) -> Dict[str, AiAgentConfig]:
    """Load all agent configurations from a directory.

    Args:
        config_dir (str): Path to the directory containing HOCON configuration files

    Returns:
        Dict[str, AiAgentConfig]: Dictionary mapping agent names to configurations
    """
    if not os.path.exists(config_dir):
        return {}

    configs = {}
    for filename in os.listdir(config_dir):
        if filename.endswith('.conf'):
            try:
                config_path = os.path.join(config_dir, filename)
                config = load_agent_config(config_path)
                configs[config.name] = config
            except Exception as e:
                print(f"Warning: Failed to load configuration from {filename}: {str(e)}")

    return configs
