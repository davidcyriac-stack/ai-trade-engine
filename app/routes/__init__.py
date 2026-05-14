from fastapi import APIRouter

from app.routes.health import router as health_router
from app.routes.trades import router as trades_router
from app.routes.positions import router as positions_router
from app.routes.dashboard import router as dashboard_router
from app.routes.ai import router as ai_router

router = APIRouter()
router.include_router(health_router)
router.include_router(ai_router, prefix="/ai")
router.include_router(dashboard_router, prefix="/dashboard")
router.include_router(trades_router, prefix="/trades")
router.include_router(positions_router, prefix="/positions")
