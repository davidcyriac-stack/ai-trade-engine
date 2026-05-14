from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class AIModel(Base):
    __tablename__ = "ai_models"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    provider = Column(String(64), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    signals = relationship("AISignal", back_populates="model")

class AISignal(Base):
    __tablename__ = "ai_signals"
    id = Column(Integer, primary_key=True)
    model_id = Column(Integer, ForeignKey("ai_models.id"), nullable=True)
    symbol = Column(String(16), nullable=False)
    direction = Column(String(8), nullable=False)
    rationale = Column(Text, nullable=False)
    confidence = Column(Float, nullable=True)
    payload = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    model = relationship("AIModel", back_populates="signals")

class TradeOrder(Base):
    __tablename__ = "trade_orders"
    id = Column(Integer, primary_key=True)
    ai_model = Column(String(64), nullable=False)
    symbol = Column(String(16), nullable=False)
    side = Column(String(8), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=True)
    status = Column(String(32), nullable=False, default="pending")
    broker = Column(String(32), nullable=False)
    broker_order_id = Column(String(128), nullable=True)
    payload = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    executed_at = Column(DateTime, nullable=True)

class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True)
    ai_model = Column(String(64), nullable=False)
    symbol = Column(String(16), nullable=False)
    quantity = Column(Integer, nullable=False)
    avg_price = Column(Float, nullable=False)
    market_value = Column(Float, nullable=True)
    pnl = Column(Float, nullable=True)
    allocation_pct = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    channel = Column(String(32), nullable=False)
    event_type = Column(String(64), nullable=False)
    subject = Column(String(128), nullable=False)
    body = Column(Text, nullable=False)
    delivered = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    delivered_at = Column(DateTime, nullable=True)
