from typing import Dict, Optional

from alpaca.trading.client import TradingClient
from alpaca.data import StockHistoricalDataClient

class BrokerInterface:
    def place_order(self, symbol: str, qty: int, side: str, order_type: str = "market", time_in_force: str = "day") -> Dict:
        raise NotImplementedError()

    def get_positions(self) -> Dict:
        raise NotImplementedError()

    def get_market_data(self, symbol: str) -> Dict:
        raise NotImplementedError()

class AlpacaBroker(BrokerInterface):
    def __init__(self, trading_client: TradingClient, data_client: Optional[StockDataClient] = None):
        self.trading_client = trading_client
        self.data_client = data_client

    def place_order(self, symbol: str, qty: int, side: str, order_type: str = "market", time_in_force: str = "day") -> Dict:
        order = self.trading_client.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type=order_type,
            time_in_force=time_in_force,
        )
        return order._raw if hasattr(order, "_raw") else order.__dict__

    def get_positions(self) -> Dict:
        positions = self.trading_client.get_all_positions()
        return [p._raw if hasattr(p, "_raw") else p.__dict__ for p in positions]

    def get_market_data(self, symbol: str) -> Dict:
        if self.data_client:
            trade = self.data_client.get_stock_latest_trade(symbol)
            return trade._raw if hasattr(trade, "_raw") else trade.__dict__
        return {}

    @staticmethod
    def create(key_id: str, secret_key: str, base_url: str):
        trading_client = TradingClient(key_id=key_id, secret_key=secret_key, paper=("paper" in base_url), base_url=base_url)
        data_client = StockHistoricalDataClient(key_id=key_id, secret_key=secret_key, base_url=base_url)
        return AlpacaBroker(trading_client=trading_client, data_client=data_client)

class IBroker(BrokerInterface):
    def __init__(self, ib):
        self.ib = ib

    def place_order(self, symbol: str, qty: int, side: str, order_type: str = "market", time_in_force: str = "day") -> Dict:
        # TODO: implement Interactive Brokers order placement via IB API
        return {}

    def get_positions(self) -> Dict:
        # TODO: implement IB position retrieval
        return {}

    def get_market_data(self, symbol: str) -> Dict:
        # TODO: implement IB market data retrieval
        return {}
