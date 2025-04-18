"""
File data source for the Knowledge Extract Toolset.

This module implements a data source for extracting knowledge from uploaded files.
"""

import streamlit as st
from io import StringIO
from typing import Optional

from ..constants import SUPPORTED_FILE_TYPES
from .data_source import DataSource

class FileDataSource(DataSource):
    """Data source for file uploads."""

    def get_data(self) -> Optional[str]:
        """Extract text from an uploaded file.

        Returns:
            Optional[str]: The extracted text or None if extraction failed
        """
        st.subheader("Extract Knowledge From File")
        st.write("Upload a file containing text to extract knowledge from.")

        uploaded_file = st.file_uploader("Choose a file", type=SUPPORTED_FILE_TYPES)

        if uploaded_file is None:
            return None

        try:
            st.success("File uploaded successfully.")
            file_content = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
            return file_content
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return None