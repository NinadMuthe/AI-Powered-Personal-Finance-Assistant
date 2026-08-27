from fastapi import APIRouter

from backend.app.api.transaction import router as transaction_router
from backend.app.api.routes import router as health_router


api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(transaction_router)


def get_route_info(router):
    routes = []
    for route in router.routes:
        if hasattr(route, "path"):
            routes.append((route.path, route.methods))
        elif hasattr(route, "routes"):
            routes.extend(get_route_info(route))
    return routes


__all__ = ["api_router", "get_route_info"]