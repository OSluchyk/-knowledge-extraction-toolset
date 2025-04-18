"""
Concrete text splitting strategy implementations.

This module implements various text splitting strategies for different use cases.
"""

import re
from typing import List

from .base import BaseTextSplitterStrategy


class SentenceSplitter(BaseTextSplitterStrategy):
    """Strategy for splitting text by sentences."""

    def split(self, text: str, chunk_size: int, overlap: int, **kwargs) -> List[str]:
        """Split text by sentence count.

        Args:
            text (str): The text to split
            chunk_size (int): Maximum number of sentences per chunk, -1 for all sentences
            overlap (int): Number of sentences to overlap between chunks

        Returns:
            List[str]: List of text chunks
        """
        # Simple sentence splitting by period, question mark, or exclamation mark
        # followed by a space or newline
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        # If chunk_size is -1, return each sentence as a separate chunk
        if chunk_size == -1:
            return sentences

        return self._create_chunks(sentences, chunk_size, overlap, " ")


class ParagraphSplitter(BaseTextSplitterStrategy):
    """Strategy for splitting text by paragraphs."""

    def split(self, text: str, chunk_size: int, overlap: int, **kwargs) -> List[str]:
        """Split text by paragraph count.

        Args:
            text (str): The text to split
            chunk_size (int): Maximum number of paragraphs per chunk, -1 for all paragraphs
            overlap (int): Number of paragraphs to overlap between chunks

        Returns:
            List[str]: List of text chunks
        """
        # Split by double newline to identify paragraphs
        paragraphs = text.split("\n\n")
        paragraphs = [p.strip() for p in paragraphs if p.strip()]

        # If chunk_size is -1, return each paragraph as a separate chunk
        if chunk_size == -1:
            return paragraphs

        return self._create_chunks(paragraphs, chunk_size, overlap, "\n\n")


class WikicodeSplitter(BaseTextSplitterStrategy):
    """Strategy for splitting text by wikicode headers."""

    def split(self, text: str, chunk_size: int, overlap: int, **kwargs) -> List[str]:
        """Split text by wikicode headers.

        Args:
            text (str): The text to split
            chunk_size (int): Maximum number of sections per chunk, -1 for all sections
            overlap (int): Number of sections to overlap between chunks

        Returns:
            List[str]: List of text chunks
        """
        # Pattern to match wikicode headers (e.g., == Header ==, === Subheader ===)
        header_pattern = r'(^|\n)=+\s*[^=]+\s*=+'

        # Split text by headers
        sections = re.split(header_pattern, text)

        # Remove empty sections and strip whitespace
        sections = [s.strip() for s in sections if s.strip()]

        # If there are no headers, return the entire text as a single chunk
        if len(sections) <= 1:
            return [text]

        # If chunk_size is -1, return each section as a separate chunk
        if chunk_size == -1:
            return sections

        return self._create_chunks(sections, chunk_size, overlap, "\n\n")


class CustomSymbolSplitter(BaseTextSplitterStrategy):
    """Strategy for splitting text by a custom symbol."""

    def split(self, text: str, chunk_size: int, overlap: int, **kwargs) -> List[str]:
        """Split text by custom symbol.

        Args:
            text (str): The text to split
            chunk_size (int): Maximum number of segments per chunk, -1 for all segments
            overlap (int): Number of segments to overlap between chunks
            **kwargs: Additional parameters, including 'symbol'

        Returns:
            List[str]: List of text chunks
        """
        symbol = kwargs.get("symbol", "")
        if not symbol:
            return [text]

        segments = text.split(symbol)
        segments = [s.strip() for s in segments if s.strip()]

        # If chunk_size is -1, return each segment as a separate chunk
        if chunk_size == -1:
            return segments

        return self._create_chunks(segments, chunk_size, overlap, symbol)