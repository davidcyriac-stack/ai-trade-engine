from fastapi import APIRouter
from app.ai_signals import AISignalAggregator

router = APIRouter()

SYMBOL_UNIVERSE = ["AAPL", "MSFT", "GOOG", "AMZN", "NVDA", "META", "TSLA", "PYPL", "CRM", "CSCO"]

@router.get("/signals")
def ai_signals():
    aggregator = AISignalAggregator()
    signals = aggregator.generate_all_signals(SYMBOL_UNIVERSE)
    return {"signals": signals}
