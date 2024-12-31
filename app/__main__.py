import os

import uvicorn

from app import app

host = os.getenv("HOST", "0.0.0.0")
port = int(os.getenv("PORT", 8080))

uvicorn.run(app, host=host, port=port)
