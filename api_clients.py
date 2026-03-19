import requests
import json
from openai import OpenAI
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class LLMClient(ABC):
    """Abstract base class for LLM API clients."""

    @abstractmethod
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a response from the LLM."""
        pass

    @abstractmethod
    def test_connection(self) -> tuple[bool, str]:
        """Test the connection to the LLM service."""
        pass


class OpenAIClient(LLMClient):
    """OpenAI API client."""

    # Models with parameter restrictions
    O1_MODELS = {'o1-preview', 'o1-mini', 'o1', 'o1-2024-12-17'}
    REASONING_MODELS = O1_MODELS | {'o3-mini', 'o3', 'gpt-5'}  # Add future reasoning models

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=api_key)

    def _is_reasoning_model(self) -> bool:
        """Check if the current model is a reasoning model with parameter restrictions."""
        return any(reasoning_model in self.model.lower() for reasoning_model in self.REASONING_MODELS)

    def _get_model_params(self, base_params: dict) -> dict:
        """Get appropriate parameters for the model, removing unsupported ones for reasoning models."""
        if self._is_reasoning_model():
            # Reasoning models only support specific parameters
            allowed_params = {'model', 'messages'}
            return {k: v for k, v in base_params.items() if k in allowed_params}
        return base_params

    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a response using OpenAI API."""
        try:
            # Base parameters
            base_params = {
                'model': self.model,
                'messages': [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            }

            # Add parameters based on model capabilities
            if not self._is_reasoning_model():
                base_params['temperature'] = 0.7
                # Try max_completion_tokens first, fallback to max_tokens
                try:
                    base_params['max_completion_tokens'] = 2000
                    response = self.client.chat.completions.create(**base_params)
                    return response.choices[0].message.content.strip()
                except Exception as e:
                    if "unsupported_parameter" in str(e).lower() and "max_completion_tokens" in str(e):
                        base_params.pop('max_completion_tokens')
                        base_params['max_tokens'] = 2000
                        response = self.client.chat.completions.create(**base_params)
                        return response.choices[0].message.content.strip()
                    else:
                        raise e
            else:
                # Reasoning models - use only supported parameters
                response = self.client.chat.completions.create(**base_params)
                return response.choices[0].message.content.strip()

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def test_connection(self) -> tuple[bool, str]:
        """Test the OpenAI API connection."""
        try:
            # Base parameters for testing
            base_params = {
                'model': self.model,
                'messages': [{"role": "user", "content": "Hello"}]
            }

            # Add parameters based on model capabilities
            if not self._is_reasoning_model():
                # Try max_completion_tokens first, fallback to max_tokens
                try:
                    base_params['max_completion_tokens'] = 10
                    response = self.client.chat.completions.create(**base_params)
                    return True, "Connection successful"
                except Exception as e:
                    if "unsupported_parameter" in str(e).lower() and "max_completion_tokens" in str(e):
                        base_params.pop('max_completion_tokens')
                        base_params['max_tokens'] = 10
                        response = self.client.chat.completions.create(**base_params)
                        return True, "Connection successful"
                    else:
                        raise e
            else:
                # Reasoning models - use only supported parameters
                response = self.client.chat.completions.create(**base_params)
                return True, "Connection successful"

        except Exception as e:
            return False, f"Connection failed: {str(e)}"


class OpenRouterClient(LLMClient):
    """OpenRouter API client."""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"

    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a response using OpenRouter API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8501",  # For OpenRouter
                "X-Title": "LLM Prompt Refinement Tool"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

            result = response.json()
            if "error" in result:
                raise Exception(f"API error: {result['error']['message']}")

            return result["choices"][0]["message"]["content"].strip()

        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenRouter request error: {str(e)}")
        except Exception as e:
            raise Exception(f"OpenRouter API error: {str(e)}")

    def test_connection(self) -> tuple[bool, str]:
        """Test the OpenRouter API connection."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8501",
                "X-Title": "LLM Prompt Refinement Tool"
            }

            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 10
            }

            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                return True, "Connection successful"
            else:
                return False, f"HTTP {response.status_code}: {response.text}"

        except Exception as e:
            return False, f"Connection failed: {str(e)}"


class OllamaClient(LLMClient):
    """Ollama API client."""

    def __init__(self, model: str, base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url.rstrip("/")

    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a response using Ollama API."""
        try:
            payload = {
                "model": self.model,
                "prompt": f"System: {system_prompt}\n\nUser: {user_prompt}\n\nAssistant:",
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 2000
                }
            }

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120
            )

            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

            result = response.json()
            if "error" in result:
                raise Exception(f"API error: {result['error']}")

            return result.get("response", "").strip()

        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama request error: {str(e)}")
        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}")

    def test_connection(self) -> tuple[bool, str]:
        """Test the Ollama API connection."""
        try:
            # First, check if Ollama is running
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)

            if response.status_code != 200:
                return False, f"Ollama server not reachable: HTTP {response.status_code}"

            # Check if the model is available
            models = response.json().get("models", [])
            model_names = [model.get("name", "") for model in models]

            if not any(self.model in name for name in model_names):
                return False, f"Model '{self.model}' not found. Available models: {', '.join(model_names)}"

            # Test a simple generation
            payload = {
                "model": self.model,
                "prompt": "Hello",
                "stream": False,
                "options": {"num_predict": 10}
            }

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                return True, "Connection successful"
            else:
                return False, f"Generation test failed: HTTP {response.status_code}"

        except Exception as e:
            return False, f"Connection failed: {str(e)}"


class APIClientFactory:
    """Factory class for creating LLM API clients."""

    @staticmethod
    def create_client(provider: str, config: Dict[str, Any]) -> LLMClient:
        """Create an LLM client based on the provider and configuration."""

        if provider == "OpenAI":
            api_key = config.get("api_key")
            model = config.get("model")

            if not api_key:
                raise ValueError("OpenAI API key is required")
            if not model:
                raise ValueError("OpenAI model is required")

            return OpenAIClient(api_key, model)

        elif provider == "OpenRouter":
            api_key = config.get("api_key")
            model = config.get("model")

            if not api_key:
                raise ValueError("OpenRouter API key is required")
            if not model:
                raise ValueError("OpenRouter model is required")

            return OpenRouterClient(api_key, model)

        elif provider == "Ollama":
            model = config.get("model")
            base_url = config.get("base_url", "http://localhost:11434")

            if not model:
                raise ValueError("Ollama model is required")

            return OllamaClient(model, base_url)

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    @staticmethod
    def test_client_connection(provider: str, config: Dict[str, Any]) -> tuple[bool, str]:
        """Test a client connection without creating a persistent client."""
        try:
            client = APIClientFactory.create_client(provider, config)
            return client.test_connection()
        except Exception as e:
            return False, f"Client creation failed: {str(e)}"