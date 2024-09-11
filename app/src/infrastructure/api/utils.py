from typing import Any

from fastapi import APIRouter as FastAPIRouter

allow_methods = ["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"]
allow_headers = [
    "Content-Type",
    "Set-Cookie",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Origin",
    "Authorization",
    "Accept-Language"
]


def convert_header_lang(header_lang: str):
    return header_lang.split(',')[0].split(';')[0].strip()


def _get_alternative_path(path: str) -> str:
    return path[:-1] if path.endswith("/") else f"{path}/"


class APIRouter(FastAPIRouter):
    def add_api_route(
        self, path: str, *args: Any, include_in_schema: bool = True, **kwargs: Any
    ) -> None:
        super().add_api_route(
            _get_alternative_path(path), *args, include_in_schema=False, **kwargs
        )
        super().add_api_route(
            path, *args, include_in_schema=include_in_schema, **kwargs
        )

    def add_api_websocket_route(self, path: str, *args: Any, **kwargs: Any) -> None:
        super().add_api_websocket_route(_get_alternative_path(path), *args, **kwargs)
        super().add_api_websocket_route(path, *args, **kwargs)
