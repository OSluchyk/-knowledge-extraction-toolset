"""
UI components for text splitter configuration and preview.

This module provides UI components for configuring and previewing text splitting.
"""

from typing import Dict, Any, List
import streamlit as st


class TextSplitterUI:
    """UI component for text splitter configuration and preview."""

    def render_config_ui(self) -> Dict[str, Any]:
        """Render the UI for configuring the text splitter.

        Returns:
            Dict[str, Any]: The configuration settings
        """
        st.subheader("Text Splitting Configuration")

        # Create columns for a more compact layout
        col1, col2 = st.columns(2)

        with col1:
            split_by = st.selectbox(
                "Split by",
                options=["paragraph", "sentence", "wikicode", "custom_symbol"],
                index=0,  # Default to paragraph
                help="Method to use for splitting the text"
            )

            # Show custom symbol input if selected
            custom_symbol = ""
            if split_by == "custom_symbol":
                custom_symbol = st.text_input(
                    "Custom symbol",
                    value=",",
                    help="Enter the symbol to split by (e.g., comma, semicolon)"
                )

        # Return the configuration
        config = {
            "split_by": split_by,
            "chunk_size": -1,
            "overlap": 0
        }

        # Add custom symbol if applicable
        if split_by == "custom_symbol":
            config["custom_symbol"] = custom_symbol

        return config

    def render_preview(self, text: str, config: Dict[str, Any], splitter: 'TextSplitter') -> None:
        """Render a preview of the text splitting.

        Args:
            text (str): The text to split
            config (Dict[str, Any]): Configuration for splitting the text
            splitter (TextSplitter): The text splitter to use
        """
        if not text:
            st.warning("No text to preview. Please extract knowledge from a file or text input.")
            return

        chunks = splitter.split_text(text, config)

        st.subheader("Text Splitting Preview")
        st.write(f"Text split into {len(chunks)} chunks")

        # Add a slider to select which chunk to view
        if len(chunks) > 0:
            # Create a container for the chunk preview
            chunk_container = st.container()

            # If there's more than one chunk, show a slider
            if len(chunks) > 1:
                # Create a slider to select which chunk to view
                selected_chunk_index = st.slider(
                    "Select chunk to view",
                    min_value=1,
                    max_value=len(chunks),
                    value=1,
                    help="Use the slider to navigate through all chunks"
                )
                # Display the selected chunk (adjust index to be 0-based)
                chunk_index = selected_chunk_index - 1

                with chunk_container:
                    st.subheader(f"Chunk {selected_chunk_index}/{len(chunks)}")
            else:
                # If there's only one chunk, display it directly
                chunk_index = 0

                with chunk_container:
                    st.subheader("Single Chunk")

            # Display chunk content
            with chunk_container:
                st.text_area(
                    "Chunk content",
                    value=chunks[chunk_index],
                    height=200,
                    disabled=True
                )

                # Display chunk statistics
                st.info(f"Chunk size: {len(chunks[chunk_index])} characters, {len(chunks[chunk_index].split())} words")
        else:
            st.warning("No chunks were created. Please check your splitting configuration.")