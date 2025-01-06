from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

DATABASE_URL = "sqlite:///./items.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("description", String),
)

metadata.create_all(engine)
