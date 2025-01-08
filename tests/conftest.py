"""
Setup to test against an in-memory Uvicorn server as described in
https://blog.jonrshar.pe/2024/Aug/17/python-tdd-ohm.html#bonus
"""

from __future__ import annotations

from collections.abc import Generator
from socket import socket
from threading import Thread
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import Client
from uvicorn import Config, Server

from app import app


@pytest.fixture
def correlation_id() -> str:
    return str(uuid4())


@pytest.fixture(scope="module")
def client() -> Generator[Client, None, None]:
    with TestServer.random_port(app) as server:
        with Client(base_url=server.url) as client:
            yield client


class TestServer:

    @classmethod
    def random_port(cls, application: FastAPI) -> TestServer:
        socket_ = socket()
        socket_.bind(("", 0))
        return cls(application, socket_)

    def __init__(self, application: FastAPI, socket_: socket):
        self._server = Server(Config(app=application))
        self._socket = socket_
        self._thread = Thread(
            target=self._server.run,
            kwargs=dict(sockets=[self._socket]),
        )

    def __enter__(self) -> TestServer:
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._server.should_exit = True
        self._thread.join()

    @property
    def url(self) -> str:
        host, port = self._socket.getsockname()
        return f"http://{host}:{port}"
