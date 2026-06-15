from dishka import Provider, Scope, provide

REPOSITORIES: list[tuple[type, type]] = [
    # Example
    #(RepositoryImpl, Repository),
]

class DomainAdaptersProvider(Provider):
    """Domain adapter provider."""

    scope = Scope.REQUEST

    for impl, interface in REPOSITORIES:
        locals()[f"{interface.__name__.lower()}"] = provide(
            impl, provides=interface, scope=Scope.REQUEST
        )
