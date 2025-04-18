"""
AI Agent package for the Knowledge Extract Toolset.

This package provides functionality for working with AI agents that can process text
using various LLM models and configurations.
"""

from .base import AiAgent, AiAgentFactory, AgentType
from .config import AiAgentConfig, load_agent_config, load_all_agent_configs
# Import agents to ensure registration
from . import agents
# Import providers to ensure registration
from . import providers

__all__ = [
    'AiAgent',
    'AiAgentFactory',
    'AgentType',
    'AiAgentConfig',
    'load_agent_config',
    'load_all_agent_configs'
]
