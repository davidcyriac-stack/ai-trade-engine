# Vercel Deployment Setup Guide

## 1. Add Vercel Postgres Database

### Option A: Via Vercel Dashboard
1. Go to https://vercel.com/dashboard/davidcyriac-stack/ai-trade-engine
2. Click **Storage** tab
3. Click **Create Database** → **Postgres**
4. Name it `ai-trade-engine-db`
5. Copy the `POSTGRES_URL` (or `DATABASE_URL`)

### Option B: Via Vercel CLI
```bash
vercel postgres create --name ai-trade-engine-db
```

## 2. Set Environment Variables

Run these commands (replace values with your actual keys):

```bash
# Database
vercel env add DATABASE_URL "postgresql://..."

# Alpaca API
vercel env add ALPACA_API_KEY "your_key_here"
vercel env add ALPACA_API_SECRET "your_secret_here"
vercel env add ALPACA_BASE_URL "https://paper-api.alpaca.markets"

# AI Model APIs
vercel env add CLAUDE_API_KEY "your_claude_key"
vercel env add OPENAI_API_KEY "your_openai_key"
vercel env add GEMINI_API_KEY "your_gemini_key"
vercel env add GROK_API_KEY "your_grok_key"

# Interactive Brokers
vercel env add IBKR_USERNAME "your_username"
vercel env add IBKR_PASSWORD "your_password"

# Email Notifications
vercel env add SMTP_HOST "smtp.gmail.com"
vercel env add SMTP_PORT "587"
vercel env add SMTP_USER "your_email@gmail.com"
vercel env add SMTP_PASS "your_app_password"
vercel env add SMTP_FROM "noreply@aitradeengine.com"
vercel env add DEFAULT_NOTIFICATION_EMAIL "your_email@gmail.com"
```

Or add them via Dashboard:
1. Project Settings → Environment Variables
2. Add each variable individually
3. Make sure to add for both Development and Production

## 3. Deploy with Database Initialized

After setting `DATABASE_URL`, the next deploy will automatically:
- Initialize the PostgreSQL database
- Create all tables from SQLAlchemy models
- Backend will be ready to use

## 4. Verify Deployment

Test the endpoints:
```bash
curl https://ai-trade-engine.vercel.app/health
curl https://ai-trade-engine.vercel.app/api/ai/signals
```
