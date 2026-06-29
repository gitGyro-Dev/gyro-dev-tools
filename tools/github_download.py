import argparse
from pathlib import Path

from common.config import GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO, GITHUB_BRANCH
from common.config import resolve_repo
from common.github_client import GitHubClient
from common.cli import add_github_common_arguments
from common.config import resolve_owner, resolve_repo, resolve_branch


def main():
    parser = argparse.ArgumentParser(description="Download a file from GitHub.")
    parser.add_argument("remote", help="Remote file path in repository.")
    parser.add_argument(
        "--output",
        help="Local output path. Defaults to remote file path.",
        default=None,
    )
    parser.add_argument(
        "--repo",
        help="Target GitHub repository name. Defaults to GITHUB_REPO.",
        default=None,
    )

    add_github_common_arguments(parser)
    args = parser.parse_args()

    remote_path = args.remote
    output_path = Path(args.output or remote_path)

    owner = resolve_owner(args.owner)
    repo = resolve_repo(args.repo)
    branch = resolve_branch(args.branch)

    client = GitHubClient(
        token=GITHUB_TOKEN,
        owner=owner,
        repo=repo,
        branch=branch,
    )

    content = client.download_file(remote_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(content)

    print("Download completed.")
    print(f"Repository: {owner}/{repo}")
    print(f"Branch: {branch}")
    print(f"Remote: {remote_path}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()