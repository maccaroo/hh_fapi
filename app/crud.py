from sqlalchemy import insert, select
from app.models import items
from app.db import database

async def create_item(name: str, description: str):
    query = insert(items).values(name=name, description=description)
    return await database.execute(query)

async def get_item(item_id: int):
    # Updated to use select(items) for SQLAlchemy 1.4+
    query = select(items).where(items.c.id == item_id)
    return await database.fetch_one(query)

async def get_all_items():
    # Updated to use select(items)
    query = select(items)
    return await database.fetch_all(query)
