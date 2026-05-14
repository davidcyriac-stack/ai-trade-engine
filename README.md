# AI Trade Engine Backend

This project is a Python-based backend for an AI-driven US market trading engine.

Features:
- FastAPI REST API and WebSocket support
- Scheduled daily signal generation and order execution
- Alpaca primary broker integration, Interactive Brokers fallback
- Real-time market data streaming and technical breakout detection
- Risk management, stop-loss, concentration limits, and notification support

## Getting Started

1. Create a Python 3.11+ virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Configure `.env` with API keys and database URL
4. Run the app: `uvicorn app.main:app --reload`

## API Endpoints

- `GET /api/health` — service health check
- `GET /api/dashboard/summary` — current positions and recent trades
- `GET /api/trades` — list stored trade orders
- `POST /api/trades/run` — trigger daily strategy execution manually
- `GET /api/positions` — current position list

## Vercel Deployment

1. Create a new Git repository and push this project.
2. On Vercel, create a new project from Git.
3. Ensure environment variables are defined in Vercel for `DATABASE_URL`, `ALPACA_API_KEY`, `ALPACA_API_SECRET`, `ALPACA_BASE_URL`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM`, and `DEFAULT_NOTIFICATION_EMAIL`.
4. Vercel will use `vercel.json` and `runtime.txt` to deploy the Python app.

> Note: Vercel is a serverless environment, so the scheduler does not run continuously. Use an external cron job or Vercel Scheduled Functions to call `POST /api/trades/run` each market day.

## Project Structure

- `app/main.py` - FastAPI application
- `app/models.py` - SQLAlchemy models
- `app/ai_signals.py` - AI signal generation
- `app/broker.py` - Broker abstraction layer
- `app/risk_manager.py` - Risk rules and position sizing
- `app/technical_analysis.py` - Breakout and indicator logic
- `app/market_data.py` - Market data ingestion and streaming
- `app/scheduler.py` - APScheduler jobs
- `app/routes/` - API endpoints
- `app/notifications.py` - Email and in-app notifications

## Notes

This backend is built for US market hours (9:30 AM ET to 4:00 PM ET) with DST support.
