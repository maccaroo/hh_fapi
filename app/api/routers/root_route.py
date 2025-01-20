from fastapi import APIRouter


router = APIRouter()

@router.get("/")
async def read_root():
    """
    Get the root of the API.
    """
    return {"message": "Welcome to Home Historian."}
