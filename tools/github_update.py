import argparse
from pathlib import Path

from common.config import GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO, GITHUB_BRANCH
from common.github_client import GitHubClient


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

    args = parser.parse_args()

    local_path = Path(args.file)

    if not local_path.exists():
        raise FileNotFoundError(f"File not found: {local_path}")

    remote_path = args.remote or local_path.as_posix()
    message = args.message or f"Update {remote_path}"

    client = GitHubClient(
        token=GITHUB_TOKEN,
        owner=GITHUB_OWNER,
        repo=GITHUB_REPO,
        branch=GITHUB_BRANCH,
    )

    result = client.update_file(
        path=remote_path,
        content=local_path.read_bytes(),
        message=message,
    )

    commit = result.get("commit", {})

    print("Update completed.")
    print(f"Repository: {GITHUB_OWNER}/{GITHUB_REPO}")
    print(f"Branch: {GITHUB_BRANCH}")
    print(f"Path: {remote_path}")
    print(f"Commit: {commit.get('sha')}")
    print(f"URL: {commit.get('html_url')}")


if __name__ == "__main__":
    main()