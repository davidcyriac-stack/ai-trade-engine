from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Position
from app.schemas import PositionSchema

router = APIRouter()

@router.get("/", response_model=list[PositionSchema])
def list_positions(db: Session = Depends(get_db)):
    return db.query(Position).all()
