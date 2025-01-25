from fastapi import FastAPI

from app.api.routers import auth_route, data_points_route, datas_route, metas_route, root_route, users_route
from app.persistence.db.database import init_db


# Initialize database
init_db()

app = FastAPI()

# Include routers
app.include_router(root_route.router)
app.include_router(auth_route.router)
app.include_router(datas_route.router)
app.include_router(data_points_route.router)
app.include_router(users_route.router)
app.include_router(metas_route.router)
