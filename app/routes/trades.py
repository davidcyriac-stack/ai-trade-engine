from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import TradeOrder
from app.schemas import TradeOrderSchema
from app.config import (
    ALPACA_API_KEY,
    ALPACA_API_SECRET,
    ALPACA_BASE_URL,
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASS,
    SMTP_FROM,
    DEFAULT_NOTIFICATION_EMAIL,
)
from app.broker import AlpacaBroker
from app.market_data import MarketDataProvider
from app.notifications import NotificationService
from app.services.trading_engine import TradingEngine

router = APIRouter()

SYMBOL_UNIVERSE = ["AAPL", "MSFT", "GOOG", "AMZN", "NVDA", "META", "TSLA", "PYPL", "CRM", "CSCO"]

@router.get("/", response_model=list[TradeOrderSchema])
def list_trades(db: Session = Depends(get_db)):
    return db.query(TradeOrder).order_by(TradeOrder.created_at.desc()).all()

@router.post("/run")
def run_trading_strategy(db: Session = Depends(get_db)):
    if not ALPACA_API_KEY or not ALPACA_API_SECRET:
        raise HTTPException(status_code=500, detail="Alpaca API credentials are not configured")

    broker = AlpacaBroker.create(ALPACA_API_KEY, ALPACA_API_SECRET, ALPACA_BASE_URL)
    market_data = MarketDataProvider(broker.data_client)
    notifier = NotificationService(
        smtp_host=SMTP_HOST,
        smtp_port=SMTP_PORT,
        username=SMTP_USER,
        password=SMTP_PASS,
        from_address=SMTP_FROM,
    )

    engine = TradingEngine(
        session=db,
        broker=broker,
        market_data=market_data,
        notifier=notifier,
        portfolio_value=4000.0,
    )
    results = engine.run_daily_strategy(SYMBOL_UNIVERSE)
    return {"results": results}
