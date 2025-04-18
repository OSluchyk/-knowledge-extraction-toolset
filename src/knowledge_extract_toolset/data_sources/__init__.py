"""
Data sources package for the Knowledge Extract Toolset.

This package contains various data source implementations for extracting knowledge
from different sources like files, text input, and Wikipedia articles.
"""

from .data_source import DataSource
from .file_data_source import FileDataSource
from .text_input_data_source import TextInputDataSource
from .wikipedia_data_source import WikipediaDataSource

__all__ = [
    'DataSource',
    'FileDataSource',
    'TextInputDataSource',
    'WikipediaDataSource'
]
