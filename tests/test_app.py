from http import HTTPStatus

from httpx import Client

HEADER_NAME = "Request-Correlation-Id"


def test_success_propagates_header(client: Client, correlation_id: str) -> None:
    response = client.get("/success", headers={HEADER_NAME: correlation_id})
    assert response.status_code == HTTPStatus.OK
    assert response.headers.get(HEADER_NAME) == correlation_id


def test_failure_propagates_header(client: Client, correlation_id: str) -> None:
    response = client.get("/failure", headers={HEADER_NAME: correlation_id})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers.get(HEADER_NAME) == correlation_id


def test_error_propagates_header(client: Client, correlation_id: str) -> None:
    response = client.get("/error", headers={HEADER_NAME: correlation_id})
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.headers.get(HEADER_NAME) == correlation_id
