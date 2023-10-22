from fastapi.routing import APIRouter

from .account_router import router as acc_router
from .admin_account_router import router as adm_acc_router
from .admin_rent_router import router as adm_rnt_router
from .admin_transport_router import router as adm_tra_router
from .payment_router import router as pay_router
from .rent_router import router as rnt_router
from .transport_router import router as tra_router

admin_router = APIRouter(prefix="/Admin")
admin_router.include_router(adm_acc_router)
admin_router.include_router(adm_tra_router)
admin_router.include_router(adm_rnt_router)

router = APIRouter(prefix="/api")
router.include_router(admin_router)
router.include_router(acc_router)
router.include_router(tra_router)
router.include_router(rnt_router)
router.include_router(pay_router)
