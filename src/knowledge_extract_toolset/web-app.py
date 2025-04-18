"""
Knowledge Extract Toolset - A Streamlit application for extracting knowledge from various sources.

This module serves as the entry point for the Streamlit web application.
It imports and runs the main application class.
"""
from knowledge_extract_toolset import KnowledgeExtractApp

# Run the application
if __name__ == "__main__":
    app = KnowledgeExtractApp()
    app.run()
