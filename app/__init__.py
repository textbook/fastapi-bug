from http import HTTPStatus
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing_extensions import Annotated


def request_id(
    response: Response,
    request_correlation_id: Annotated[Optional[str], Header()] = None,
) -> None:
    if request_correlation_id is not None:
        response.headers.append("Request-Correlation-Id", request_correlation_id)


app = FastAPI(dependencies=[Depends(request_id)])


@app.exception_handler(StarletteHTTPException)
async def _(request: Request, exc: StarletteHTTPException):
    if exc.headers is None:
        exc.headers = dict()
    if (
        request_correlation_id := request.headers.get("Request-Correlation-Id")
    ) is not None:
        exc.headers["Request-Correlation-Id"] = request_correlation_id
    return await http_exception_handler(request, exc)


@app.get("/success")
def _() -> None:
    pass


@app.get("/failure")
def _() -> None:
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND)


@app.get("/error")
def _() -> None:
    raise ValueError("oh no!")
