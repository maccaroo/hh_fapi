from sqlalchemy.orm import Query
from dataclasses import dataclass

from app.api.schemas.pagination_schema import PaginatedResponse


@dataclass
class PaginationContext:
    limit: int = 10
    offset: int = 0
    search: str = ""


def paginate_query(query: Query, limit: int, offset: int):
    total = query.count()
    results = query.offset(offset).limit(limit).all()
    return PaginatedResponse(
        total=total, 
        limit=limit, 
        offset=offset, 
        items=results
        )
