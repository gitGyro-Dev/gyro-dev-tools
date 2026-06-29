import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_OWNER = os.environ.get("GITHUB_OWNER")
GITHUB_REPO = os.environ.get("GITHUB_REPO")
GITHUB_BRANCH = os.environ.get("GITHUB_BRANCH", "main")

if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN is not set.")

if not GITHUB_OWNER:
    raise RuntimeError("GITHUB_OWNER is not set.")

if not GITHUB_REPO:
    raise RuntimeError("GITHUB_REPO is not set.")


def resolve_repo(repo: str | None) -> str:
    """Resolve target repository name."""
    return repo or GITHUB_REPO
