"""Unit tests for the pure functions in PromptRefiner.

These cover validate_inputs and _clean_response, neither of which needs an
LLM client, so the whole suite runs offline with no API calls.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prompt_refiner import PromptRefiner


@pytest.fixture
def refiner():
    # validate_inputs / _clean_response never touch the client, so None is fine.
    return PromptRefiner(None)


def test_ollama_client_uses_chat_api_and_disables_thinking(monkeypatch):
    # Thinking models return an empty 'response' under /api/generate and an
    # empty 'content' unless thinking is off — the exact failure seen on the
    # first real run against local Ollama.
    import api_clients

    captured = {}

    class FakeResponse:
        status_code = 200
        text = ""

        def json(self):
            return {"message": {"content": "  refined answer  "}}

    def fake_post(url, json=None, timeout=None):
        captured["url"] = url
        captured["payload"] = json
        return FakeResponse()

    monkeypatch.setattr(api_clients.requests, "post", fake_post)
    client = api_clients.OllamaClient("qwen3:4b")
    out = client.generate_response("be brief", "answer this")

    assert out == "refined answer"
    assert captured["url"].endswith("/api/chat")
    assert captured["payload"]["messages"] == [
        {"role": "system", "content": "be brief"},
        {"role": "user", "content": "answer this"},
    ]
    assert captured["payload"]["think"] is False


def test_clean_response_strips_think_blocks(refiner):
    messy = "<think>deliberating at length</think>\n\nThe actual answer."
    assert refiner._clean_response(messy) == "The actual answer."


# --- validate_inputs -------------------------------------------------------

def test_validate_inputs_happy_path(refiner):
    ok, msg = refiner.validate_inputs(
        "What is the target audience for this article?",
        "Beginners who have never seen machine learning before.",
    )
    assert ok is True
    assert msg == ""


def test_validate_inputs_empty_questions(refiner):
    ok, msg = refiner.validate_inputs("", "Some sufficiently long response text.")
    assert ok is False
    assert "Clarifying questions are required" in msg


def test_validate_inputs_whitespace_only_responses(refiner):
    ok, msg = refiner.validate_inputs("A real clarifying question here?", "   \n\t  ")
    assert ok is False
    assert "User responses are required" in msg


def test_validate_inputs_questions_too_short(refiner):
    ok, msg = refiner.validate_inputs("hi?", "This is a long enough response string.")
    assert ok is False
    assert "too short" in msg


def test_validate_inputs_responses_too_short(refiner):
    ok, msg = refiner.validate_inputs("What is the desired tone for this?", "short")
    assert ok is False
    assert "too short" in msg


# --- _clean_response -------------------------------------------------------

def test_clean_response_strips_surrounding_double_quotes(refiner):
    raw = '"The audience is beginners and the tone should be friendly."'
    cleaned = refiner._clean_response(raw)
    assert not cleaned.startswith('"')
    assert not cleaned.endswith('"')
    assert cleaned.startswith("The audience")


def test_clean_response_strips_surrounding_single_quotes(refiner):
    raw = "'The audience is beginners and the tone should be friendly.'"
    cleaned = refiner._clean_response(raw)
    assert not cleaned.startswith("'")
    assert not cleaned.endswith("'")


def test_clean_response_removes_sure_lead_in(refiner):
    raw = "Sure, I'd be happy to help! The audience is beginners."
    cleaned = refiner._clean_response(raw)
    assert cleaned == "The audience is beginners."


def test_clean_response_removes_here_are_the_answers_lead_in(refiner):
    raw = "Here are the answers to the clarifying questions: The tone is casual."
    cleaned = refiner._clean_response(raw)
    assert cleaned == "The tone is casual."


def test_clean_response_strips_xml_tags(refiner):
    raw = "<answer>The audience is beginners.</answer>"
    cleaned = refiner._clean_response(raw)
    assert "<" not in cleaned and ">" not in cleaned
    assert "The audience is beginners." in cleaned


def test_clean_response_collapses_blank_lines(refiner):
    raw = "First paragraph.\n\n\n\nSecond paragraph."
    cleaned = refiner._clean_response(raw)
    assert "\n\n\n" not in cleaned
    assert "First paragraph.\n\nSecond paragraph." == cleaned


def test_clean_response_leaves_clean_text_unchanged(refiner):
    raw = "The audience is beginners and the tone is friendly."
    cleaned = refiner._clean_response(raw)
    assert cleaned == raw
