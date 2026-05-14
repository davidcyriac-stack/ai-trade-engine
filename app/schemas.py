from datetime import datetime
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class TradeOrderSchema(BaseModel):
    id: int
    ai_model: str
    symbol: str
    side: str
    quantity: int
    price: Optional[float]
    status: str
    broker: str
    broker_order_id: Optional[str]
    payload: Optional[Dict[str, Any]]
    created_at: datetime
    executed_at: Optional[datetime]

    class Config:
        orm_mode = True

class PositionSchema(BaseModel):
    id: int
    ai_model: str
    symbol: str
    quantity: int
    avg_price: float
    market_value: Optional[float]
    pnl: Optional[float]
    allocation_pct: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class AISignalSchema(BaseModel):
    id: int
    model_id: int
    symbol: str
    direction: str
    rationale: str
    confidence: Optional[float]
    payload: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        orm_mode = True
