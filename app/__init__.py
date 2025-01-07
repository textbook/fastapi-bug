from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request


app = FastAPI()


@app.middleware("http")
async def propagate_request_id(request: Request, call_next):
    response = await call_next(request)
    if (
        request_correlation_id := request.headers.get("Request-Correlation-Id")
    ) is not None:
        response.headers["Request-Correlation-Id"] = request_correlation_id
    return response


@app.get("/success")
def _() -> None:
    pass


@app.get("/failure")
def _() -> None:
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND)


@app.get("/error")
def _() -> None:
    raise ValueError("oh no!")
