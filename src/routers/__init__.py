from fastapi.routing import APIRouter

from .account_router import router as acc_router

router = APIRouter()
router.include_router(acc_router)
