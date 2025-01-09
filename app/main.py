from fastapi import FastAPI
from app.routers import readings_route, root_route, sensors_route
from app.db.database import init_db

app = FastAPI()

# Initialize database
init_db()

# Include routers
app.include_router(root_route.router)
app.include_router(sensors_route.router, prefix="/sensors", tags=["Sensors"])
app.include_router(readings_route.router, prefix="/readings", tags=["Readings"])
