"""
Main application module for the Knowledge Extract Toolset.

This module implements the main application class that orchestrates the different
data sources and UI components.
"""

import os
import streamlit as st

from .constants import (
    TEXT_INPUT_KEY, TEXT_PROCESSED_KEY, SEARCH_RESULTS_KEY, LOAD_ARTICLE_KEY,
    SELECTED_TITLE_KEY, ARTICLE_DATA_KEY, WIKI_QUERY_KEY, TEXT_CHUNKS_KEY,
    SPLITTER_CONFIG_KEY, DEFAULT_SPLITTER_CONFIG, AI_AGENT_KEY, AI_AGENT_RESULT_KEY
)
from .data_sources import FileDataSource, TextInputDataSource, WikipediaDataSource
from .text_splitter import TextSplitter
from .ai_agent import AiAgentFactory, AgentType, load_all_agent_configs

class KnowledgeExtractApp:
    """Main application class for the Knowledge Extract Toolset."""

    def __init__(self):
        """Initialize the application."""
        self._configure_page()
        self._initialize_session_state()
        self._data_sources = [
            FileDataSource(),
            TextInputDataSource(),
            WikipediaDataSource()
        ]
        self._text_splitter = TextSplitter()

        # Load AI agent configurations
        self._load_ai_agents()

    def _configure_page(self):
        """Configure the Streamlit page settings."""
        st.set_page_config(
            page_title="Knowledge Extraction Toolset",
            page_icon=":brain:",
            layout="wide",
            initial_sidebar_state="collapsed",

        )
        st.title("Knowledge Extraction Toolset")

    def _initialize_session_state(self):
        """Initialize Streamlit session state variables."""
        # Initialize TEXT_PROCESSED_KEY to False, all others to None
        st.session_state.setdefault(TEXT_PROCESSED_KEY, False)
        st.session_state.setdefault(TEXT_INPUT_KEY, None)
        st.session_state.setdefault(SEARCH_RESULTS_KEY, None)
        st.session_state.setdefault(LOAD_ARTICLE_KEY, None)
        st.session_state.setdefault(SELECTED_TITLE_KEY, None)
        st.session_state.setdefault(ARTICLE_DATA_KEY, None)
        st.session_state.setdefault(WIKI_QUERY_KEY, None)
        st.session_state.setdefault(TEXT_CHUNKS_KEY, None)
        st.session_state.setdefault(SPLITTER_CONFIG_KEY, DEFAULT_SPLITTER_CONFIG)
        st.session_state.setdefault(AI_AGENT_KEY, None)
        st.session_state.setdefault(AI_AGENT_RESULT_KEY, None)
        # Add new session state variables for summarization
        st.session_state.setdefault("SUMMARY_AGENT_KEY", None)
        st.session_state.setdefault("SUMMARY_RESULT_KEY", None)

    def _load_ai_agents(self):
        """Load AI agent configurations from the config directory."""
        # Define the path to the agent configurations
        config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "config", "agents")

        # Load all agent configurations
        self._agent_configs = load_all_agent_configs(config_dir)

        # Log the loaded configurations
        if self._agent_configs:
            print(f"Loaded {len(self._agent_configs)} AI agent configurations:")
            for name in self._agent_configs:
                print(f"  - {name}")
        else:
            print("No AI agent configurations found in", config_dir)

    def run(self):
        """Run the application."""
        # Create main tabs for the application
        main_tab_titles = [
            "Content Acquisition",
            "Content Preparation",
            "AI Processing"
        ]

        main_tabs = st.tabs(main_tab_titles)

        # Content Acquisition tab
        with main_tabs[0]:
            self._render_data_loading_section()


        # Content Preparation tab
        with main_tabs[1]:
            self._render_text_splitting_section()

        # AI Processing tab
        with main_tabs[2]:
            # Create tabs for different AI processing types
            ai_tab_titles = [
                "Knowledge Extraction",
                "Summarization"
            ]

            ai_tabs = st.tabs(ai_tab_titles)

            # Knowledge Extraction tab
            with ai_tabs[0]:
                self._render_knowledge_extraction_tab()

            # Summarization tab
            with ai_tabs[1]:
                self._render_summarization_tab()

        # Create tabs for processing results
        st.markdown("---")
        st.markdown("## Processing Results")

        result_tab_titles = [
            "Raw Text",
            "Text Split",
            "Extracted Knowledge",
            "Knowledge Summary"
        ]

        result_tabs = st.tabs(result_tab_titles)

        # Raw Text tab
        with result_tabs[0]:
            if st.session_state.get(TEXT_INPUT_KEY):
                st.subheader("Raw Text")

                # Get the current text from session state
                current_text = st.session_state[TEXT_INPUT_KEY]

                # Display the text in an editable text area
                edited_text = st.text_area(
                    "Content",
                    value=current_text,
                    height=300,
                    key="raw_text_display"
                )

                # Add an Apply Changes button
                if st.button("Apply Changes", key="raw_text_apply_changes_button"):
                    if edited_text != current_text:
                        st.session_state[TEXT_INPUT_KEY] = edited_text
                        # Set the TEXT_PROCESSED flag to False to indicate that the text needs to be processed
                        st.session_state[TEXT_PROCESSED_KEY] = False
                        st.success("Changes applied successfully!")
            else:
                st.warning("No content has been acquired yet.")

        # Text Split tab
        with result_tabs[1]:
            if st.session_state.get(TEXT_CHUNKS_KEY):
                st.subheader("Text Split into Chunks")

                # Add slider and preview of chosen split
                self._text_splitter.render_preview(
                    st.session_state[TEXT_INPUT_KEY],
                    st.session_state[SPLITTER_CONFIG_KEY]
                )
            else:
                st.warning("Text has not been split into chunks yet.")

        # Extracted Knowledge tab
        with result_tabs[2]:
            if st.session_state.get(AI_AGENT_RESULT_KEY) and st.session_state.get(AI_AGENT_KEY):
                st.subheader(f"Knowledge Extracted by {st.session_state[AI_AGENT_KEY]}")
                result = st.session_state[AI_AGENT_RESULT_KEY]

                if "error" in result:
                    st.error(result["error"])
                    st.text_area("Raw Response", result.get("raw_response", ""), height=300)
                else:
                    st.json(result)
            else:
                st.warning("No knowledge has been extracted yet.")

        # Knowledge Summary tab
        with result_tabs[3]:
            if st.session_state.get("SUMMARY_RESULT_KEY") and st.session_state.get("SUMMARY_AGENT_KEY"):
                st.subheader(f"Summary Generated by {st.session_state['SUMMARY_AGENT_KEY']}")
                result = st.session_state["SUMMARY_RESULT_KEY"]

                st.markdown(result["summary"])
                st.write(f"Original length: {result['original_length']} characters")
                st.write(f"Summary length: {result['summary_length']} characters")
                st.write(f"Reduction: {result['reduction_percentage']}%")
            else:
                st.warning("No summary has been generated yet.")

    def _render_data_loading_section(self):
        """Render the data loading section of the UI."""
        st.write("Acquire content from various sources to extract knowledge from.")

        # Create tabs for different data sources
        tab_titles = [
            "From File",
            "From Text Input",
            "From Wikipedia"
        ]

        tabs = st.tabs(tab_titles)

        # Process each data source in its corresponding tab
        for i, (tab, data_source) in enumerate(zip(tabs, self._data_sources)):
            with tab:
                data = data_source.get_data()
                if data:
                    st.session_state[TEXT_INPUT_KEY] = data
                    # Set the TEXT_PROCESSED flag to False to indicate that the text needs to be processed
                    st.session_state[TEXT_PROCESSED_KEY] = False

    def _render_text_splitting_section(self):
        """Render the text splitting section of the UI."""
        if not st.session_state.get(TEXT_INPUT_KEY):
            st.warning("No content to prepare. Please acquire content from one of the sources above.")
            return

        st.write("Configure how to split the content into chunks for processing by the AI models.")

        # Get the current splitter configuration
        current_config = st.session_state.get(SPLITTER_CONFIG_KEY, DEFAULT_SPLITTER_CONFIG)

        # Render the splitter configuration UI
        new_config = self._text_splitter.render_config_ui()

        # Update the configuration if it has changed
        if new_config != current_config:
            st.session_state[SPLITTER_CONFIG_KEY] = new_config
            # Reset the chunks when configuration changes
            st.session_state[TEXT_CHUNKS_KEY] = None

        # Add a button to split the text
        if st.button("Split Content", key="split_text_button"):
            with st.spinner("Splitting content..."):
                # Get the current text from session state
                current_text = st.session_state[TEXT_INPUT_KEY]

                # Split the text using the current configuration
                chunks = self._text_splitter.split_text(current_text, new_config)

                # Store the chunks in session state
                st.session_state[TEXT_CHUNKS_KEY] = chunks

                st.success(f"Content split into {len(chunks)} chunks")


    def _render_knowledge_extraction_tab(self):
        """Render the UI for the knowledge extraction tab."""
        st.subheader("Extract Knowledge from Content")

        # Check if we have text to process
        if not st.session_state.get(TEXT_INPUT_KEY):
            st.warning("No content to process. Please acquire content from one of the sources in the Content Acquisition section.")
            return

        # Check if we have chunks to process
        if not st.session_state.get(TEXT_CHUNKS_KEY):
            st.warning("Content has not been split into chunks. Please split the content in the Content Preparation section.")
            return

        # Display the available knowledge extraction agents
        knowledge_extraction_agents = {name: config for name, config in self._agent_configs.items() 
                                      if config.agent_type == "knowledge_extraction"}

        if not knowledge_extraction_agents:
            st.error("No knowledge extraction agents available. Please check the configuration directory.")
            return

        # Create a selectbox for choosing an agent
        agent_names = list(knowledge_extraction_agents.keys())
        selected_agent_name = st.selectbox(
            "Select Knowledge Extraction Agent",
            agent_names,
            index=0 if agent_names else None,
            key="knowledge_extraction_agent_selectbox"
        )

        if selected_agent_name:
            # Get the selected agent configuration
            agent_config = knowledge_extraction_agents[selected_agent_name]

            # Display agent information
            with st.expander("Agent Information", expanded=False):
                st.write(f"**Description:** {agent_config.description}")
                st.write(f"**Model:** {agent_config.model_provider} / {agent_config.model_name}")

            # Display processing options
            st.subheader("Processing Options")

            output_format = st.selectbox(
                "Output Format",
                ["json", "markdown", "text"],
                index=0,
                key="output_format_selectbox"
            )

            use_batch_mode = st.checkbox(
                "Use Batch Mode (if available)",
                value=False,
                key="use_batch_mode_checkbox"
            )

            # Add chunk range selection
            use_chunk_range = st.checkbox(
                "Process specific chunk range",
                value=False,
                key="use_chunk_range_checkbox"
            )

            chunk_range_start = 1
            chunk_range_end = len(st.session_state.get(TEXT_CHUNKS_KEY, [])) or 1

            if use_chunk_range:
                col1, col2 = st.columns(2)
                with col1:
                    chunk_range_start = st.number_input(
                        "Start chunk (inclusive)",
                        min_value=1,
                        max_value=chunk_range_end,
                        value=1,
                        step=1,
                        key="chunk_range_start"
                    )
                with col2:
                    chunk_range_end = st.number_input(
                        "End chunk (inclusive)",
                        min_value=chunk_range_start,
                        max_value=len(st.session_state.get(TEXT_CHUNKS_KEY, [])) or 1,
                        value=min(5, len(st.session_state.get(TEXT_CHUNKS_KEY, [])) or 1),
                        step=1,
                        key="chunk_range_end"
                    )

            options = {"output_format": output_format}

            # Process button
            if st.button("Extract Knowledge", key="extract_knowledge_button"):
                with st.spinner(f"Extracting knowledge with {selected_agent_name}..."):
                    try:
                        # Create the agent
                        agent_type = AgentType.from_string(agent_config.agent_type)
                        agent = AiAgentFactory.create_agent(agent_type, agent_config)

                        # Get the chunks
                        chunks = st.session_state[TEXT_CHUNKS_KEY]

                        # Apply chunk range filtering if enabled
                        if use_chunk_range:
                            # Convert to 0-based indexing for slicing
                            start_idx = chunk_range_start - 1
                            end_idx = chunk_range_end
                            chunks = chunks[start_idx:end_idx]
                            st.info(f"Processing {len(chunks)} chunks (from chunk {chunk_range_start} to {chunk_range_end})")

                        # Process each chunk or use batch mode
                        if use_batch_mode and hasattr(agent, 'process_batch'):
                            # Use batch mode if available
                            result = agent.process_batch(chunks, **options)
                        else:
                            # Process chunks one by one
                            combined_result = {}
                            for i, chunk in enumerate(chunks):
                                st.write(f"Processing chunk {i+1}/{len(chunks)}...")
                                chunk_result = agent.process(chunk, **options)
                                # Combine results (assuming JSON format)
                                if isinstance(chunk_result, dict) and not "error" in chunk_result:
                                    for key, value in chunk_result.items():
                                        if key in combined_result:
                                            if isinstance(combined_result[key], list):
                                                if isinstance(value, list):
                                                    combined_result[key].extend(value)
                                                else:
                                                    combined_result[key].append(value)
                                        else:
                                            combined_result[key] = value if isinstance(value, list) else [value]
                                else:
                                    st.warning(f"Chunk {i+1} processing error: {chunk_result.get('error', 'Unknown error')}")

                            result = combined_result

                        # Store the result in session state
                        st.session_state[AI_AGENT_KEY] = selected_agent_name
                        st.session_state[AI_AGENT_RESULT_KEY] = result

                        st.success("Knowledge extraction complete!")
                    except Exception as e:
                        st.error(f"Error extracting knowledge: {str(e)}")

            # Display the result if available
            if st.session_state.get(AI_AGENT_RESULT_KEY) and st.session_state.get(AI_AGENT_KEY) == selected_agent_name:
                st.subheader("Extracted Knowledge")

                result = st.session_state[AI_AGENT_RESULT_KEY]

                # Display the result
                if "error" in result:
                    st.error(result["error"])
                    st.text_area("Raw Response", result.get("raw_response", ""), height=300)
                else:
                    st.json(result)

                    # Add file saving options
                    st.subheader("Save Extracted Knowledge")
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        file_name = st.text_input("File name", "extracted_knowledge", key="knowledge_file_name")
                        file_format = st.selectbox(
                            "File format",
                            ["json", "txt", "md"],
                            index=0,
                            key="knowledge_file_format"
                        )

                    with col2:
                        st.write("")
                        st.write("")
                        if st.button("Save to File", key="save_knowledge_button"):
                            try:
                                import json
                                import os

                                # Ensure file has correct extension
                                if not file_name.endswith(f".{file_format}"):
                                    file_name = f"{file_name}.{file_format}"

                                # Prepare content based on format
                                if file_format == "json":
                                    content = json.dumps(result, indent=2)
                                elif file_format == "md":
                                    # Convert JSON to markdown
                                    content = "# Extracted Knowledge\n\n"
                                    for key, value in result.items():
                                        content += f"## {key}\n"
                                        if isinstance(value, list):
                                            for item in value:
                                                content += f"- {item}\n"
                                        else:
                                            content += f"{value}\n\n"
                                else:  # txt
                                    content = json.dumps(result, indent=2)

                                # Save to file
                                with open(file_name, "w", encoding="utf-8") as f:
                                    f.write(content)

                                st.success(f"Successfully saved to {os.path.abspath(file_name)}")
                            except Exception as e:
                                st.error(f"Error saving file: {str(e)}")

    def _render_summarization_tab(self):
        """Render the UI for the summarization tab."""
        st.subheader("Summarize Extracted Knowledge")

        # Check if we have knowledge extraction results to summarize
        if not st.session_state.get(AI_AGENT_RESULT_KEY):
            st.warning("No extracted knowledge to summarize. Please extract knowledge first in the Knowledge Extraction tab.")
            return

        # Display the available summarization agents
        summarization_agents = {name: config for name, config in self._agent_configs.items() 
                               if config.agent_type == "summarization"}

        if not summarization_agents:
            st.error("No summarization agents available. Please check the configuration directory.")
            return

        # Create a selectbox for choosing an agent
        agent_names = list(summarization_agents.keys())
        selected_agent_name = st.selectbox(
            "Select Summarization Agent",
            agent_names,
            index=0 if agent_names else None,
            key="summarization_agent_selectbox"
        )

        if selected_agent_name:
            # Get the selected agent configuration
            agent_config = summarization_agents[selected_agent_name]

            # Display agent information
            with st.expander("Agent Information", expanded=False):
                st.write(f"**Description:** {agent_config.description}")
                st.write(f"**Model:** {agent_config.model_provider} / {agent_config.model_name}")

            # Display processing options
            st.subheader("Processing Options")

            length = st.selectbox(
                "Summary Length",
                ["short", "medium", "long"],
                index=1,
                key="length_selectbox"
            )

            focus = st.selectbox(
                "Summary Focus",
                ["general", "technical", "simplified"],
                index=0,
                key="focus_selectbox"
            )

            options = {"length": length, "focus": focus}

            # Process button
            if st.button("Generate Summary", key="generate_summary_button"):
                with st.spinner(f"Generating summary with {selected_agent_name}..."):
                    try:
                        # Create the agent
                        agent_type = AgentType.from_string(agent_config.agent_type)
                        agent = AiAgentFactory.create_agent(agent_type, agent_config)

                        # Get the extracted knowledge
                        extracted_knowledge = st.session_state[AI_AGENT_RESULT_KEY]

                        # Convert to text if it's a dictionary
                        if isinstance(extracted_knowledge, dict):
                            import json
                            knowledge_text = json.dumps(extracted_knowledge, indent=2)
                        else:
                            knowledge_text = str(extracted_knowledge)

                        # Process the text
                        result = agent.process(knowledge_text, **options)

                        # Store the result in session state
                        st.session_state["SUMMARY_AGENT_KEY"] = selected_agent_name
                        st.session_state["SUMMARY_RESULT_KEY"] = result

                        st.success("Summary generation complete!")
                    except Exception as e:
                        st.error(f"Error generating summary: {str(e)}")

            # Display the result if available
            if st.session_state.get("SUMMARY_RESULT_KEY") and st.session_state.get("SUMMARY_AGENT_KEY") == selected_agent_name:
                st.subheader("Generated Summary")

                result = st.session_state["SUMMARY_RESULT_KEY"]

                # Display the result
                st.markdown(result["summary"])
                st.write(f"Original length: {result['original_length']} characters")
                st.write(f"Summary length: {result['summary_length']} characters")
                st.write(f"Reduction: {result['reduction_percentage']}%")

                # Add file saving options
                st.subheader("Save Summary")
                col1, col2 = st.columns([3, 1])

                with col1:
                    file_name = st.text_input("File name", "summary", key="summary_file_name")
                    file_format = st.selectbox(
                        "File format",
                        ["txt", "md"],
                        index=0,
                        key="summary_file_format"
                    )

                with col2:
                    st.write("")
                    st.write("")
                    if st.button("Save to File", key="save_summary_button"):
                        try:
                            import os

                            # Ensure file has correct extension
                            if not file_name.endswith(f".{file_format}"):
                                file_name = f"{file_name}.{file_format}"

                            # Prepare content based on format
                            if file_format == "md":
                                content = f"# Summary\n\n{result['summary']}\n\n"
                                content += f"**Original length:** {result['original_length']} characters\n\n"
                                content += f"**Summary length:** {result['summary_length']} characters\n\n"
                                content += f"**Reduction:** {result['reduction_percentage']}%"
                            else:  # txt
                                content = f"SUMMARY\n\n{result['summary']}\n\n"
                                content += f"Original length: {result['original_length']} characters\n"
                                content += f"Summary length: {result['summary_length']} characters\n"
                                content += f"Reduction: {result['reduction_percentage']}%"

                            # Save to file
                            with open(file_name, "w", encoding="utf-8") as f:
                                f.write(content)

                            st.success(f"Successfully saved to {os.path.abspath(file_name)}")
                        except Exception as e:
                            st.error(f"Error saving file: {str(e)}")
