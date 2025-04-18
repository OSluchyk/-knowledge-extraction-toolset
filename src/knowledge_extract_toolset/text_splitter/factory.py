"""
Factory for creating text splitter strategies.

This module provides a factory for creating text splitter strategies based on the specified type.
"""

from enum import Enum, auto
from typing import Dict

from .base import TextSplitterStrategy
from .strategies import (
    ParagraphSplitter,
    SentenceSplitter,
    WikicodeSplitter,
    CustomSymbolSplitter
)


class SplitterType(Enum):
    """Enum for different types of text splitters."""
    PARAGRAPH = auto()
    SENTENCE = auto()
    WIKICODE = auto()
    CUSTOM_SYMBOL = auto()

    @classmethod
    def from_string(cls, value: str) -> 'SplitterType':
        """Convert string to SplitterType enum.

        Args:
            value (str): String representation of splitter type

        Returns:
            SplitterType: Corresponding enum value
        """
        mapping = {
            "paragraph": cls.PARAGRAPH,
            "sentence": cls.SENTENCE,
            "wikicode": cls.WIKICODE,
            "custom_symbol": cls.CUSTOM_SYMBOL
        }
        return mapping.get(value, cls.PARAGRAPH)


class TextSplitterFactory:
    """Factory for creating text splitter strategies."""

    @staticmethod
    def create_splitter(splitter_type: SplitterType) -> TextSplitterStrategy:
        """Create a text splitter strategy based on the specified type.

        Args:
            splitter_type (SplitterType): Type of splitter to create

        Returns:
            TextSplitterStrategy: The created splitter strategy
        """
        splitters: Dict[SplitterType, TextSplitterStrategy] = {
            SplitterType.PARAGRAPH: ParagraphSplitter(),
            SplitterType.SENTENCE: SentenceSplitter(),
            SplitterType.WIKICODE: WikicodeSplitter(),
            SplitterType.CUSTOM_SYMBOL: CustomSymbolSplitter()
        }
        return splitters.get(splitter_type, ParagraphSplitter())