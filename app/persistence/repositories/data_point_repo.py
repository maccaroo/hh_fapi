from sqlalchemy.orm import Session


class DataPointRepository:

    def __init__(self, db: Session):
        self.db = db

    
    