import pytest
from app.core.domains.data_domain import Data, DataType

def test_init():
    data_domain = Data(1, "testName", "testDescription", DataType.STRING)
    assert data_domain is not None
    assert data_domain.id == 1
    assert data_domain.name == "testName"
    assert data_domain.description == "testDescription"
    assert data_domain.data_type == DataType.STRING
