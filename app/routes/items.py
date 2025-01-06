from fastapi import APIRouter, HTTPException
from app.schemas import Item, ItemInDB
from app.crud import create_item, get_item, get_all_items

router = APIRouter()

@router.post("/items/", response_model=ItemInDB)
async def create_item_route(item: Item):
    item_id = await create_item(item.name, item.description)
    return {**item.dict(), "id": item_id}

@router.get("/items/{item_id}", response_model=ItemInDB)
async def get_item_route(item_id: int):
    item = await get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.get("/items/", response_model=list[ItemInDB])
async def get_all_items_route():
    return await get_all_items()
