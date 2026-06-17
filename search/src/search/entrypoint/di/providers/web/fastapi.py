from dishka import Provider, Scope, from_context
from starlette.requests import Request


class FastapiProvider(Provider):
    request = from_context(Request, scope=Scope.REQUEST)
