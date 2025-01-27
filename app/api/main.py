from fastapi import FastAPI

from app.api.routers import auth_router, data_points_router, datas_router, metas_router, root_router, users_router
from app.persistence.database import init_db


# Initialize database
init_db()

app = FastAPI()

# Include routers
app.include_router(root_router.router)
app.include_router(auth_router.router)
app.include_router(datas_router.router)
app.include_router(data_points_router.router)
app.include_router(users_router.router)
app.include_router(metas_router.router)
