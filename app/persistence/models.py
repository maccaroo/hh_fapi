import datetime
import json
from sqlalchemy import JSON, Integer, String, Text, DateTime, Column, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, class_mapper
from sqlalchemy.types import TypeDecorator
from sqlalchemy.ext.declarative import as_declarative, declared_attr


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


@as_declarative()
class BaseWithToDict:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def to_dict(self, include_relationships=True, include_columns=True, visited=None):
        """
        Convert the SQLAlchemy object to a dictionary, including relationships.
        
        Args:
            include_relationships (bool): Whether to include related objects.
            include_columns (bool): Whether to include direct columns.
            visited (set): Tracks visited objects to avoid infinite recursion.
        
        Returns:
            dict: The object represented as a dictionary.
        """
        if visited is None:
            visited = set()

        # Avoid infinite recursion by skipping already visited objects
        if self in visited:
            return {}
        visited.add(self)

        data = {}

        # Include column attributes
        if include_columns:
            for column in class_mapper(self.__class__).columns:
                data[column.name] = getattr(self, column.name)

        # Include relationships
        if include_relationships:
            for rel in class_mapper(self.__class__).relationships:
                related_obj = getattr(self, rel.key)
                if related_obj is None:
                    data[rel.key] = None
                elif isinstance(related_obj, list):  # Handle one-to-many or many-to-many
                    data[rel.key] = [obj.to_dict(include_relationships, include_columns, visited) for obj in related_obj]
                else:  # Handle one-to-one or many-to-one
                    data[rel.key] = related_obj.to_dict(include_relationships, include_columns, visited)

        return data


class User(BaseWithToDict):
    __tablename__ = "user"
    __table_args__ = {"schema": "hh"}

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    datas = relationship("Data", back_populates="created_by_user")


data_types = ["string", "integer", "float", "datetime"]
data_types_joined = ','.join(['\'' + _dt + '\'' for _dt in data_types])

class Data(BaseWithToDict):
    __tablename__ = "data"
    __table_args__ = (
        CheckConstraint(f"data_type IN ({data_types_joined})", name="check_data_type_value"),
        {"schema": "hh"}
    )

    id = Column(Integer, primary_key=True, index=True)
    created_by_user_id = Column(Integer, ForeignKey("hh.user.id", ondelete="restrict"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    data_type = Column(String, nullable=False)

    data_points = relationship("DataPoint", back_populates="data")
    created_by_user = relationship("User", back_populates="datas")
    data_metas = relationship("DataMeta")


class DataPoint(BaseWithToDict):
    __tablename__ = "data_point"
    __table_args__ = {"schema": "hh"}

    id = Column(Integer, primary_key=True, index=True)
    data_id = Column(Integer, ForeignKey("hh.data.id", ondelete="RESTRICT"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    value = Column(JSON, nullable=False)

    data = relationship("Data", back_populates="data_points")


meta_types = ["string", "integer", "float", "datetime"]
meta_types_joined = ','.join(['\'' + _dt + '\'' for _dt in meta_types])

class Meta(BaseWithToDict):
    __tablename__ = "meta"
    __table_args__ = (
        CheckConstraint(f"meta_type IN ({meta_types_joined})", name="check_meta_type_value"),
        {"schema": "hh"},
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    meta_type = Column(String, nullable=False)

    data_metas = relationship("DataMeta", back_populates="meta")


class DataMeta(BaseWithToDict):
    __tablename__ = "data_meta"
    __table_args__ = {"schema": "hh"}

    id = Column(Integer, primary_key=True, index=True)
    data_id = Column(Integer, ForeignKey("hh.data.id", ondelete="RESTRICT"), nullable=False)
    meta_id = Column(Integer, ForeignKey("hh.meta.id", ondelete="RESTRICT"), nullable=False)
    value = Column(JSON, nullable=False)

    data = relationship("Data", back_populates="data_metas")
    meta = relationship("Meta")

    # TODO: Add validation for 'value' column.