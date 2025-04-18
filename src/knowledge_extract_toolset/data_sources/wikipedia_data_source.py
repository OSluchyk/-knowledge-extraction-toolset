"""
Wikipedia data source for the Knowledge Extract Toolset.

This module implements a data source for extracting knowledge from Wikipedia articles.
"""

import streamlit as st
from typing import List, Tuple, Optional, Any
from wikipedia import wikipedia, DisambiguationError, PageError

from ..constants import (
    WIKI_QUERY_KEY, SEARCH_RESULTS_KEY, ARTICLE_DATA_KEY, SELECTED_TITLE_KEY,
    WIKIPEDIA_LANGUAGE, MAX_SEARCH_RESULTS, MAX_DISAMBIGUATION_SUGGESTIONS
)
from .data_source import DataSource

class WikipediaDataSource(DataSource):
    """Data source for Wikipedia articles."""

    def __init__(self):
        """Initialize the Wikipedia data source."""
        # Set Wikipedia language
        wikipedia.set_lang(WIKIPEDIA_LANGUAGE)

    def search_wikipedia(self, query: str) -> List[str]:
        """Search Wikipedia for articles matching the query.

        Args:
            query (str): The search query

        Returns:
            List[str]: List of article titles matching the query
        """
        try:
            with st.spinner("Finding suggestions..."):
                results = wikipedia.search(query, results=MAX_SEARCH_RESULTS)
            return results
        except Exception as e:
            st.error(f"Search failed: {e}")
            return []

    def load_article(self, title: str) -> Tuple[Optional[Any], Optional[str]]:
        """Load a Wikipedia article by title.

        Args:
            title (str): The title of the article to load

        Returns:
            Tuple[Optional[Any], Optional[str]]: A tuple containing the page object and summary
        """
        try:
            with st.spinner(f"Loading '{title}'..."):
                page = wikipedia.page(title, auto_suggest=False)
                summary = wikipedia.summary(title, auto_suggest=False)
            return page, summary
        except DisambiguationError as e:
            suggestions = ", ".join(e.options[:MAX_DISAMBIGUATION_SUGGESTIONS])
            st.error(f"This topic is ambiguous. Suggestions: {suggestions}")
            return None, None
        except PageError:
            st.error("This page could not be found.")
            return None, None
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            return None, None

    def get_data(self) -> Optional[str]:
        """Extract text from a Wikipedia article.

        Returns:
            Optional[str]: The article content or None if extraction failed
        """
        # Step 1: Input field for searching
        wiki_query = st.text_input(
            "🔎 Enter a Wikipedia topic:",
            placeholder="Start typing to see suggestions...",
            key="wiki_search_input"
        )

        # When query is entered, fetch search results
        if wiki_query and (not st.session_state.get(WIKI_QUERY_KEY) or 
                          wiki_query != st.session_state.get(WIKI_QUERY_KEY)):
            st.session_state[WIKI_QUERY_KEY] = wiki_query
            results = self.search_wikipedia(wiki_query)
            st.session_state[SEARCH_RESULTS_KEY] = results
            st.session_state[ARTICLE_DATA_KEY] = None  # Reset previous article

        # Step 2: Show suggestions as selectable options
        search_results = st.session_state.get(SEARCH_RESULTS_KEY)
        if search_results is not None:
            if len(search_results) == 0:
                st.warning("No articles found. Try a different topic.")
                return None

            st.write("Select an article:")
            selected_article = st.selectbox(
                "Choose an article to load:",
                options=search_results,
                index=0,
                label_visibility="collapsed"
            )

            # Load button to confirm selection
            if st.button("Load Article", key="load_article_button") and selected_article:
                page, summary = self.load_article(selected_article)

                if page and summary:
                    st.session_state[ARTICLE_DATA_KEY] = (page, summary)
                    st.session_state[SELECTED_TITLE_KEY] = selected_article
                    st.info(f"Article loaded: {page.title}. 🌐 [View on Wikipedia]({page.url})")
                    return page.content

        return None