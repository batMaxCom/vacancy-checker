from collections.abc import Callable

from fastapi import APIRouter, Request, Response
from httpx import AsyncClient, URL

PROXY_CONTROLLER = APIRouter()


def _proxy_route_factory(upstream_base: str) -> Callable:
    async def handler(request: Request, path: str) -> Response:
        body = await request.body()
        async with AsyncClient(base_url=upstream_base) as client:
            resp = await client.request(
                method=request.method,
                url=URL(path=f"/{path}"),
                params=dict(request.query_params),
                content=body,
                headers={
                    k: v
                    for k, v in request.headers.items()
                    if k.lower() not in ("host", "content-length")
                },
            )
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            headers=dict(resp.headers),
        )

    return handler


ROUTES: list[tuple[str, str]] = [
    ("/auth", "auth_url"),
    ("/user", "user_url"),
    ("/api/v1/search-jobs", "search_url"),
    ("/api/v1/search-profiles", "search_url"),
    ("/source", "vacancy_url"),
    ("/vacancy", "vacancy_url"),
]


def setup_proxy_routes(controller: APIRouter, upstream_map: dict[str, str]) -> None:
    for prefix, config_key in ROUTES:
        base_url = upstream_map[config_key]
        handler = _proxy_route_factory(base_url)
        controller.api_route(
            f"{prefix}/{{path:path}}",
            methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        )(handler)
