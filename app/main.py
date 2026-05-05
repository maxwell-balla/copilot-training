import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.api import employees
from app.core.config import get_settings
from app.core.database import Base, engine
from app.exceptions.handlers import register_exception_handlers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)

logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = get_settings()
    if settings.app_env == "local":
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Employee API",
    description="REST API for managing employees",
    version="0.0.1",
    lifespan=lifespan,
)

register_exception_handlers(app)
app.include_router(employees.router)


@app.get("/actuator/health", tags=["actuator"])
def health() -> dict[str, str]:
    return {"status": "UP"}
