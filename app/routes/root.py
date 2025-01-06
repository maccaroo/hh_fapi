from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "You've found the root!"}
