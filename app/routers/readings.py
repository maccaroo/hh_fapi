from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.reading import Reading, ReadingCreate
from app.services.reading_service import add_reading, get_readings
from app.utils.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=Reading)
def add_reading_endpoint(value: ReadingCreate, db: Session = Depends(get_db)):
    return add_reading(db, value)

@router.get("/{sensor_id}/readings", response_model=list[Reading])
def list_readings_endpoint(sensor_id: int, db: Session = Depends(get_db)):
    return get_readings(db, sensor_id)
