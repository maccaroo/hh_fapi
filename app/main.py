from fastapi import FastAPI
from app.routers import root, sensors, sensor_values
from app.db.database import init_db

app = FastAPI()

# Initialize database
init_db()

# Include routers
app.include_router(root.router)
app.include_router(sensors.router, prefix="/sensors", tags=["Sensors"])
app.include_router(sensor_values.router, prefix="/sensor-values", tags=["Sensor Values"])
