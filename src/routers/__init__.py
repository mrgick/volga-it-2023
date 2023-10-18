from fastapi.routing import APIRouter

from .account_router import router as acc_router
from .admin_account_router import router as adm_acc_router

router = APIRouter()
router.include_router(acc_router)
router.include_router(adm_acc_router)
