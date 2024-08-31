from typing import Any

from fastapi import APIRouter as FastAPIRouter, Header

from src.domain.usecases import GetProductById
from src.domain.usecases.get_products import GetProducts
from src.infrastructure.repositories import DeDBRepository, EnDBRepository, RuDBRepository

allow_methods = ["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"]
allow_headers = [
    "Content-Type",
    "Set-Cookie",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Origin",
    "Authorization",
    "Accept-Language"
]

languages = ["en", "ru", "de"]


def check_language(lang):
    if lang not in languages:
        return languages[0]
    return lang


def get_db_imple(accept_language):
    lang = check_language(accept_language.split(',')[0].split(';')[0].strip())
    repos = {
        "ru": RuDBRepository(),
        "en": EnDBRepository(),
        "de": DeDBRepository(),
    }
    return repos.get(lang)


def get_usecase_get_product_by_id(accept_language: str = Header("en")):
    return GetProductById(get_db_imple(accept_language))


def get_usecase_get_products(accept_language: str = Header("en")):
    return GetProducts(get_db_imple(check_language(accept_language)))


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
