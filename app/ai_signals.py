import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from app.config import CLAUDE_API_KEY, GEMINI_API_KEY, GROK_API_KEY, OPENAI_API_KEY

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

try:
    import openai
except ImportError:
    openai = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from xai import Client as GrokClient
except ImportError:
    GrokClient = None


class AIService(ABC):
    def __init__(self, api_key: str, model_name: str, provider_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self.provider_name = provider_name

    @abstractmethod
    def generate_signals(self, symbol_universe: List[str]) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    def parse_response(self, response_text: str) -> List[Dict[str, Any]]:
        try:
            parsed = json.loads(response_text)
            if isinstance(parsed, list):
                return [self.normalize_signal(item) for item in parsed if isinstance(item, dict)]
        except json.JSONDecodeError:
            pass

        signals = []
        for line in response_text.splitlines():
            if not line.strip():
                continue
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                symbol, direction, rationale = parts[0], parts[1], parts[2]
                signals.append({
                    "ai_model": self.provider_name,
                    "symbol": symbol.upper(),
                    "direction": direction.lower(),
                    "confidence": None,
                    "rationale": rationale,
                })
        return signals

    def normalize_signal(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "ai_model": raw.get("ai_model", self.provider_name),
            "symbol": raw.get("symbol", "").upper(),
            "direction": raw.get("direction", "buy").lower(),
            "confidence": raw.get("confidence"),
            "rationale": raw.get("rationale", ""),
        }

    def build_trade_prompt(self, symbol_universe: List[str]) -> str:
        return (
            "You are an institutional equities analyst. Review the following symbol universe and return a JSON array of top intraday entry signals. "
            "For each symbol, include symbol, direction (buy/sell), confidence (0-1), and a short rationale. "
            "Focus on US equities and prefer technical breakouts with volume confirmation. "
            f"Universe: {', '.join(symbol_universe)}"
        )


class ClaudeAI(AIService):
    def __init__(self):
        super().__init__(CLAUDE_API_KEY, "claude-3.5", "Claude")

    def generate_signals(self, symbol_universe: List[str]) -> List[Dict[str, Any]]:
        if not self.api_key or Anthropic is None:
            return []

        client = Anthropic(api_key=self.api_key)
        prompt = self.build_trade_prompt(symbol_universe)
        response = client.completions.create(
            model=self.model_name,
            prompt=f"\n\nHuman: {prompt}\n\nAssistant:",
            max_tokens_to_sample=350,
            temperature=0.2,
        )
        return self.parse_response(response.completion)


class ChatGPTAI(AIService):
    def __init__(self):
        super().__init__(OPENAI_API_KEY, "gpt-4o-mini", "ChatGPT")
        if openai is not None:
            openai.api_key = self.api_key

    def generate_signals(self, symbol_universe: List[str]) -> List[Dict[str, Any]]:
        if not self.api_key or openai is None:
            return []

        prompt = self.build_trade_prompt(symbol_universe)
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a highly accurate equity trading analyst."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=400,
            temperature=0.2,
        )
        text = response.choices[0].message["content"]
        return self.parse_response(text)


class GeminiAI(AIService):
    def __init__(self):
        super().__init__(GEMINI_API_KEY, "gemini-1.5-mini", "Gemini")
        if genai is not None:
            genai.configure(api_key=self.api_key)

    def generate_signals(self, symbol_universe: List[str]) -> List[Dict[str, Any]]:
        if not self.api_key or genai is None:
            return []

        prompt = self.build_trade_prompt(symbol_universe)
        response = genai.chat.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.last if hasattr(response, "last") else str(response)
        return self.parse_response(text)


class GrokAI(AIService):
    def __init__(self):
        super().__init__(GROK_API_KEY, "grok-1", "Grok")

    def generate_signals(self, symbol_universe: List[str]) -> List[Dict[str, Any]]:
        if not self.api_key or GrokClient is None:
            return []

        client = GrokClient(api_key=self.api_key)
        response = client.generate(prompt=self.build_trade_prompt(symbol_universe))
        text = response.text if hasattr(response, "text") else str(response)
        return self.parse_response(text)


class AISignalAggregator:
    def __init__(self):
        self.services = [ClaudeAI(), ChatGPTAI(), GeminiAI(), GrokAI()]

    def generate_all_signals(self, symbol_universe: List[str]) -> List[Dict[str, Any]]:
        signals: List[Dict[str, Any]] = []
        for service in self.services:
            signals.extend(service.generate_signals(symbol_universe))
        return signals
