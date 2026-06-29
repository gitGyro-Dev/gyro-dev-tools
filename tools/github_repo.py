import argparse

from common.cli import add_repository_argument
from common.config import GITHUB_TOKEN, GITHUB_OWNER, GITHUB_BRANCH, resolve_repo
from common.github_client import GitHubClient


def main():
    parser = argparse.ArgumentParser(description="Show GitHub repository information.")
    add_repository_argument(parser)
    args = parser.parse_args()

    repo = resolve_repo(args.repo)

    client = GitHubClient(
        token=GITHUB_TOKEN,
        owner=GITHUB_OWNER,
        repo=repo,
        branch=GITHUB_BRANCH,
    )

    data = client.get_repository()

    print("Repository information.")
    print(f"Repository: {data.get('full_name')}")
    print(f"Private: {data.get('private')}")
    print(f"Default branch: {data.get('default_branch')}")
    print(f"Description: {data.get('description')}")
    print(f"URL: {data.get('html_url')}")


if __name__ == "__main__":
    main()