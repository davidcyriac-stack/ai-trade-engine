# API Documentation

## Base URL
```
https://ai-trade-engine.vercel.app
```

## Authentication
All endpoints require proper environment variable configuration for broker APIs and database access.

## Endpoints

### Health & Status

#### GET /health
Basic health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

#### GET /api/health
Detailed system health check.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "broker": "connected",
  "scheduler": "running",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### AI Signals

#### GET /api/ai/signals
Retrieve current AI-generated trading signals.

**Query Parameters:**
- `symbol` (optional): Filter by specific symbol
- `limit` (optional): Number of signals to return (default: 50)

**Response:**
```json
{
  "signals": [
    {
      "id": 1,
      "model_id": 1,
      "symbol": "AAPL",
      "direction": "BUY",
      "rationale": "Strong technical breakout with positive momentum",
      "confidence": 0.85,
      "payload": {
        "rsi": 65.2,
        "macd": 1.23,
        "volume": 45230000
      },
      "created_at": "2024-01-15T09:30:00Z"
    }
  ],
  "total": 10
}
```

### Trading Operations

#### GET /api/trades
List all trade orders with filtering options.

**Query Parameters:**
- `status` (optional): Filter by status (pending, executed, cancelled)
- `symbol` (optional): Filter by symbol
- `limit` (optional): Number of trades to return (default: 100)
- `offset` (optional): Pagination offset (default: 0)

**Response:**
```json
{
  "trades": [
    {
      "id": 1,
      "ai_model": "claude-3",
      "symbol": "AAPL",
      "side": "BUY",
      "quantity": 100,
      "price": 185.50,
      "status": "executed",
      "broker": "alpaca",
      "broker_order_id": "order_12345",
      "created_at": "2024-01-15T09:35:00Z",
      "executed_at": "2024-01-15T09:35:15Z"
    }
  ],
  "total": 25,
  "page": 1,
  "pages": 3
}
```

#### POST /api/trades/run
Manually trigger the daily trading strategy execution.

**Request Body:**
```json
{
  "dry_run": false,
  "symbols": ["AAPL", "MSFT", "GOOG"],
  "max_positions": 5
}
```

**Response:**
```json
{
  "status": "executed",
  "orders_placed": 3,
  "orders": [
    {
      "symbol": "AAPL",
      "side": "BUY",
      "quantity": 50,
      "price": 185.50
    }
  ],
  "execution_time": "2.3s"
}
```

#### GET /api/trades/{trade_id}
Get detailed information about a specific trade.

**Response:**
```json
{
  "id": 1,
  "ai_model": "claude-3",
  "symbol": "AAPL",
  "side": "BUY",
  "quantity": 100,
  "price": 185.50,
  "status": "executed",
  "broker": "alpaca",
  "broker_order_id": "order_12345",
  "fees": 0.50,
  "pnl": 125.00,
  "created_at": "2024-01-15T09:35:00Z",
  "executed_at": "2024-01-15T09:35:15Z",
  "updated_at": "2024-01-15T16:00:00Z"
}
```

### Positions

#### GET /api/positions
Get current portfolio positions.

**Query Parameters:**
- `broker` (optional): Filter by broker (alpaca, ibkr)

**Response:**
```json
{
  "positions": [
    {
      "symbol": "AAPL",
      "quantity": 100,
      "avg_price": 180.25,
      "current_price": 185.50,
      "market_value": 18550.00,
      "unrealized_pnl": 525.00,
      "unrealized_pnl_percent": 2.91,
      "broker": "alpaca",
      "updated_at": "2024-01-15T16:00:00Z"
    }
  ],
  "total_value": 18550.00,
  "total_pnl": 525.00,
  "total_pnl_percent": 2.91
}
```

#### GET /api/positions/{symbol}
Get position details for a specific symbol.

**Response:**
```json
{
  "symbol": "AAPL",
  "quantity": 100,
  "avg_price": 180.25,
  "current_price": 185.50,
  "market_value": 18550.00,
  "unrealized_pnl": 525.00,
  "unrealized_pnl_percent": 2.91,
  "day_change": 2.15,
  "day_change_percent": 1.19,
  "broker": "alpaca",
  "last_updated": "2024-01-15T16:00:00Z"
}
```

### Dashboard & Analytics

#### GET /api/dashboard/summary
Get portfolio summary and key metrics.

**Response:**
```json
{
  "portfolio_value": 125000.00,
  "cash_balance": 25000.00,
  "day_pnl": 1250.50,
  "day_pnl_percent": 1.02,
  "total_pnl": 8750.25,
  "total_pnl_percent": 7.53,
  "positions_count": 8,
  "winning_positions": 6,
  "losing_positions": 2,
  "last_updated": "2024-01-15T16:00:00Z"
}
```

#### GET /api/dashboard/stats
Get detailed trading statistics.

**Response:**
```json
{
  "total_trades": 156,
  "winning_trades": 98,
  "losing_trades": 58,
  "win_rate": 62.82,
  "avg_win": 245.50,
  "avg_loss": -185.75,
  "profit_factor": 1.85,
  "max_drawdown": -1250.00,
  "sharpe_ratio": 1.23,
  "volatility": 15.2,
  "period": "30d"
}
```

#### GET /api/dashboard/performance
Get performance metrics over time.

**Query Parameters:**
- `period` (optional): Time period (1d, 7d, 30d, 90d, 1y)

**Response:**
```json
{
  "performance": [
    {
      "date": "2024-01-15",
      "portfolio_value": 125000.00,
      "pnl": 1250.50,
      "pnl_percent": 1.02
    }
  ],
  "period": "30d",
  "total_return": 7.53,
  "annualized_return": 15.2,
  "volatility": 12.8
}
```

### Broker Integration

#### GET /api/broker/account
Get broker account information.

**Response:**
```json
{
  "broker": "alpaca",
  "account_id": "acc_12345",
  "status": "ACTIVE",
  "cash": 25000.00,
  "portfolio_value": 125000.00,
  "buying_power": 50000.00,
  "daytrade_count": 2,
  "last_updated": "2024-01-15T16:00:00Z"
}
```

#### GET /api/broker/positions
Get current positions from broker.

**Response:**
```json
{
  "positions": [
    {
      "symbol": "AAPL",
      "quantity": 100,
      "side": "long",
      "avg_price": 180.25,
      "current_price": 185.50,
      "market_value": 18550.00,
      "unrealized_pnl": 525.00,
      "unrealized_pnl_percent": 2.91
    }
  ],
  "broker": "alpaca"
}
```

#### POST /api/broker/order
Place a new order.

**Request Body:**
```json
{
  "symbol": "AAPL",
  "side": "buy",
  "quantity": 50,
  "order_type": "market",
  "time_in_force": "day"
}
```

**Response:**
```json
{
  "order_id": "order_12345",
  "status": "accepted",
  "symbol": "AAPL",
  "side": "buy",
  "quantity": 50,
  "price": 185.50,
  "broker": "alpaca",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Market Data

#### GET /api/market/quote/{symbol}
Get real-time quote for a symbol.

**Response:**
```json
{
  "symbol": "AAPL",
  "bid": 185.45,
  "ask": 185.50,
  "last": 185.47,
  "volume": 45230000,
  "timestamp": "2024-01-15T16:00:00Z"
}
```

#### GET /api/market/bars
Get historical bars for a symbol.

**Query Parameters:**
- `symbol` (required): Stock symbol
- `start` (optional): Start date (YYYY-MM-DD)
- `end` (optional): End date (YYYY-MM-DD)
- `timeframe` (optional): Bar timeframe (1Min, 5Min, 1D)

**Response:**
```json
{
  "symbol": "AAPL",
  "timeframe": "1D",
  "bars": [
    {
      "timestamp": "2024-01-15T16:00:00Z",
      "open": 182.50,
      "high": 186.25,
      "low": 181.80,
      "close": 185.50,
      "volume": 45230000
    }
  ]
}
```

### Risk Management

#### GET /api/risk/limits
Get current risk limits and usage.

**Response:**
```json
{
  "max_position_size": 10000.00,
  "max_portfolio_risk": 5000.00,
  "max_daily_loss": 2500.00,
  "max_concentration": 0.20,
  "current_portfolio_risk": 1250.00,
  "current_daily_loss": 350.00,
  "risk_status": "normal"
}
```

#### POST /api/risk/assess
Assess risk for a potential trade.

**Request Body:**
```json
{
  "symbol": "AAPL",
  "quantity": 100,
  "price": 185.50,
  "side": "buy"
}
```

**Response:**
```json
{
  "approved": true,
  "risk_score": 2.1,
  "position_size": 18550.00,
  "portfolio_impact": 0.15,
  "concentration": 0.12,
  "stop_loss_price": 175.00,
  "reasons": []
}
```

## Error Responses

All endpoints return standardized error responses:

```json
{
  "error": "ErrorType",
  "message": "Human-readable error message",
  "details": {
    "field": "specific_field",
    "value": "invalid_value"
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Rate Limits

- API calls are limited to 100 requests per minute per IP
- Broker API calls respect their respective rate limits
- Market data endpoints have higher limits during market hours

## WebSocket Support

Real-time updates are available via WebSocket:

```
ws://ai-trade-engine.vercel.app/ws/market/{symbol}
ws://ai-trade-engine.vercel.app/ws/portfolio
ws://ai-trade-engine.vercel.app/ws/signals
```

## SDK Examples

### Python
```python
import requests

# Get health status
response = requests.get("https://ai-trade-engine.vercel.app/health")
print(response.json())

# Get trading signals
response = requests.get("https://ai-trade-engine.vercel.app/api/ai/signals")
signals = response.json()
```

### JavaScript
```javascript
// Fetch signals
fetch('https://ai-trade-engine.vercel.app/api/ai/signals')
  .then(response => response.json())
  .then(data => console.log(data));

// WebSocket connection
const ws = new WebSocket('ws://ai-trade-engine.vercel.app/ws/market/AAPL');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Real-time quote:', data);
};
```

### cURL
```bash
# Health check
curl https://ai-trade-engine.vercel.app/health

# Get signals
curl https://ai-trade-engine.vercel.app/api/ai/signals

# Place order
curl -X POST https://ai-trade-engine.vercel.app/api/broker/order \
  -H "Content-Type: application/json" \
  -d '{"symbol":"AAPL","side":"buy","quantity":10,"order_type":"market"}'
```