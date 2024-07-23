from fastapi.routing import APIRouter

from arithmetic.web.api import auth, docs, dummy, echo, monitoring, operation

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])
api_router.include_router(operation.router, prefix="/operation", tags=["operation"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
