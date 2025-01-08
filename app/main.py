from fastapi import FastAPI
from app.routers import root, sensors, readings
from app.db.database import init_db

app = FastAPI()

# Initialize database
init_db()

# Include routers
app.include_router(root.router)
app.include_router(sensors.router, prefix="/sensors", tags=["Sensors"])
app.include_router(readings.router, prefix="/readings", tags=["Readings"])
