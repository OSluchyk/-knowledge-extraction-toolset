"""
Constants for the Knowledge Extract Toolset.

This module contains all the constants used throughout the application.
"""

# Session state keys
TEXT_INPUT_KEY = "text_input"
TEXT_PROCESSED_KEY = "text_processed"  # Flag to indicate if the text has been processed
SEARCH_RESULTS_KEY = "search_results"
LOAD_ARTICLE_KEY = "load_article"
SELECTED_TITLE_KEY = "selected_title"
ARTICLE_DATA_KEY = "article_data"
WIKI_QUERY_KEY = "wiki_query"
TEXT_CHUNKS_KEY = "text_chunks"  # List of text chunks after splitting
SPLITTER_CONFIG_KEY = "splitter_config"  # Configuration for text splitting
AI_AGENT_KEY = "ai_agent"  # Selected AI agent
AI_AGENT_RESULT_KEY = "ai_agent_result"  # Result of AI agent processing

# Application constants
SUPPORTED_FILE_TYPES = ["txt", "pdf"]
WIKIPEDIA_LANGUAGE = "en"
MAX_SEARCH_RESULTS = 10
MAX_DISAMBIGUATION_SUGGESTIONS = 5

# Default splitter configuration
DEFAULT_SPLITTER_CONFIG = {
    "split_by": "paragraph",
    "chunk_size": -1,
    "overlap": 0
}
