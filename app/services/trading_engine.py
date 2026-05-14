from typing import Dict, List
from sqlalchemy.orm import Session
from app.ai_signals import AISignalAggregator
from app.market_data import MarketDataProvider
from app.models import AISignal, TradeOrder
from app.notifications import NotificationService
from app.risk_manager import RiskManager

class TradingEngine:
    def __init__(self, session: Session, broker, market_data: MarketDataProvider, notifier: NotificationService, portfolio_value: float = 4000.0):
        self.session = session
        self.broker = broker
        self.market_data = market_data
        self.notifier = notifier
        self.risk_manager = RiskManager(portfolio_value)
        self.signal_aggregator = AISignalAggregator()

    def generate_signals(self, symbol_universe: List[str]) -> List[Dict]:
        return self.signal_aggregator.generate_all_signals(symbol_universe)

    def persist_signal(self, signal: Dict) -> None:
        entry = AISignal(
            model_id=0,
            symbol=signal.get("symbol", ""),
            direction=signal.get("direction", "buy"),
            rationale=signal.get("rationale", ""),
            confidence=signal.get("confidence"),
            payload=signal,
        )
        self.session.add(entry)

    def execute_signal(self, signal: Dict) -> Dict:
        last_price = self.market_data.get_latest_price(signal["symbol"])
        quantity = self.risk_manager.allocation_for_order(last_price)
        if quantity <= 0:
            return {"status": "skipped", "reason": "zero quantity or price unavailable"}

        order = self.broker.place_order(
            symbol=signal["symbol"],
            qty=quantity,
            side=signal["direction"],
            order_type="market",
            time_in_force="day",
        )

        trade = TradeOrder(
            ai_model=signal["ai_model"],
            symbol=signal["symbol"],
            side=signal["direction"],
            quantity=quantity,
            price=last_price,
            status="filled",
            broker="alpaca",
            broker_order_id=order.get("id"),
            payload=order,
        )
        self.session.add(trade)
        self.session.commit()

        self.notifier.send_email(
            self.notifier.from_address,
            f"Trade executed: {signal['symbol']} {signal['direction']}",
            f"Executed {signal['direction']} order for {quantity} {signal['symbol']} at approx. ${last_price}.",
        )

        return {"status": "executed", "order": order}

    def run_daily_strategy(self, symbol_universe: List[str]) -> List[Dict]:
        signals = self.generate_signals(symbol_universe)
        results = []
        for signal in signals:
            self.persist_signal(signal)
            results.append(self.execute_signal(signal))
        self.session.commit()
        return results
