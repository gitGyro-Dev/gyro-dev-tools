import argparse
from pathlib import Path

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
    parser.add_argument("--create", action="store_true", help="Create a release.")
    parser.add_argument("--tag", help="Release tag name.")
    parser.add_argument("--name", help="Release name.")
    parser.add_argument("--body", help="Release body text.")
    parser.add_argument("--body-file", help="Path to release body markdown file.")
    parser.add_argument("--draft", action="store_true", help="Create as draft release.")
    parser.add_argument("--prerelease", action="store_true", help="Create as prerelease.")

    args = parser.parse_args()
    repo = resolve_repo(args.repo)

    client = GitHubClient(
        token=GITHUB_TOKEN,
        owner=GITHUB_OWNER,
        repo=repo,
        branch=GITHUB_BRANCH,
    )

    if args.create:
        if not args.tag:
            raise RuntimeError("--tag is required when using --create.")

        body = args.body or ""

        if args.body_file:
            body = Path(args.body_file).read_text(encoding="utf-8")

        release = client.create_release(
            tag_name=args.tag,
            name=args.name or args.tag,
            body=body,
            draft=args.draft,
            prerelease=args.prerelease,
        )

        print("Release created.")
        print(f"Repository: {GITHUB_OWNER}/{repo}")
        print(f"Tag: {release.get('tag_name')}")
        print(f"Name: {release.get('name')}")
        print(f"URL: {release.get('html_url')}")
        return

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