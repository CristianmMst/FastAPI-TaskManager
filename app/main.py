from fastapi import FastAPI
from app.routes import AppRoutes

from app.modules.tasks.model import TaskDB
from sqlmodel import SQLModel
from app.core.database import engine
from contextlib import asynccontextmanager


class App:
    def __init__(self, routes=AppRoutes):
        self.routes = routes

    def run(self):
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            SQLModel.metadata.create_all(bind=engine)
            yield

        app = FastAPI(lifespan=lifespan)

        app.include_router(self.routes)

        return app


app = App(routes=AppRoutes().routes).run()
