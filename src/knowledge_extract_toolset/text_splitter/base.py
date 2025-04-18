"""
Base classes for text splitting strategies.

This module defines the abstract base classes and interfaces for text splitting strategies.
"""

from typing import List, Dict, Any
from abc import ABC, abstractmethod


class TextSplitterStrategy(ABC):
    """Abstract base class for text splitting strategies."""

    @abstractmethod
    def split(self, text: str, chunk_size: int, overlap: int, **kwargs) -> List[str]:
        """Split text into chunks using the strategy.

        Args:
            text (str): The text to split
            chunk_size (int): Maximum number of units per chunk, -1 for all units
            overlap (int): Number of units to overlap between chunks
            **kwargs: Additional strategy-specific parameters

        Returns:
            List[str]: List of text chunks
        """
        pass


class BaseTextSplitterStrategy(TextSplitterStrategy):
    """Base implementation for text splitting strategies with common functionality."""

    def _create_chunks(self, units: List[str], chunk_size: int, overlap: int, separator: str) -> List[str]:
        """Create chunks from a list of units with specified overlap.

        Args:
            units (List[str]): The units to chunk (sentences, paragraphs, etc.)
            chunk_size (int): Maximum number of units per chunk
            overlap (int): Number of units to overlap between chunks
            separator (str): String to use when joining units

        Returns:
            List[str]: List of text chunks
        """
        chunks = []
        start = 0
        unit_count = len(units)

        while start < unit_count:
            # Calculate end position with overlap
            end = min(start + chunk_size, unit_count)

            # Add chunk to list
            chunks.append(separator.join(units[start:end]))

            # Move start position for next chunk, considering overlap
            start = end - overlap if end < unit_count else unit_count

        return chunks

    @abstractmethod
    def split(self, text: str, chunk_size: int, overlap: int, **kwargs) -> List[str]:
        pass