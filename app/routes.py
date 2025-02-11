from fastapi import APIRouter

from app.modules.auth.routes import router as auth_router
from app.modules.tasks.routes import router as tasks_router


class AppRoutes:
    @property
    def routes(self):
        routes = APIRouter(prefix="/api/v1")

        routes.include_router(auth_router, prefix="/auth", tags=["auth"])
        routes.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

        return routes
