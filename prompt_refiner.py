import re
from typing import Tuple
from api_clients import LLMClient


class PromptRefiner:
    """Handles LLM prompt refinement using XML-structured inputs to produce clean, natural output."""

    SYSTEM_INSTRUCTION = """You are an expert communicator. Your task is to take a set of clarifying questions and the user's raw, unstructured answers, and transform them into a clear, well-structured response that directly answers those questions.

CRITICAL: Your response must start immediately with the actual answers. Do NOT include:
- Conversational greetings ("Sure, I'd be happy to help!")
- Explanatory lead-ins ("Here are the answers...")
- Meta-commentary about the task
- Any introductory phrases

Your response should:
- Start directly with the refined answers
- Be well-organized and address each question clearly
- Use the user's intended meaning from their raw responses
- Sound natural but get straight to the point
- NOT be wrapped in quotation marks
- NOT include any conversational fluff

Simply provide the refined, direct answers that can be immediately pasted back to the original AI."""

    def __init__(self, llm_client: LLMClient):
        """Initialize the prompt refiner with an LLM client."""
        self.llm_client = llm_client

    def _create_user_query(self, clarifying_questions: str, raw_responses: str) -> str:
        """Create the formatted user query for the refiner model."""
        return f"""<clarifying_questions>
{clarifying_questions.strip()}
</clarifying_questions>
<raw_user_responses>
{raw_responses.strip()}
</raw_user_responses>

Please transform the raw responses into clear, direct answers to the clarifying questions. The output should be a natural response that I can paste back to the AI who asked these questions - not instructions about what to write, but actual answers formatted appropriately."""

    def _clean_response(self, response: str) -> str:
        """Clean and format the LLM response."""
        # Remove any XML tags if present (fallback for models that might still use them)
        cleaned = re.sub(r'<[^>]+>', '', response)

        # Remove surrounding quotation marks if present
        cleaned = cleaned.strip()
        if (cleaned.startswith('"') and cleaned.endswith('"')) or (cleaned.startswith("'") and cleaned.endswith("'")):
            cleaned = cleaned[1:-1].strip()

        # Remove common conversational lead-ins
        lead_in_patterns = [
            r'^Sure,?\s*I\'?d be happy to help!?\s*',
            r'^Here are the answers?.*?(?:to the clarifying questions?)?.*?:\s*',
            r'^Based on.*?responses?:?\s*',
            r'^I\'ll help.*?questions?:?\s*',
            r'^Let me.*?questions?:?\s*',
            r'^I can help.*?:\s*',
            r'^Certainly!?\s*',
            r'^Of course!?\s*',
            r'^Here\'s what.*?:\s*',
            r'^Here\'s my response.*?:\s*',
            r'^Here are the.*?based on.*?:\s*'
        ]

        for pattern in lead_in_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE | re.MULTILINE)

        # Clean up whitespace
        cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned.strip())

        return cleaned

    def refine_prompt(self, clarifying_questions: str, raw_responses: str) -> str:
        """
        Refine the prompt using the LLM.

        Args:
            clarifying_questions: The AI's original list of queries
            raw_responses: The user's unstructured answers

        Returns:
            The refined prompt as clean, natural text

        Raises:
            Exception: If refinement fails for any reason
        """
        if not clarifying_questions.strip():
            raise ValueError("Clarifying questions cannot be empty")

        if not raw_responses.strip():
            raise ValueError("User responses cannot be empty")

        try:
            # Create the user query for the refiner model
            user_query = self._create_user_query(clarifying_questions, raw_responses)

            # Call the LLM
            response = self.llm_client.generate_response(
                system_prompt=self.SYSTEM_INSTRUCTION,
                user_prompt=user_query
            )

            if not response or not response.strip():
                raise Exception("LLM returned empty response")

            # Clean and return the response
            cleaned_response = self._clean_response(response)

            if not cleaned_response or len(cleaned_response.strip()) < 20:
                raise Exception("LLM response appears to be too short or empty after cleaning")

            return cleaned_response

        except ValueError as e:
            # Re-raise input validation errors
            raise e
        except Exception as e:
            # Wrap other errors with context
            raise Exception(f"Prompt refinement failed: {str(e)}")

    def validate_inputs(self, clarifying_questions: str, raw_responses: str) -> Tuple[bool, str]:
        """
        Validate the inputs before processing.

        Args:
            clarifying_questions: The AI's questions
            raw_responses: The user's responses

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not clarifying_questions or not clarifying_questions.strip():
            return False, "Clarifying questions are required"

        if not raw_responses or not raw_responses.strip():
            return False, "User responses are required"

        # Check minimum length requirements
        if len(clarifying_questions.strip()) < 10:
            return False, "Clarifying questions seem too short"

        if len(raw_responses.strip()) < 10:
            return False, "User responses seem too short"

        return True, ""

    def preview_refinement_input(self, clarifying_questions: str, raw_responses: str) -> str:
        """
        Preview what will be sent to the LLM for refinement.

        Args:
            clarifying_questions: The AI's questions
            raw_responses: The user's responses

        Returns:
            The formatted input that will be sent to the LLM
        """
        return self._create_user_query(clarifying_questions, raw_responses)