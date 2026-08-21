"""
Unit tests for LLMClient multi-provider fallback chain (ADR-0001).
"""

from unittest.mock import patch, MagicMock
import pytest
from src.pipelines.llm_client import LLMClient


def test_llm_client_initialization():
    client = LLMClient(
        gemini_model="gemini-1.5-flash",
        groq_model="llama-3.1-8b-instant",
        temperature=0.3,
    )
    assert client.gemini_model_name == "gemini-1.5-flash"
    assert client.groq_model_name == "llama-3.1-8b-instant"
    assert client.temperature == 0.3


def test_llm_client_offline_fallback():
    # Initialize client without API keys to trigger offline fallback
    client = LLMClient()
    client.gemini_api_key = ""
    client.groq_api_key = ""

    prompt = (
        "Context Information:\n"
        "Q: How do I request a refund?\n"
        "A: You can request a refund in Billing Settings.\n\n"
        "User Question: I want a refund"
    )

    response, provider = client.invoke(prompt=prompt, system_message="Billing support")

    assert provider == "offline_fallback"
    assert "refund" in response.lower()
    assert "offline mode" in response.lower()


def test_llm_client_gemini_success():
    client = LLMClient()
    client.gemini_api_key = "fake_gemini_key"

    mock_resp = MagicMock()
    mock_resp.content = "Gemini generated answer: Check your billing portal."

    with patch.object(client, "_call_gemini", return_value=mock_resp.content) as mock_gemini:
        response, provider = client.invoke(prompt="How to get refund?", system_message="Billing")
        assert provider == "gemini"
        assert "Gemini generated answer" in response
        mock_gemini.assert_called_once()


def test_llm_client_groq_fallback_on_gemini_failure():
    client = LLMClient()
    client.gemini_api_key = "fake_gemini_key"
    client.groq_api_key = "fake_groq_key"

    # Simulate Gemini 429 RateLimitError, forcing fallback to Groq
    with patch.object(client, "_call_gemini", side_effect=Exception("429 ResourceExhausted")):
        with patch.object(client, "_call_groq", return_value="Groq generated fallback answer") as mock_groq:
            response, provider = client.invoke(prompt="How to get refund?")
            assert provider == "groq"
            assert "Groq generated fallback answer" in response
            mock_groq.assert_called_once()
