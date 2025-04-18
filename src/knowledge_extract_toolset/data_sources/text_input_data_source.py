"""
Text input data source for the Knowledge Extract Toolset.

This module implements a data source for extracting knowledge from direct text input.
"""

import streamlit as st
from typing import Optional

from ..constants import TEXT_INPUT_KEY, TEXT_PROCESSED_KEY
from .data_source import DataSource

class TextInputDataSource(DataSource):
    """Data source for direct text input."""

    def get_data(self) -> Optional[str]:
        """Get text from user input.

        Returns:
            Optional[str]: The user-entered text or None if no text was entered
        """
        st.subheader("Extract Knowledge From Text")
        st.write("Enter text to extract knowledge from or edit text loaded from other sources.")

        # Get current text from session state
        current_value = st.session_state.get(TEXT_INPUT_KEY) or ""

        # Display text area with current value
        user_input = st.text_area("Enter or edit text", height=300, value=current_value, key="user_input_text_area")

        # Update session state with the current text input
        # This ensures the text is available for processing even if the user doesn't click "Apply Changes"
        if user_input != current_value:
            st.session_state[TEXT_INPUT_KEY] = user_input

        # Add an Apply Changes button
        if st.button("Apply Changes", key="apply_text_changes_button"):
            if user_input:
                # Set the TEXT_PROCESSED flag to False to indicate that the text needs to be processed
                st.session_state[TEXT_PROCESSED_KEY] = False
                st.success("Changes applied successfully!")
                return user_input
            else:
                st.warning("No text to apply. Please enter some text.")
                return None

        # Return None if no changes were applied
        return None