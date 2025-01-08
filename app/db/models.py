import datetime  # Import the module instead of just the class
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # Fully qualified name

    values = relationship("SensorValue", back_populates="sensor", cascade="all, delete-orphan")

class SensorValue(Base):
    __tablename__ = "sensor_values"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)  # Fully qualified name
    value = Column(Float, nullable=False)
    extra_metadata = Column(Text, nullable=True)

    sensor = relationship("Sensor", back_populates="values")
