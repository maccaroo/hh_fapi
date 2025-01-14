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
    __table_args__ = {"schema": "hh"}

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    created_by = Column(Integer, ForeignKey("hh.user.id"), nullable=False)

    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    readings = relationship("Reading", back_populates="sensor", cascade="all, delete-orphan")


class Reading(Base):
    __tablename__ = "reading"
    __table_args__ = {"schema": "hh"}

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    sensor_id = Column(Integer, ForeignKey("hh.sensor.id"), nullable=False)
    value = Column(Float, nullable=False)
    extra_metadata = Column(JSONEncodedDict, nullable=True)

    sensor = relationship("Sensor", back_populates="readings")

class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "hh"}

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
