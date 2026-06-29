import argparse
from pathlib import Path

from common.config import GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO, GITHUB_BRANCH
from common.config import resolve_repo
from common.github_client import GitHubClient
from common.cli import add_github_common_arguments
from common.config import resolve_owner, resolve_repo, resolve_branch


def main():
    parser = argparse.ArgumentParser(description="Update a file on GitHub.")
    parser.add_argument("file", help="Local file path to upload.")
    parser.add_argument(
        "--remote",
        help="Remote path in repository. Defaults to local file path.",
        default=None,
    )
    parser.add_argument(
        "--message",
        help="Commit message.",
        default=None,
    )
    parser.add_argument(
        "--repo",
        help="Target GitHub repository name. Defaults to GITHUB_REPO.",
        default=None,
    )

    add_github_common_arguments(parser)
    args = parser.parse_args()

    local_path = Path(args.file)

    if not local_path.exists():
        raise FileNotFoundError(f"File not found: {local_path}")

    remote_path = args.remote or local_path.as_posix()
    message = args.message or f"Update {remote_path}"

    owner = resolve_owner(args.owner)
    repo = resolve_repo(args.repo)
    branch = resolve_branch(args.branch)

    client = GitHubClient(
        token=GITHUB_TOKEN,
        owner=owner,
        repo=repo,
        branch=branch,
    )

    result = client.update_file(
        path=remote_path,
        content=local_path.read_bytes(),
        message=message,
    )

    commit = result.get("commit", {})

    print("Update completed.")
    print(f"Repository: {owner}/{repo}")
    print(f"Branch: {branch}")
    print(f"Path: {remote_path}")
    print(f"Commit: {commit.get('sha')}")
    print(f"URL: {commit.get('html_url')}")


if __name__ == "__main__":
    main()