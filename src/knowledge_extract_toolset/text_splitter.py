"""
Text splitter module for the Knowledge Extract Toolset.

This module implements functionality to split text into chunks based on user-defined configuration.
Following SOLID principles, this implementation separates concerns and uses the Strategy pattern
for different text splitting methods.

This module is maintained for backward compatibility.
The actual implementation has been moved to the text_splitter package.
"""

from typing import List, Dict, Any

# Import the UI class
from .text_splitter.ui import TextSplitterUI
# Import the factory
from .text_splitter.factory import TextSplitterFactory, SplitterType


class TextSplitter:
    """Text splitter class for splitting text into chunks.

    This class acts as a facade for the text splitting functionality,
    delegating to the appropriate strategy based on configuration.
    """

    def __init__(self):
        """Initialize the text splitter."""
        self._ui = TextSplitterUI()
        self._factory = TextSplitterFactory()

    def split_text(self, text: str, config: Dict[str, Any]) -> List[str]:
        """Split text into chunks based on the provided configuration.

        Args:
            text (str): The text to split
            config (Dict[str, Any]): Configuration for splitting the text

        Returns:
            List[str]: List of text chunks
        """
        if not text:
            return []

        # Get splitting parameters from config
        chunk_size = config.get("chunk_size", -1)
        overlap = config.get("overlap", 0)
        split_by = config.get("split_by", "paragraph")
        custom_symbol = config.get("custom_symbol", "")

        # Create the appropriate splitter strategy
        splitter_type = SplitterType.from_string(split_by)
        splitter = self._factory.create_splitter(splitter_type)

        # Additional parameters for specific strategies
        kwargs = {}
        if splitter_type == SplitterType.CUSTOM_SYMBOL:
            kwargs["symbol"] = custom_symbol

        # Split the text using the selected strategy
        return splitter.split(text, chunk_size, overlap, **kwargs)

    def render_config_ui(self) -> Dict[str, Any]:
        """Render the UI for configuring the text splitter.

        Returns:
            Dict[str, Any]: The configuration settings
        """
        return self._ui.render_config_ui()

    def render_preview(self, text: str, config: Dict[str, Any]) -> None:
        """Render a preview of the text splitting.

        Args:
            text (str): The text to split
            config (Dict[str, Any]): Configuration for splitting the text
        """
        self._ui.render_preview(text, config, self)

