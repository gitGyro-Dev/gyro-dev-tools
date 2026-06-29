import argparse
import difflib
from pathlib import Path

from common.cli import add_repository_argument
from common.config import GITHUB_TOKEN, GITHUB_OWNER, GITHUB_BRANCH, resolve_repo
from common.github_client import GitHubClient


def main():
    parser = argparse.ArgumentParser(
        description="Show diff between a local file and a GitHub file."
    )
    parser.add_argument("file", help="Local file path.")
    parser.add_argument(
        "--remote",
        help="Remote path in repository. Defaults to local file path.",
        default=None,
    )

    add_repository_argument(parser)

    args = parser.parse_args()

    local_path = Path(args.file)

    if not local_path.exists():
        raise FileNotFoundError(f"Local file not found: {local_path}")

    remote_path = args.remote or local_path.as_posix()
    repo = resolve_repo(args.repo)

    client = GitHubClient(
        token=GITHUB_TOKEN,
        owner=GITHUB_OWNER,
        repo=repo,
        branch=GITHUB_BRANCH,
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

    print(f"Repository: {GITHUB_OWNER}/{repo}")
    print(f"Branch: {GITHUB_BRANCH}")
    print(f"Path: {remote_path}")

    if diff_text:
        print(diff_text)
    else:
        print("No differences.")


if __name__ == "__main__":
    main()
