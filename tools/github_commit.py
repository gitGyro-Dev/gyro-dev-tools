import argparse

from common.cli import add_repository_argument
from common.config import GITHUB_TOKEN, GITHUB_OWNER, GITHUB_BRANCH, resolve_repo
from common.github_client import GitHubClient


def main():
    parser = argparse.ArgumentParser(description="Show recent GitHub commits.")
    add_repository_argument(parser)
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Number of commits to show. Defaults to 10.",
    )

    args = parser.parse_args()
    repo = resolve_repo(args.repo)

    client = GitHubClient(
        token=GITHUB_TOKEN,
        owner=GITHUB_OWNER,
        repo=repo,
        branch=GITHUB_BRANCH,
    )

    commits = client.list_commits(limit=args.limit)

    print("Recent commits.")
    print(f"Repository: {GITHUB_OWNER}/{repo}")
    print(f"Branch: {GITHUB_BRANCH}")

    for item in commits:
        sha = item.get("sha", "")[:12]
        commit = item.get("commit", {})
        message = commit.get("message", "").splitlines()[0]
        author = commit.get("author", {}).get("name")
        date = commit.get("author", {}).get("date")
        url = item.get("html_url")

        print()
        print(f"- {sha} {message}")
        print(f"  Author: {author}")
        print(f"  Date: {date}")
        print(f"  URL: {url}")


if __name__ == "__main__":
    main()