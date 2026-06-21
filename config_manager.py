import os
import streamlit as st
from dotenv import load_dotenv, set_key, find_dotenv
from typing import Dict, Any, Optional

class ConfigManager:
    """Manages configuration settings with .env file persistence."""

    PROVIDERS = ["OpenAI", "OpenRouter", "Ollama"]

    ENV_KEYS = {
        "OpenAI": {
            "api_key": "OPENAI_API_KEY",
            "model": "OPENAI_MODEL"
        },
        "OpenRouter": {
            "api_key": "OPENROUTER_API_KEY",
            "model": "OPENROUTER_MODEL"
        },
        "Ollama": {
            "model": "OLLAMA_MODEL",
            "base_url": "OLLAMA_BASE_URL"
        }
    }

    DEFAULT_VALUES = {
        "ACTIVE_PROVIDER": "OpenAI",
        "OPENAI_MODEL": "gpt-4o",  # Use gpt-4o as default instead of gpt-4
        "OPENROUTER_MODEL": "mistralai/mixtral-8x7b-instruct",
        "OLLAMA_MODEL": "llama3",
        "OLLAMA_BASE_URL": "http://localhost:11434"
    }

    def __init__(self):
        """Initialize configuration manager and load existing settings."""
        self.env_file = find_dotenv() or ".env"
        load_dotenv(self.env_file)
        self._ensure_env_file_exists()
        self._load_defaults()

    def _ensure_env_file_exists(self):
        """Create .env file if it doesn't exist."""
        if not os.path.exists(self.env_file):
            with open(self.env_file, 'w') as f:
                f.write("# LLM Prompt Refinement Tool Configuration\n")

    def _load_defaults(self):
        """Load default values for missing environment variables."""
        for key, default_value in self.DEFAULT_VALUES.items():
            if not os.getenv(key):
                self.set_env_value(key, default_value)

    def get_env_value(self, key: str) -> Optional[str]:
        """Get environment variable value."""
        return os.getenv(key)

    def set_env_value(self, key: str, value: str):
        """Set environment variable and persist to .env file."""
        os.environ[key] = value
        set_key(self.env_file, key, value)

    def get_active_provider(self) -> str:
        """Get the currently active provider."""
        return self.get_env_value("ACTIVE_PROVIDER") or "OpenAI"

    def set_active_provider(self, provider: str):
        """Set the active provider."""
        if provider in self.PROVIDERS:
            self.set_env_value("ACTIVE_PROVIDER", provider)

    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        """Get configuration for a specific provider."""
        config = {}
        if provider in self.ENV_KEYS:
            for field, env_key in self.ENV_KEYS[provider].items():
                config[field] = self.get_env_value(env_key) or ""
        return config

    def save_provider_config(self, provider: str, config: Dict[str, str]):
        """Save configuration for a specific provider."""
        if provider in self.ENV_KEYS:
            for field, value in config.items():
                if field in self.ENV_KEYS[provider]:
                    env_key = self.ENV_KEYS[provider][field]
                    if value.strip():  # Only save non-empty values
                        self.set_env_value(env_key, value.strip())

    def validate_provider_config(self, provider: str) -> tuple[bool, str]:
        """Validate that a provider has all required configuration."""
        config = self.get_provider_config(provider)

        if provider == "OpenAI":
            if not config.get("api_key"):
                return False, "OpenAI API key is required"
            if not config.get("model"):
                return False, "OpenAI model name is required"

        elif provider == "OpenRouter":
            if not config.get("api_key"):
                return False, "OpenRouter API key is required"
            if not config.get("model"):
                return False, "OpenRouter model name is required"

        elif provider == "Ollama":
            if not config.get("model"):
                return False, "Ollama model name is required"
            if not config.get("base_url"):
                return False, "Ollama base URL is required"

        return True, ""

    def render_config_ui(self):
        """Render the configuration UI in Streamlit."""
        st.sidebar.header("Configuration")

        # Provider selection
        current_provider = self.get_active_provider()
        selected_provider = st.sidebar.selectbox(
            "Active Provider",
            self.PROVIDERS,
            index=self.PROVIDERS.index(current_provider) if current_provider in self.PROVIDERS else 0,
            key="provider_selectbox"
        )

        if selected_provider != current_provider:
            self.set_active_provider(selected_provider)
            st.rerun()

        # Provider-specific configuration
        st.sidebar.subheader(f"{selected_provider} Settings")
        config = self.get_provider_config(selected_provider)
        updated_config = {}

        if selected_provider == "OpenAI":
            updated_config["api_key"] = st.sidebar.text_input(
                "API Key",
                value=config.get("api_key", ""),
                type="password",
                help="Your OpenAI API key",
                key="openai_api_key"
            )
            updated_config["model"] = st.sidebar.text_input(
                "Model Name",
                value=config.get("model", "gpt-4o"),
                help="e.g., gpt-4o, gpt-4, gpt-3.5-turbo, o1-preview, o1-mini",
                key="openai_model"
            )

        elif selected_provider == "OpenRouter":
            updated_config["api_key"] = st.sidebar.text_input(
                "API Key",
                value=config.get("api_key", ""),
                type="password",
                help="Your OpenRouter API key",
                key="openrouter_api_key"
            )
            updated_config["model"] = st.sidebar.text_input(
                "Model Name",
                value=config.get("model", "mistralai/mixtral-8x7b-instruct"),
                help="e.g., mistralai/mixtral-8x7b-instruct",
                key="openrouter_model"
            )

        elif selected_provider == "Ollama":
            updated_config["model"] = st.sidebar.text_input(
                "Model Name",
                value=config.get("model", "llama3"),
                help="e.g., llama3, mistral",
                key="ollama_model"
            )
            updated_config["base_url"] = st.sidebar.text_input(
                "Base URL",
                value=config.get("base_url", "http://localhost:11434"),
                help="Ollama server URL",
                key="ollama_base_url"
            )

        # Save button
        if st.sidebar.button("Save Settings", type="primary", key="save_settings"):
            self.save_provider_config(selected_provider, updated_config)
            st.sidebar.success("Settings saved!")
            st.rerun()

        # Validation status
        is_valid, error_msg = self.validate_provider_config(selected_provider)
        if not is_valid:
            st.sidebar.warning(error_msg)
        else:
            st.sidebar.success("Configuration valid")

        return selected_provider, is_valid