"""
LLM Client module with Multi-Provider Fallback Chain (ADR-0001).
Implements resilient triple-provider failover:
1. Google Gemini Free Tier (Primary)
2. Groq API (Fallback 1)
3. Offline Grounded Fallback (Fallback 2)
"""

import os
from typing import Any
from dotenv import load_dotenv
from src.config import env_path

# Load environment variables
load_dotenv(dotenv_path=env_path)


class LLMClient:
    """
    Multi-provider LLM client implementing the fallback chain per ADR-0001:
    - Primary: Google Gemini API (gemini-1.5-flash / gemini-2.0-flash)
    - Fallback 1: Groq API (llama-3.1-8b-instant / llama3-70b-8192)
    - Fallback 2: Offline deterministic grounded generation
    """

    def __init__(
        self,
        gemini_model: str = "gemini-1.5-flash",
        groq_model: str = "llama-3.1-8b-instant",
        temperature: float = 0.2,
    ):
        self.gemini_model_name = gemini_model
        self.groq_model_name = groq_model
        self.temperature = temperature

        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.groq_api_key = os.getenv("GROQ_API_KEY", "").strip()

    def _call_gemini(self, prompt: str, system_message: str = "") -> str:
        """
        Call Google Gemini via langchain-google-genai.
        """
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not configured in environment.")

        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.messages import SystemMessage, HumanMessage

        llm = ChatGoogleGenerativeAI(
            model=self.gemini_model_name,
            google_api_key=self.gemini_api_key,
            temperature=self.temperature,
        )

        messages = []
        if system_message:
            messages.append(SystemMessage(content=system_message))
        messages.append(HumanMessage(content=prompt))

        response = llm.invoke(messages)
        return str(response.content).strip()

    def _call_groq(self, prompt: str, system_message: str = "") -> str:
        """
        Call Groq via langchain-groq.
        """
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY is not configured in environment.")

        from langchain_groq import ChatGroq
        from langchain_core.messages import SystemMessage, HumanMessage

        llm = ChatGroq(
            model=self.groq_model_name,
            groq_api_key=self.groq_api_key,
            temperature=self.temperature,
        )

        messages = []
        if system_message:
            messages.append(SystemMessage(content=system_message))
        messages.append(HumanMessage(content=prompt))

        response = llm.invoke(messages)
        return str(response.content).strip()

    def _call_offline_fallback(self, prompt: str, system_message: str = "") -> str:
        """
        Offline deterministic fallback when cloud APIs are unavailable.
        Extracts answer context directly if present in prompt.
        """
        if "Context Information:" in prompt:
            # Extract and return the grounded context cleanly
            context_section = prompt.split("Context Information:")[-1].split("User Question:")[0].strip()
            return f"{context_section}\n\n(Note: Generated via local knowledge base in offline mode)."
        return "I apologize, but our AI service is currently operating in offline mode. Please refer to our help center or contact support directly."

    def invoke(self, prompt: str, system_message: str = "") -> tuple[str, str]:
        """
        Execute generation across the fallback chain.
        Returns tuple: (response_text, provider_used)
        """
        # 1. Primary: Google Gemini
        if self.gemini_api_key:
            try:
                response = self._call_gemini(prompt=prompt, system_message=system_message)
                return response, "gemini"
            except Exception as e:
                print(f"Warning: Primary LLM (Gemini) failed: {e}. Attempting Groq fallback...")
        else:
            print("Notice: GEMINI_API_KEY missing. Checking Groq fallback...")

        # 2. Fallback 1: Groq API
        if self.groq_api_key:
            try:
                response = self._call_groq(prompt=prompt, system_message=system_message)
                return response, "groq"
            except Exception as e:
                print(f"Warning: Fallback LLM (Groq) failed: {e}. Attempting offline fallback...")
        else:
            print("Notice: GROQ_API_KEY missing. Using offline fallback...")

        # 3. Fallback 2: Offline Fallback
        response = self._call_offline_fallback(prompt=prompt, system_message=system_message)
        return response, "offline_fallback"
