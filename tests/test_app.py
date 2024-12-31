from uuid import uuid4

import pytest
from httpx import Client

HEADER_NAME = "Request-Correlation-Id"

pytestmark = pytest.mark.filterwarnings("ignore::DeprecationWarning")


def test_success_propagates_header(client: Client) -> None:
    header_value = str(uuid4())
    response = client.get("/success", headers={HEADER_NAME: header_value})
    assert response.headers.get(HEADER_NAME) == header_value


def test_failure_does_not_propagate_header(client: Client) -> None:
    header_value = str(uuid4())
    response = client.get("/failure", headers={HEADER_NAME: header_value})
    assert response.headers.get(HEADER_NAME) == header_value
