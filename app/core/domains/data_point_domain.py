from datetime import datetime
from app.core.domains import data_domain
from app.core.services.exceptions import ValidationException


class DataPoint:
    def __init__(self, data_point_id: int, data_id: int, created_at: str, value: dict):
        self.data_point_id = data_point_id
        self.data_id = data_id
        self.created_at = created_at
        self.value = value


def validate_data_point(data_point: DataPoint, data_type: data_domain.DataType):
    """
    Validate the data point
    """
    try:
        # Validate the data type
        value = data_point.value
        if data_type == data_domain.DataType.STRING:
            value = str(value)
        elif data_type == data_domain.DataType.INTEGER:
            value = int(value)
        elif data_type == data_domain.DataType.FLOAT:
            value = float(value)
        elif data_type == data_domain.DataType.DATETIME:
            value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        else:
            raise ValueError("Unsupported data type")
    except TypeError as e:
        raise ValidationException(str(e))
    except ValueError as e:
        raise ValidationException(str(e))
