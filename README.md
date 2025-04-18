# Knowledge Extract Toolset

A toolset for extracting knowledge from various sources, including files, text input, and Wikipedia articles.

## Features

- Extract text from files (TXT, PDF)
- Extract text from direct input
- Extract text from Wikipedia articles
- Split text into chunks using various strategies
- Process text using AI agents for knowledge extraction, summarization, and more
- Save extracted knowledge and summaries to files in various formats (JSON, TXT, MD)

## Installation

### Prerequisites

- Python 3.13 or higher
- Poetry (for dependency management)

### Setup

1. Clone the repository
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

## Usage

### Running the Application

The application can be run using the provided shell script:
```bash
./run.sh
```

Or manually with Poetry:
```bash
poetry run streamlit run src/knowledge_extract_toolset/web-app.py
```

### Using the Application

The application provides a web interface with the following tabs:

1. **Extract Knowledge From File**: Upload and extract text from files
2. **Extract Knowledge From Text**: Input text directly
3. **Extract Knowledge From Wikipedia Article**: Search and extract text from Wikipedia articles
4. **AI Processing**: Process extracted text using AI agents
   - **Knowledge Extraction**: Extract structured knowledge from text
   - **Summarization**: Generate summaries of extracted knowledge

#### Processing Specific Chunk Ranges

When extracting knowledge, you can choose to process only a specific range of chunks instead of all chunks:

1. Split your content into chunks in the Content Preparation section
2. In the Knowledge Extraction tab, check the "Process specific chunk range" option
3. Specify the start and end chunk numbers (e.g., chunks 1-5)
4. Click "Extract Knowledge" to process only the selected chunks

This feature is useful for:
- Testing extraction on a small subset of chunks
- Focusing on specific sections of content
- Reducing processing time for large documents

#### Saving Results to Files

After processing text with AI agents, you can save the results to files:

- **Extracted Knowledge**: Save in JSON, TXT, or MD formats
- **Summaries**: Save in TXT or MD formats

To save a result:
1. Process text using the appropriate AI agent
2. Scroll down to the "Save Extracted Knowledge" or "Save Summary" section
3. Enter a file name (or use the default)
4. Select the desired file format
5. Click the "Save to File" button

### AI Agents

The application includes an AI agent system that can process text using various LLM models. The following agents are available:

- **Knowledge Extraction Agent**: Extracts structured knowledge from text
- **Summarization Agent**: Summarizes text with configurable length and focus

#### Configuring AI Agents

AI agents are configured using HOCON configuration files in the `config/agents` directory. Each agent has its own configuration file with the following structure:

```hocon
# Agent identification
name = "Agent Name"
description = "Agent description"
agent_type = "agent_type"  # knowledge_extraction, summarization, etc.

# Model configuration
model_provider = "provider"  # openai, gemini, etc.
model_name = "model_name"  # gpt-3.5-turbo, gemini-pro, etc.
temperature = 0.7
max_tokens = 1000

# Prompt configuration
prompt_template = """
Prompt template with {variables}
"""

prompt_variables = []

# Provider-specific configuration
provider_config {
    api_key = ${?API_KEY_ENV_VAR}
}
```

#### Adding New AI Agents

To add a new AI agent:

1. Create a new configuration file in the `config/agents` directory
2. Implement the agent class in the `src/knowledge_extract_toolset/ai_agent/agents` directory
3. Register the agent with the `AiAgentFactory`

## Development

### Project Structure

- `src/knowledge_extract_toolset/` - Main application code
  - `web-app.py` - Streamlit web application
  - `app.py` - Main application class
  - `constants.py` - Application constants
  - `data_sources/` - Data source implementations
  - `text_splitter/` - Text splitting functionality
  - `ai_agent/` - AI agent functionality
    - `base.py` - Base classes for AI agents
    - `config.py` - Configuration management
    - `providers/` - Model provider implementations
    - `agents/` - Agent implementations
- `tests/` - Test files
- `config/` - Configuration files
  - `agents/` - AI agent configurations

### Testing Information

Tests are implemented using the Python `unittest` framework. To run all tests:
```bash
poetry run python -m unittest discover tests
```

To run a specific test file:
```bash
poetry run python -m unittest tests/test_wikipedia_api.py
```

### Adding New Tests
1. Create a new test file in the `tests` directory with a name starting with `test_`.
2. Import the necessary modules and the `unittest` framework.
3. Create a test class that inherits from `unittest.TestCase`.
4. Implement test methods that start with `test_`.
5. Use assertions to verify expected behavior.

Example:
```python
import unittest
from wikipedia import wikipedia

class TestWikipediaAPI(unittest.TestCase):
    def setUp(self):
        wikipedia.set_lang("en")

    def test_search(self):
        results = wikipedia.search("Python programming language", results=5)
        self.assertTrue(len(results) > 0)
```

### Test Example
A simple test for the Wikipedia API functionality has been created in `tests/test_wikipedia_api.py`. This test verifies:
1. The search functionality returns relevant results
2. The page retrieval functionality returns pages with content, title, and URL

### Code Style
- Follow PEP 8 guidelines for Python code
- Use docstrings for classes and functions
- Keep functions small and focused on a single responsibility

### Streamlit Application
The application is built using Streamlit and provides three main functionalities:
1. Extract knowledge from files
2. Extract knowledge from text
3. Extract knowledge from Wikipedia articles

When extending the application:
- Keep the tab-based interface for different data sources
- Use Streamlit session state for managing application state
- Handle exceptions appropriately with user-friendly error messages

### External APIs
The application uses the Wikipedia API for retrieving article data. When working with this API:
- Set the language using `wikipedia.set_lang("en")`
- Handle disambiguation errors and page errors
- Use `auto_suggest=False` to get exact matches

## License

This project is licensed under the MIT License - see the LICENSE file for details.
