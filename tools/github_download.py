import argparse
from pathlib import Path

from common.cli import add_repository_argument
from common.config import GITHUB_TOKEN, GITHUB_OWNER, GITHUB_BRANCH, resolve_repo
from common.github_client import GitHubClient


def main():
    parser = argparse.ArgumentParser(description="Download a file from GitHub.")
    parser.add_argument("remote", help="Remote file path in repository.")
    parser.add_argument(
        "--output",
        help="Local output path. Defaults to remote file path.",
        default=None,
    )

    add_repository_argument(parser)
    args = parser.parse_args()

    remote_path = args.remote
    output_path = Path(args.output or remote_path)
    repo = resolve_repo(args.repo)

    client = GitHubClient(
        token=GITHUB_TOKEN,
        owner=GITHUB_OWNER,
        repo=repo,
        branch=GITHUB_BRANCH,
    )

    content = client.download_file(remote_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(content)

    print("Download completed.")
    print(f"Repository: {GITHUB_OWNER}/{repo}")
    print(f"Branch: {GITHUB_BRANCH}")
    print(f"Remote: {remote_path}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
