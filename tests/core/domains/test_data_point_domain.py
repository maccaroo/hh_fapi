import pytest

from app.core.domains.data_domain import DataType
from app.core.domains.data_point_domain import DataPoint, validate_data_point
from app.core.services.exceptions import ValidationException


def test_init():
    data_point = DataPoint(1, 2, "2025-12-31 23:59:59", 123)
    assert data_point is not None
    assert data_point.id == 1
    assert data_point.data_id == 2
    assert data_point.created_at == "2025-12-31 23:59:59"
    assert data_point.value == 123

def test_validate_nominal():
    data_point = DataPoint(1, 2, "2025-12-31 23:59:59", "Fred")
    validate_data_point(data_point, DataType.STRING)

def test_validate_nominal_invalid():
    data_point = DataPoint(1, 2, "2025-12-31 23:59:59", 12.34)
    with pytest.raises(ValidationException):
        validate_data_point(data_point, DataType.INTEGER)
