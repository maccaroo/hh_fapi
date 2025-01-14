from fastapi import FastAPI

from app.routers import auth_route, readings_route, root_route, sensors_route, users_route
from app.db.database import init_db


# Initialize database
init_db()

app = FastAPI()

# Include routers
app.include_router(root_route.router)
app.include_router(auth_route.router)
app.include_router(sensors_route.router)
app.include_router(readings_route.router)
app.include_router(users_route.router)
