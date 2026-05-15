# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AI Trade Engine Backend                      │
│                    FastAPI + PostgreSQL + Vercel                    │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
          ┌─────────▼────────┐ ┌────▼────┐ ┌──────▼──────┐
          │   FastAPI API    │ │ Database│ │  Scheduler  │
          │   Endpoints      │ │ (Postgres│ │ (APScheduler│
          │                  │ │   SQL)   │ │   Jobs)     │
          └──────────────────┘ └─────────┘ └─────────────┘
                    │               │               │
                    └───────────────┼───────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
          ┌─────────▼────────┐ ┌────▼────┐ ┌──────▼──────┐
          │   AI Signals     │ │  Brokers │ │ Market Data │
          │   Generation     │ │ (Alpaca/ │ │  Streaming  │
          │   (Claude/GPT)   │ │   IBKR)  │ │             │
          └──────────────────┘ └─────────┘ └─────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
          ┌─────────▼────────┐ ┌────▼────┐ ┌──────▼──────┐
          │   Risk Manager   │ │  Trading │ │ Notifications│
          │   (Stop Loss)    │ │  Engine  │ │   (Email)    │
          │                  │ │          │ │              │
          └──────────────────┘ └─────────┘ └─────────────┘
```

## Component Details

### 1. API Layer (FastAPI)
- **Purpose**: REST API endpoints for frontend and external integrations
- **Key Features**:
  - Automatic OpenAPI documentation
  - Request validation with Pydantic
  - CORS support for web clients
  - Async/await support for high concurrency
- **Endpoints**:
  - `/health` - Health checks
  - `/api/ai/signals` - AI trading signals
  - `/api/trades/*` - Trade management
  - `/api/positions/*` - Portfolio positions
  - `/api/dashboard/*` - Analytics and reporting

### 2. Database Layer (PostgreSQL)
- **Purpose**: Persistent data storage for trades, signals, and analytics
- **Schema**:
  - `ai_models` - AI model configurations
  - `ai_signals` - Trading signals with rationale
  - `trade_orders` - Executed trades with broker details
  - `positions` - Current portfolio holdings
- **Features**:
  - SQLAlchemy ORM for type safety
  - Connection pooling for performance
  - Automatic migrations on startup
  - Vercel Postgres for serverless hosting

### 3. Scheduler Layer (APScheduler)
- **Purpose**: Background job execution for automated trading
- **Jobs**:
  - Daily signal generation (9:30 AM ET)
  - Order execution (9:35 AM ET)
  - Position monitoring (every 5 min during market hours)
  - Risk assessment (hourly)
  - Database cleanup (daily)
- **Execution**: Runs in serverless environment via cron triggers

### 4. AI Signals Layer
- **Purpose**: Generate trading signals using multiple AI models
- **Supported Models**:
  - Anthropic Claude (primary)
  - OpenAI GPT-4 (alternative)
  - Google Gemini (backup)
  - xAI Grok (experimental)
- **Features**:
  - Multi-model fallback system
  - Confidence scoring
  - Signal caching and deduplication
  - Technical analysis integration

### 5. Broker Integration Layer
- **Purpose**: Execute trades through multiple broker APIs
- **Supported Brokers**:
  - Alpaca (primary - commission-free)
  - Interactive Brokers (advanced features)
- **Features**:
  - Unified broker interface
  - Automatic failover between brokers
  - Order status tracking
  - Position synchronization

### 6. Market Data Layer
- **Purpose**: Real-time and historical market data streaming
- **Data Sources**:
  - Alpaca Market Data API (primary)
  - Yahoo Finance (fallback)
- **Features**:
  - Real-time quotes and trades
  - Historical bars (1min, 5min, daily)
  - Technical indicators calculation
  - News and sentiment integration

### 7. Risk Management Layer
- **Purpose**: Protect capital through automated risk controls
- **Rules**:
  - Position size limits
  - Portfolio concentration limits
  - Daily loss limits
  - Stop-loss orders
  - Volatility filters
- **Features**:
  - Pre-trade risk assessment
  - Real-time position monitoring
  - Automatic position reduction

### 8. Trading Engine Layer
- **Purpose**: Execute trading strategies based on AI signals
- **Features**:
  - Signal-to-order conversion
  - Position sizing algorithms
  - Order routing optimization
  - Execution monitoring
  - Performance tracking

### 9. Notifications Layer
- **Purpose**: Alert users of important events and errors
- **Channels**:
  - Email (SMTP)
  - In-app notifications (future)
  - Webhooks (future)
- **Events**:
  - Trade executions
  - Risk limit breaches
  - System errors
  - Daily performance summaries

## Data Flow

### Signal Generation Flow
```
Market Data → Technical Analysis → AI Models → Signal Generation → Risk Assessment → Order Creation
```

### Trade Execution Flow
```
AI Signal → Risk Check → Position Sizing → Broker API → Order Placement → Confirmation → Database Update
```

### Monitoring Flow
```
Market Data → Position Updates → P&L Calculation → Risk Monitoring → Alerts/Notifications
```

## Deployment Architecture

### Vercel Serverless
- **Functions**: API endpoints as serverless functions
- **Database**: Vercel Postgres with connection pooling
- **Storage**: Environment variables for configuration
- **Scaling**: Automatic horizontal scaling
- **CDN**: Global edge network for low latency

### Environment Configuration
- **Production**: Live trading environment
- **Preview**: Staging for testing new features
- **Development**: Local development environment

## Security Architecture

### API Security
- Environment variable-based secrets
- Input validation and sanitization
- Rate limiting protection
- CORS policy enforcement

### Data Security
- Encrypted database connections
- Secure API key storage
- Audit logging for all trades
- Backup and recovery procedures

### Broker Security
- OAuth2 for Alpaca authentication
- Secure WebSocket connections
- API key rotation policies
- Multi-factor authentication where supported

## Performance Characteristics

### Latency Targets
- API Response: <500ms for simple queries
- Signal Generation: <30 seconds
- Trade Execution: <5 seconds
- Market Data: <100ms for quotes

### Scalability
- Horizontal scaling via Vercel
- Database connection pooling
- Caching for frequently accessed data
- Async processing for heavy computations

### Reliability
- Automatic retries for failed operations
- Circuit breakers for external APIs
- Graceful degradation on failures
- Comprehensive error handling and logging

## Monitoring & Observability

### Metrics
- API response times and error rates
- Database query performance
- Broker API call success rates
- Trading performance statistics

### Logging
- Structured JSON logging
- Error tracking and alerting
- Audit trails for all trades
- Performance monitoring

### Alerts
- System health monitoring
- Risk limit breach notifications
- Trading performance alerts
- Infrastructure issue detection