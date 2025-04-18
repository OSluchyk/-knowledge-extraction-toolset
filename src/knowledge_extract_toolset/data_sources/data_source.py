"""
Abstract base class for data sources in the Knowledge Extract Toolset.

This module defines the interface that all data sources must implement.
"""

from abc import ABC, abstractmethod
from typing import Optional

class DataSource(ABC):
    """Abstract base class for data sources."""

    @abstractmethod
    def get_data(self) -> Optional[str]:
        """Retrieve data from the source.

        Returns:
            Optional[str]: The extracted text data or None if extraction failed
        """
        pass