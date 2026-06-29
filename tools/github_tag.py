import argparse

from common.cli import add_repository_argument
from common.config import GITHUB_TOKEN, GITHUB_OWNER, GITHUB_BRANCH, resolve_repo
from common.github_client import GitHubClient


def main():
    parser = argparse.ArgumentParser(description="Show GitHub repository tags.")
    add_repository_argument(parser)
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Number of tags to show. Defaults to 20.",
    )

    args = parser.parse_args()
    repo = resolve_repo(args.repo)

    client = GitHubClient(
        token=GITHUB_TOKEN,
        owner=GITHUB_OWNER,
        repo=repo,
        branch=GITHUB_BRANCH,
    )

    tags = client.list_tags(limit=args.limit)

    print("Repository tags.")
    print(f"Repository: {GITHUB_OWNER}/{repo}")

    if not tags:
        print("No tags found.")
        return

    for tag in tags:
        name = tag.get("name")
        commit = tag.get("commit", {})
        sha = commit.get("sha", "")[:12]
        url = commit.get("url")

        print()
        print(f"- {name}")
        print(f"  Commit: {sha}")
        print(f"  API URL: {url}")


if __name__ == "__main__":
    main()