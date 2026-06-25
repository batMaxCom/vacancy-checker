from click import Context, group, pass_context
from uvicorn import Config as UvicornConfig
from uvicorn import Server as UvicornServer

from gateway.entrypoint.web.configs.web import get_web_config


@group()
@pass_context
def main(context: Context) -> None:
    """CLI for API Gateway."""
    config  = get_web_config()
    app_config = config.app_config
    gateway_config = config.gateway_config
    uvicorn_config = UvicornConfig(
        app="gateway.entrypoint.web.application:app_factory",
        host=config.server_host,
        port=config.server_port,
        loop=config.loop,
        factory=True,
        reload=True,
    )
    uvicorn_server = UvicornServer(uvicorn_config)

    container = cli_container( uvicorn_config, uvicorn_server)
    setup_dishka(container, context, finalize_container=True)


main.command(start_uvicorn)
