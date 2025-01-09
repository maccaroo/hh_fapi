from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.reading import Reading, ReadingCreate
from app.services.reading_service import add_reading, delete_reading_by_id, get_reading_by_id, get_readings
from app.utils.dependencies import get_db

router = APIRouter()


### Readings endpoints

@router.post("/", response_model=Reading, status_code=status.HTTP_201_CREATED)
def add_reading_endpoint(value: ReadingCreate, db: Session = Depends(get_db)):
    """
    Create a reading.
    """
    return add_reading(db, value)

@router.get("/{reading_id}", response_model=Reading)
def get_reading_endpoint(reading_id: int, db: Session = Depends(get_db)):
    """
    Get a reading.
    """
    reading = get_reading_by_id(db, reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    return reading

@router.delete("/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reading_endpoint(reading_id: int, db: Session = Depends(get_db)):
    """
    Delete a reading.
    """
    success = delete_reading_by_id(db, reading_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reading not found")
    return
