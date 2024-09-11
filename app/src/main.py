from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.infrastructure.api import value_error_exception_handler
from src.infrastructure.api.utils import allow_methods, allow_headers
from src.infrastructure.api.v1 import router as api_v1_router
from src.infrastructure.configs import api_config


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


main_app = FastAPI(
    lifespan=lifespan
)

main_app.include_router(api_v1_router)

main_app.add_exception_handler(ValueError, value_error_exception_handler)


main_app.add_middleware(
    CORSMiddleware,
    allow_origins=api_config.allowed_origins,
    allow_credentials=True,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
)

# start local
if __name__ == "__main__":
    if api_config.https:
        uvicorn.run(
            "src.main:main_app",
            port=api_config.port,
            host=api_config.host,
            reload=True,
            ssl_keyfile='../../certs/keyfile.key',
            ssl_certfile='../../certs/certfile.crt'
        )
    else:
        uvicorn.run("src.main:main_app", port=api_config.port, host=api_config.host, reload=True)
