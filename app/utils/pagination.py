from sqlalchemy.orm import Session, Query
from dataclasses import dataclass


@dataclass
class PaginationContext:
    db: Session = None
    limit: int = 10
    offset: int = 0
    search: str = ""


def paginate_query(query: Query, limit: int, offset: int):
    total = query.count()
    results = query.offset(offset).limit(limit).all()
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": results,
    }
