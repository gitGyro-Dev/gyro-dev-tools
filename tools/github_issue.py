import argparse
from pathlib import Path

from common.cli import add_repository_argument
from common.config import GITHUB_TOKEN, GITHUB_OWNER, GITHUB_BRANCH, resolve_repo
from common.github_client import GitHubClient


def main():
    parser = argparse.ArgumentParser(description="Show or create GitHub issues.")
    add_repository_argument(parser)

    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--state", default="open", choices=["open", "closed", "all"])

    parser.add_argument("--create", action="store_true", help="Create an issue.")
    parser.add_argument("--title", help="Issue title.")
    parser.add_argument("--body", help="Issue body text.")
    parser.add_argument("--body-file", help="Path to issue body markdown file.")
    parser.add_argument("--labels", help="Comma-separated labels.")

    args = parser.parse_args()
    repo = resolve_repo(args.repo)

    client = GitHubClient(
        token=GITHUB_TOKEN,
        owner=GITHUB_OWNER,
        repo=repo,
        branch=GITHUB_BRANCH,
    )

    if args.create:
        if not args.title:
            raise RuntimeError("--title is required when using --create.")

        body = args.body or ""
        if args.body_file:
            body = Path(args.body_file).read_text(encoding="utf-8")

        labels = None
        if args.labels:
            labels = [x.strip() for x in args.labels.split(",") if x.strip()]

        issue = client.create_issue(
            title=args.title,
            body=body,
            labels=labels,
        )

        print("Issue created.")
        print(f"Repository: {GITHUB_OWNER}/{repo}")
        print(f"Title: {issue.get('title')}")
        print(f"Number: #{issue.get('number')}")
        print(f"URL: {issue.get('html_url')}")
        return

    issues = client.list_issues(limit=args.limit, state=args.state)

    print("Repository issues.")
    print(f"Repository: {GITHUB_OWNER}/{repo}")
    print(f"State: {args.state}")

    if not issues:
        print("No issues found.")
        return

    for issue in issues:
        if "pull_request" in issue:
            continue

        print()
        print(f"- #{issue.get('number')} {issue.get('title')}")
        print(f"  State: {issue.get('state')}")
        print(f"  Created: {issue.get('created_at')}")
        print(f"  URL: {issue.get('html_url')}")


if __name__ == "__main__":
    main()