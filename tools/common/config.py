def resolve_repo(repo: str | None) -> str:
    """
    Resolve repository name.
    """

    return repo if repo else GITHUB_REPO