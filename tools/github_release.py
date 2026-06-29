import argparse

from common.cli import add_repository_argument
from common.config import GITHUB_TOKEN, GITHUB_OWNER, GITHUB_BRANCH, resolve_repo
from common.github_client import GitHubClient


def main():
    parser = argparse.ArgumentParser(description="Show GitHub repository releases.")
    add_repository_argument(parser)
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of releases to show. Defaults to 10.",
    )

    args = parser.parse_args()
    repo = resolve_repo(args.repo)

    client = GitHubClient(
        token=GITHUB_TOKEN,
        owner=GITHUB_OWNER,
        repo=repo,
        branch=GITHUB_BRANCH,
    )

    releases = client.list_releases(limit=args.limit)

    print("Repository releases.")
    print(f"Repository: {GITHUB_OWNER}/{repo}")

    if not releases:
        print("No releases found.")
        return

    for release in releases:
        print()
        print(f"- {release.get('tag_name')}: {release.get('name')}")
        print(f"  Draft: {release.get('draft')}")
        print(f"  Prerelease: {release.get('prerelease')}")
        print(f"  Published: {release.get('published_at')}")
        print(f"  URL: {release.get('html_url')}")


if __name__ == "__main__":
    main()