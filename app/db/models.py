import datetime
import json
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator
from app.db.base import Base


class JSONEncodedDict(TypeDecorator):
    """Custom type to automatically serialize/deserialize JSON."""
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value)  # Serialize to JSON string

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return json.loads(value)  # Deserialize to Python dict


class Sensor(Base):
    __tablename__ = "sensor"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)  # Fully qualified name

    readings = relationship("Reading", back_populates="sensor", cascade="all, delete-orphan")


class Reading(Base):
    __tablename__ = "reading"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensor.id"), nullable=False)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)  # Fully qualified name
    value = Column(Float, nullable=False)
    extra_metadata = Column(JSONEncodedDict, nullable=True)

    sensor = relationship("Sensor", back_populates="readings")
