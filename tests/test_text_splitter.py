import unittest
from knowledge_extract_toolset.text_splitter import (
    TextSplitter, 
    SentenceSplitter, 
    ParagraphSplitter, 
    WikicodeSplitter, 
    CustomSymbolSplitter,
    SplitterType,
    TextSplitterFactory
)

class TestTextSplitter(unittest.TestCase):
    """Test cases for the TextSplitter class and its components."""

    def setUp(self):
        """Set up test fixtures."""
        self.text_splitter = TextSplitter()
        self.factory = TextSplitterFactory()

        # Sample text for testing
        self.paragraph_text = "This is paragraph one.\n\nThis is paragraph two.\n\nThis is paragraph three."
        self.sentence_text = "This is sentence one. This is sentence two. This is sentence three."
        self.wikicode_text = "== Section 1 ==\nContent for section 1.\n\n== Section 2 ==\nContent for section 2."
        self.custom_symbol_text = "Item 1,Item 2,Item 3,Item 4"

    def test_paragraph_splitter(self):
        """Test splitting by paragraphs."""
        config = {"split_by": "paragraph", "chunk_size": -1, "overlap": 0}
        chunks = self.text_splitter.split_text(self.paragraph_text, config)
        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks[0], "This is paragraph one.")
        self.assertEqual(chunks[1], "This is paragraph two.")
        self.assertEqual(chunks[2], "This is paragraph three.")

    def test_sentence_splitter(self):
        """Test splitting by sentences."""
        config = {"split_by": "sentence", "chunk_size": -1, "overlap": 0}
        chunks = self.text_splitter.split_text(self.sentence_text, config)
        self.assertEqual(len(chunks), 3)
        self.assertEqual(chunks[0], "This is sentence one.")
        self.assertEqual(chunks[1], "This is sentence two.")
        self.assertEqual(chunks[2], "This is sentence three.")

    def test_wikicode_splitter(self):
        """Test splitting by wikicode headers."""
        config = {"split_by": "wikicode", "chunk_size": -1, "overlap": 0}
        chunks = self.text_splitter.split_text(self.wikicode_text, config)
        self.assertEqual(len(chunks), 2)

    def test_custom_symbol_splitter(self):
        """Test splitting by custom symbol."""
        config = {"split_by": "custom_symbol", "chunk_size": -1, "overlap": 0, "custom_symbol": ","}
        chunks = self.text_splitter.split_text(self.custom_symbol_text, config)
        self.assertEqual(len(chunks), 4)
        self.assertEqual(chunks[0], "Item 1")
        self.assertEqual(chunks[1], "Item 2")
        self.assertEqual(chunks[2], "Item 3")
        self.assertEqual(chunks[3], "Item 4")

    def test_chunk_size_and_overlap(self):
        """Test chunk size and overlap parameters."""
        # Test with chunk_size=2 and overlap=0
        config = {"split_by": "paragraph", "chunk_size": 2, "overlap": 0}
        chunks = self.text_splitter.split_text(self.paragraph_text, config)
        self.assertEqual(len(chunks), 2)

        # Test with chunk_size=2 and overlap=1
        config = {"split_by": "paragraph", "chunk_size": 2, "overlap": 1}
        chunks = self.text_splitter.split_text(self.paragraph_text, config)
        self.assertEqual(len(chunks), 2)

    def test_factory_creates_correct_strategies(self):
        """Test that the factory creates the correct strategies."""
        paragraph_splitter = self.factory.create_splitter(SplitterType.PARAGRAPH)
        self.assertIsInstance(paragraph_splitter, ParagraphSplitter)

        sentence_splitter = self.factory.create_splitter(SplitterType.SENTENCE)
        self.assertIsInstance(sentence_splitter, SentenceSplitter)

        wikicode_splitter = self.factory.create_splitter(SplitterType.WIKICODE)
        self.assertIsInstance(wikicode_splitter, WikicodeSplitter)

        custom_symbol_splitter = self.factory.create_splitter(SplitterType.CUSTOM_SYMBOL)
        self.assertIsInstance(custom_symbol_splitter, CustomSymbolSplitter)

    def test_empty_text(self):
        """Test with empty text."""
        config = {"split_by": "paragraph", "chunk_size": -1, "overlap": 0}
        chunks = self.text_splitter.split_text("", config)
        self.assertEqual(len(chunks), 0)

if __name__ == "__main__":
    unittest.main()
