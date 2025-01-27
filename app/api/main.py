from fastapi import FastAPI
import uvicorn

from app.config.app_config import settings
from app.api.routers import auth_router, data_points_router, datas_router, metas_router, root_router, users_router
from app.persistence.database import init_db


app = FastAPI(debug=settings.API_DEBUG)

# Include routers
app.include_router(root_router.router)
app.include_router(auth_router.router)
app.include_router(datas_router.router)
app.include_router(data_points_router.router)
app.include_router(users_router.router)
app.include_router(metas_router.router)


def main():
    # Initialize database
    init_db()

    # Run the server
    uvicorn.run('app.api.main:app', host=settings.UVICORN_HOST, port=settings.UVICORN_PORT, reload=settings.UVICORN_RELOAD)


if __name__ == "__main__":
    main()
