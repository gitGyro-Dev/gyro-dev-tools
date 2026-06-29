import argparse


def add_repository_argument(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """
    Add a common repository option to the parser.
    """

    parser.add_argument(
        "--repo",
        metavar="REPOSITORY",
        default=None,
        help="Target GitHub repository. Defaults to GITHUB_REPO.",
    )

    return parser