# LLM Prompt Refinement Tool

A Streamlit application that transforms clarifying questions and brain-dump answers into clear, structured responses you can paste back to the AI.

## Features

- **Multi-Provider Support**: Works with OpenAI, OpenRouter, and Ollama
- **Dynamic Configuration**: Secure API key management with local .env persistence
- **Clean Output**: Generates natural, ready-to-use prompts without formatting overhead
- **Real-time Validation**: Input validation and connection testing
- **Responsive UI**: Clean three-column interface for easy prompt refinement

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```

2. **Configure your LLM provider**:
   - Open the Configuration sidebar
   - Select your provider (OpenAI, OpenRouter, or Ollama)
   - Enter your API credentials
   - Click "Save Settings"

3. **Refine your responses**:
   - Paste AI clarifying questions in the left column
   - Brain-dump your answers in the middle column
   - Click "Refine Response"
   - Copy the structured response from the right column and paste back to the original AI

## Provider Setup

### OpenAI
- **API Key**: Your OpenAI API key
- **Model**: Model name (e.g., `gpt-4o`, `gpt-4`, `o1-preview`, `o1-mini`, `gpt-5`)
- **Note**: Automatically handles model-specific parameter restrictions:
  - **Regular models**: Support temperature, max_tokens/max_completion_tokens
  - **Reasoning models** (o1, o3, gpt-5 series): Use default parameters only (temperature=1)

### OpenRouter
- **API Key**: Your OpenRouter API key
- **Model**: Full model path (e.g., `mistralai/mixtral-8x7b-instruct`)

### Ollama
- **Model**: Local model name (e.g., `llama3`, `mistral`)
- **Base URL**: Ollama server URL (default: `http://localhost:11434`)

## Example Usage

**Input - Clarifying Questions:**
```
1. What specific topic should the content focus on?
2. Who is the target audience?
3. What tone and style should be used?
4. What is the desired length?
```

**Input - Raw User Responses:**
```
I want to write about machine learning but for complete beginners.
Make it friendly and approachable, not too technical.
Maybe around 1000 words with some simple examples they can understand.
```

**Output - Refined Response:**
```
I want to write about machine learning for complete beginners. The target audience is people who have never encountered ML before - maybe students, professionals curious about the field, or general readers interested in technology.

The tone should be friendly and approachable, avoiding technical jargon. I want to use simple language that makes complex concepts accessible. The content should include practical examples that readers can relate to from their daily lives, like how Netflix recommends movies or how email filters work.

The goal is to create an introduction that covers what machine learning actually is, how it works in basic terms, and why it matters in everyday life.
```

## File Structure

```
rosetta-prompt/
├── app.py              # Main Streamlit application
├── config_manager.py   # Configuration and .env management
├── api_clients.py      # LLM API client implementations
├── prompt_refiner.py   # Core prompt refinement logic
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (auto-created)
└── .gitignore         # Git ignore rules
```

## Security Notes

- API keys are stored locally in a `.env` file
- Keys are masked in the UI for security
- No credentials are logged or transmitted except to their respective APIs
- The `.env` file is excluded from git via `.gitignore`

## Troubleshooting

### Connection Issues
- **OpenAI/OpenRouter**: Verify your API key is correct and has sufficient credits
- **Ollama**: Ensure Ollama is running locally and the model is installed

### Model Not Found (Ollama)
```bash
# List available models
ollama list

# Pull a model if needed
ollama pull llama3
```

### Empty Responses
- Check that your inputs meet the minimum length requirements
- Verify the selected model supports the requested functionality
- Try with a different model or provider

## Development

The application is modular and extensible:

- `ConfigManager`: Handles all configuration and persistence
- `APIClientFactory`: Creates appropriate LLM clients
- `PromptRefiner`: Core refinement logic with XML processing
- `app.py`: Streamlit UI and user interaction

## License

This project is provided as-is for educational and development purposes.