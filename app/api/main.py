from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
import uvicorn

from app.config.app_config import settings
from app.config.logging_config import init_logger, get_module_logger
from app.api.routers import auth_router, data_metas_router, data_points_router, datas_router, metas_router, root_router, users_router
from app.persistence.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start up code
    init_logger()
    logger = get_module_logger()
    logger.info("App is starting up...")
    yield

    # Shutdown code
    logger.info("App is shutting down...")


def main():
    # Initialise logger
    init_logger()
    logging.info("Logger initialised successfully")

    # Initialize database
    init_db()

    # Run the server
    uvicorn.run('app.api.main:app', host=settings.UVICORN_HOST, port=settings.UVICORN_PORT, reload=settings.UVICORN_RELOAD)


app = FastAPI(debug=settings.API_DEBUG, lifespan=lifespan)

# Include routers
app.include_router(root_router.router)
app.include_router(auth_router.router)
app.include_router(datas_router.router)
app.include_router(data_points_router.router)
app.include_router(users_router.router)
app.include_router(metas_router.router)
app.include_router(data_metas_router.router)


if __name__ == "__main__":
    main()