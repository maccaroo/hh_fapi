from fastapi import APIRouter, Request, HTTPException

router = APIRouter()

@router.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def catch_all(request: Request, full_path: str):
    raise HTTPException(status_code=404, detail=f"Endpoint '{request.method} {request.url.path}' not found")
