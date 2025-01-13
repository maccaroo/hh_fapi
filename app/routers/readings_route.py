from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import app.schemas.reading_schema as reading_schema
import app.services.reading_service as reading_service
from app.utils.dependencies import get_db

router = APIRouter(prefix="/readings", tags=["Readings"])


### Readings endpoints

@router.post("/", response_model=reading_schema.ReadingResponse, status_code=status.HTTP_201_CREATED)
def add_reading_endpoint(reading_create: reading_schema.ReadingCreate, db: Session = Depends(get_db)):
    """
    Create a reading.
    """
    reading = reading_service.add_reading(db, reading_create)
    return reading


@router.get("/{reading_id}", response_model=reading_schema.ReadingResponse)
def get_reading_endpoint(reading_id: int, db: Session = Depends(get_db)):
    """
    Get a reading.
    """
    reading = reading_service.get_reading_by_id(db, reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    return reading


@router.delete("/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reading_endpoint(reading_id: int, db: Session = Depends(get_db)):
    """
    Delete a reading.
    """
    success = reading_service.delete_reading_by_id(db, reading_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reading not found")
    return
