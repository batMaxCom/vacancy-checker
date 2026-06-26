from signal import SIGINT, signal

from click import argument, option
from dishka import FromDishka
from dishka.integrations.click import inject
from uvicorn import Server as UvicornServer


@argument("path", default=None, required=False)
@option("-h", "--host", default=None, help="Host to run the application")
@option("-p", "--port", default=None, help="Application launch port")
@inject
def start_uvicorn(
    path: str | None,
    host: str | None,
    port: int | None,
    *,
    uvicorn_server: FromDishka[UvicornServer],
) -> None:
    """
    Launch an application on FastAPI
    Command: auth-cli start-uvicorn.
    """
    if path is not None:
        uvicorn_server.config.app = path

    if host is not None:
        uvicorn_server.config.host = host

    if port is not None:
        uvicorn_server.config.port = port

    signal(
        SIGINT, lambda signum, frame: uvicorn_server.handle_exit(sig=signum, frame=frame)
    )

    uvicorn_server.run()
