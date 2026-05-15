# 🚀 AI Trade Engine Backend

A production-ready Python FastAPI backend for an AI-driven US market trading engine with PostgreSQL, APScheduler, multi-broker APIs (Alpaca, Interactive Brokers), and real-time market data streaming.

## ✨ Features

### Core Architecture
- **FastAPI Framework** - High-performance async REST API with automatic OpenAPI docs
- **PostgreSQL Database** - Production-ready relational database with SQLAlchemy ORM
- **APScheduler** - Background job scheduling for automated trading execution
- **CORS Support** - Cross-origin requests enabled for frontend integration

### Trading & Broker Integration
- **Multi-Broker Support** - Alpaca (primary) and Interactive Brokers (fallback)
- **Real-time Market Data** - Live streaming from Alpaca with Yahoo Finance fallback
- **AI Signal Generation** - Claude, OpenAI, Gemini, and Grok integration
- **Risk Management** - Stop-loss, position sizing, concentration limits
- **Order Execution** - Automated trade placement with error handling

### Data & Analytics
- **Technical Analysis** - Breakout detection, RSI, MACD, moving averages
- **Market Data Streaming** - Real-time quotes, bars, and trade data
- **Portfolio Tracking** - Position monitoring and P&L calculation
- **Trade History** - Complete audit trail of all transactions

### Infrastructure
- **Vercel Deployment** - Serverless deployment with automatic scaling
- **Environment Configuration** - Secure API key management
- **Health Monitoring** - Comprehensive system health checks
- **Email Notifications** - SMTP-based trade alerts and system notifications

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │    │   FastAPI API   │    │   PostgreSQL    │
│   (Dashboard)   │◄──►│   (Endpoints)   │◄──►│   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                    ┌─────────────────┐
                    │   APScheduler  │
                    │ (Background Jobs)│
                    └─────────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
            ┌───────▼──────┐  ┌──────▼──────┐
            │   Alpaca     │  │ Interactive │
            │   Broker     │  │   Brokers   │
            └──────────────┘  └─────────────┘
                    │                 │
            ┌───────▼───────────────▼──────┐
            │        Market Data APIs      │
            │   (Real-time Streaming)      │
            └──────────────────────────────┘
```

## 🚀 Quick Start

### Local Development

1. **Clone and Setup**
   ```bash
   git clone https://github.com/davidcyriac-stack/ai-trade-engine.git
   cd ai-trade-engine
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Database Setup**
   ```bash
   # For local PostgreSQL
   createdb ai_trade_engine
   export DATABASE_URL="postgresql://user:password@localhost/ai_trade_engine"
   ```

4. **Run the Application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the Dashboard**
   - Dashboard: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Vercel Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial deployment"
   git push origin main
   ```

2. **Deploy on Vercel**
   - Connect GitHub repository to Vercel
   - Vercel will auto-detect Python project
   - Add environment variables in Vercel dashboard

3. **Database Setup**
   - Create Vercel Postgres database
   - Add `DATABASE_URL` environment variable

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `ALPACA_API_KEY` | Alpaca trading API key | Yes |
| `ALPACA_API_SECRET` | Alpaca trading API secret | Yes |
| `ALPACA_BASE_URL` | Alpaca API base URL | No (defaults to paper) |
| `CLAUDE_API_KEY` | Anthropic Claude API key | No |
| `OPENAI_API_KEY` | OpenAI API key | No |
| `GEMINI_API_KEY` | Google Gemini API key | No |
| `GROK_API_KEY` | xAI Grok API key | No |
| `IBKR_USERNAME` | Interactive Brokers username | No |
| `IBKR_PASSWORD` | Interactive Brokers password | No |
| `SMTP_HOST` | Email SMTP host | No |
| `SMTP_PORT` | Email SMTP port | No |
| `SMTP_USER` | Email SMTP username | No |
| `SMTP_PASS` | Email SMTP password | No |
| `SMTP_FROM` | Email from address | No |
| `DEFAULT_NOTIFICATION_EMAIL` | Default notification email | No |

### Database Schema

The application uses the following main models:

- **AIModel** - AI model configurations
- **AISignal** - Trading signals generated by AI
- **TradeOrder** - Executed trade orders
- **Position** - Current portfolio positions

## 📡 API Endpoints

### Health & Status
- `GET /health` - Service health check
- `GET /api/health` - Detailed health status

### Trading Operations
- `GET /api/ai/signals` - Get current AI trading signals
- `POST /api/trades/run` - Execute trading strategy manually
- `GET /api/trades` - List all trade orders
- `GET /api/positions` - Get current positions

### Dashboard & Analytics
- `GET /api/dashboard/summary` - Portfolio summary
- `GET /api/dashboard/stats` - Trading statistics
- `GET /api/dashboard/performance` - Performance metrics

### Broker Integration
- `GET /api/broker/positions` - Current broker positions
- `GET /api/broker/account` - Account information
- `POST /api/broker/order` - Place new order

## 🔄 Background Jobs (APScheduler)

The application runs several scheduled jobs:

- **Daily Signal Generation** - 9:30 AM ET (market open)
- **Order Execution** - 9:35 AM ET
- **Position Monitoring** - Every 5 minutes during market hours
- **Risk Assessment** - Hourly during market hours
- **Database Cleanup** - Daily at midnight

## 🏦 Broker Integration

### Alpaca Broker
- Primary broker for paper/live trading
- Real-time market data streaming
- Commission-free trading
- REST and WebSocket APIs

### Interactive Brokers
- Fallback broker for advanced features
- Institutional-grade execution
- Global market access
- Advanced order types

## 🤖 AI Integration

Supports multiple AI models for signal generation:

- **Claude (Anthropic)** - Primary AI model
- **GPT-4 (OpenAI)** - Alternative model
- **Gemini (Google)** - Backup model
- **Grok (xAI)** - Experimental model

## 📊 Real-time Data Streaming

- **Stock Quotes** - Real-time bid/ask prices
- **Trade Data** - Live trade executions
- **Market Bars** - 1-minute, 5-minute, daily bars
- **News Integration** - Market news and sentiment

## 🛡️ Risk Management

- **Position Sizing** - Risk-based position allocation
- **Stop Loss** - Automatic loss protection
- **Concentration Limits** - Maximum exposure per symbol
- **Daily Loss Limits** - Portfolio-level risk controls
- **Volatility Filters** - Avoid high-volatility periods

## 📧 Notifications

- **Email Alerts** - Trade executions and errors
- **System Notifications** - Health checks and warnings
- **Customizable Recipients** - Multiple email addresses
- **SMTP Configuration** - Flexible email provider support

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_trading.py
```

## 📈 Monitoring & Logging

- **Structured Logging** - JSON-formatted logs
- **Health Endpoints** - System status monitoring
- **Performance Metrics** - Response times and error rates
- **Database Monitoring** - Connection pool and query performance

## 🔒 Security

- **API Key Management** - Secure environment variable storage
- **Input Validation** - Pydantic model validation
- **Rate Limiting** - Request throttling protection
- **CORS Configuration** - Cross-origin request control

## 🚀 Deployment Options

### Vercel (Recommended)
- Serverless deployment
- Automatic scaling
- Built-in CDN
- PostgreSQL integration

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes
- Helm charts available in `k8s/` directory
- Horizontal Pod Autoscaling
- ConfigMap and Secret management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or issues:
- Create an issue on GitHub
- Check the documentation
- Review the API documentation at `/docs`

---

**Live Demo:** https://ai-trade-engine.vercel.app
**API Docs:** https://ai-trade-engine.vercel.app/docs
**Repository:** https://github.com/davidcyriac-stack/ai-trade-engine

This backend is built for US market hours (9:30 AM ET to 4:00 PM ET) with DST support.
