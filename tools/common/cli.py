import argparse


def add_github_common_arguments(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument(
        "--owner",
        help="Target GitHub owner or organization. Defaults to GITHUB_OWNER.",
        default=None,
    )
    parser.add_argument(
        "--repo",
        help="Target GitHub repository name. Defaults to GITHUB_REPO.",
        default=None,
    )
    parser.add_argument(
        "--branch",
        help="Target GitHub branch. Defaults to GITHUB_BRANCH.",
        default=None,
    )
    return parser