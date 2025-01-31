from enum import Enum

class DataType(Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    DATETIME = "datetime"

class Data:

    def __init__(self, id: int, name: str, description: str, data_type: DataType):
        self.id = id
        
        self.name = name
        self.description = description
        self.data_type = data_type
