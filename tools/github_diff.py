import argparse
import difflib
from pathlib import Path

from common.config import GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO, GITHUB_BRANCH
from common.config import resolve_repo
from common.github_client import GitHubClient
from common.cli import add_github_common_arguments
from common.config import resolve_owner, resolve_repo, resolve_branch


def main():
    parser = argparse.ArgumentParser(description="Show diff between local file and GitHub file.")
    parser.add_argument("file", help="Local file path.")
    parser.add_argument(
        "--remote",
        help="Remote path in repository. Defaults to local file path.",
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
        raise FileNotFoundError(f"Local file not found: {local_path}")

    remote_path = args.remote or local_path.as_posix()

    owner = resolve_owner(args.owner)
    repo = resolve_repo(args.repo)
    branch = resolve_branch(args.branch)

    client = GitHubClient(
        token=GITHUB_TOKEN,
        owner=owner,
        repo=repo,
        branch=branch,
    )

    remote_content = client.download_file(remote_path).decode("utf-8").splitlines()
    local_content = local_path.read_text(encoding="utf-8").splitlines()

    diff = difflib.unified_diff(
        remote_content,
        local_content,
        fromfile=f"github:{remote_path}",
        tofile=f"local:{local_path}",
        lineterm="",
    )

    diff_text = "\n".join(diff)

    if diff_text:
        print(diff_text)
        print(f"Repository: {owner}/{repo}")
        print(f"Branch: {branch}")
    else:
        print("No differences.")


if __name__ == "__main__":
    main()