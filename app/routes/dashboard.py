from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Position, TradeOrder

router = APIRouter()

@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    positions = db.query(Position).all()
    trades = db.query(TradeOrder).order_by(TradeOrder.created_at.desc()).limit(10).all()
    return {
        "positions": [
            {
                "symbol": p.symbol,
                "quantity": p.quantity,
                "avg_price": p.avg_price,
                "market_value": p.market_value,
                "pnl": p.pnl,
                "allocation_pct": p.allocation_pct,
            }
            for p in positions
        ],
        "recent_trades": [
            {
                "ai_model": t.ai_model,
                "symbol": t.symbol,
                "side": t.side,
                "quantity": t.quantity,
                "price": t.price,
                "status": t.status,
                "created_at": t.created_at,
            }
            for t in trades
        ],
    }
