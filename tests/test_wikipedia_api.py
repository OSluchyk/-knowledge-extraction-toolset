import unittest
from wikipedia import wikipedia

class TestWikipediaAPI(unittest.TestCase):
    """Test the Wikipedia API functionality used in the application."""
    
    def setUp(self):
        """Set up the test environment."""
        # Set Wikipedia language to English
        wikipedia.set_lang("en")
    
    def test_search(self):
        """Test the Wikipedia search functionality."""
        # Search for a term that should return results
        results = wikipedia.search("Python programming language", results=5)
        
        # Verify that results were returned
        self.assertTrue(len(results) > 0, "Wikipedia search should return results")
        
        # Verify that the results contain relevant terms
        relevant_terms = ["Python", "programming", "language"]
        found_relevant = False
        for result in results:
            if any(term.lower() in result.lower() for term in relevant_terms):
                found_relevant = True
                break
        
        self.assertTrue(found_relevant, "Search results should contain relevant terms")
    
    def test_page_retrieval(self):
        """Test the Wikipedia page retrieval functionality."""
        # Get a page that should exist
        page = wikipedia.page("Python (programming language)", auto_suggest=False)
        
        # Verify that the page has content
        self.assertTrue(len(page.content) > 0, "Wikipedia page should have content")
        
        # Verify that the page has a title
        self.assertTrue(len(page.title) > 0, "Wikipedia page should have a title")
        
        # Verify that the page has a URL
        self.assertTrue(len(page.url) > 0, "Wikipedia page should have a URL")

if __name__ == "__main__":
    unittest.main()