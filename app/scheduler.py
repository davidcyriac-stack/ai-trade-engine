from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
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
from app.db import SessionLocal
from app.broker import AlpacaBroker
from app.market_data import MarketDataProvider
from app.notifications import NotificationService
from app.services.trading_engine import TradingEngine

SYMBOL_UNIVERSE = ["AAPL", "MSFT", "GOOG", "AMZN", "NVDA", "META", "TSLA", "PYPL", "CRM", "CSCO"]

scheduler = AsyncIOScheduler(timezone=pytz.timezone("US/Eastern"))


def run_daily_signal_job():
    if not ALPACA_API_KEY or not ALPACA_API_SECRET:
        print("Skipping daily signal job because Alpaca credentials are not configured.")
        return

    broker = AlpacaBroker.create(ALPACA_API_KEY, ALPACA_API_SECRET, ALPACA_BASE_URL)
    market_data = MarketDataProvider(broker.data_client)
    notifier = NotificationService(
        smtp_host=SMTP_HOST,
        smtp_port=SMTP_PORT,
        username=SMTP_USER,
        password=SMTP_PASS,
        from_address=SMTP_FROM,
    )

    with SessionLocal() as session:
        engine = TradingEngine(
            session=session,
            broker=broker,
            market_data=market_data,
            notifier=notifier,
            portfolio_value=4000.0,
        )
        results = engine.run_daily_strategy(SYMBOL_UNIVERSE)
        print("Daily signal job completed", results)


def init_scheduler():
    scheduler.add_job(
        run_daily_signal_job,
        CronTrigger(hour=9, minute=0, timezone="US/Eastern"),
        id="daily_signal_job",
        replace_existing=True,
    )
    scheduler.start()
