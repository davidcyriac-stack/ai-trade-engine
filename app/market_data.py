from typing import Dict, List, Optional

import pandas as pd
import yfinance as yf
from alpaca.data import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

class MarketDataProvider:
    def __init__(self, alpaca_data_client: Optional[StockDataClient] = None):
        self.alpaca_data_client = alpaca_data_client

    def get_historical_bars(self, symbol: str, start: str, end: str, timeframe: str = "1D") -> Dict:
        if self.alpaca_data_client:
            tf = TimeFrame.Day if timeframe == "1D" else TimeFrame.Minute
            request = StockBarsRequest(symbol_or_symbols=[symbol], start=start, end=end, timeframe=tf)
            bars = self.alpaca_data_client.get_stock_bars(request)
            return {symbol: [bar._raw for bar in bars[symbol]]}

        return self.get_yahoo_history(symbol, period="6mo", interval="1d")

    def get_yahoo_history(self, symbol: str, period: str = "6mo", interval: str = "1d") -> Dict:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period=period, interval=interval)
        return history.reset_index().to_dict(orient="list")

    def get_latest_price(self, symbol: str) -> float:
        if self.alpaca_data_client:
            trade = self.alpaca_data_client.get_stock_latest_trade(symbol)
            return float(trade.price)

        history = self.get_yahoo_history(symbol, period="5d", interval="1d")
        if history.get("Close"):
            return float(history["Close"][-1])
        return 0.0

    def to_dataframe(self, history: Dict) -> pd.DataFrame:
        return pd.DataFrame(history)
