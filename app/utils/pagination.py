from sqlalchemy.orm import Session, Query
from dataclasses import dataclass


@dataclass
class PaginationContext:
    limit: int
    offset: int
    search: str
    db: Session


def paginate_query(query: Query, limit: int, offset: int):
    total = query.count()
    results = query.offset(offset).limit(limit).all()
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": results,
    }
