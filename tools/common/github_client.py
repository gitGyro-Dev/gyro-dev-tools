"""
GitHub REST API client for Gyro Dev Tools.

This client is intentionally lightweight and depends only on requests.
It provides shared methods used by CLI tools under tools/.
"""

from __future__ import annotations

import base64
from typing import Any

import requests


class GitHubClient:
    """Small GitHub REST API client for repository operations."""

    API_VERSION = "2022-11-28"
    DEFAULT_TIMEOUT = 30

    def __init__(self, token: str, owner: str, repo: str, branch: str = "main"):
        if not token:
            raise ValueError("token is required")
        if not owner:
            raise ValueError("owner is required")
        if not repo:
            raise ValueError("repo is required")
        if not branch:
            raise ValueError("branch is required")

        self.token = token
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}"

        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": self.API_VERSION,
        }

    # ------------------------------------------------------------------
    # Low-level HTTP helpers
    # ------------------------------------------------------------------

    def _request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        """Execute an HTTP request with shared headers and timeout."""
        timeout = kwargs.pop("timeout", self.DEFAULT_TIMEOUT)

        headers = self.headers.copy()
        extra_headers = kwargs.pop("headers", None)
        if extra_headers:
            headers.update(extra_headers)

        return requests.request(
            method=method,
            url=url,
            headers=headers,
            timeout=timeout,
            **kwargs,
        )

    def _get(self, url: str, **kwargs: Any) -> requests.Response:
        return self._request("GET", url, **kwargs)

    def _put(self, url: str, **kwargs: Any) -> requests.Response:
        return self._request("PUT", url, **kwargs)

    def _post(self, url: str, **kwargs: Any) -> requests.Response:
        return self._request("POST", url, **kwargs)

    def _patch(self, url: str, **kwargs: Any) -> requests.Response:
        return self._request("PATCH", url, **kwargs)

    def _delete(self, url: str, **kwargs: Any) -> requests.Response:
        return self._request("DELETE", url, **kwargs)

    def _handle_response(self, res: requests.Response, message: str) -> Any:
        """Return JSON response or raise a detailed RuntimeError."""
        if not res.ok:
            raise RuntimeError(f"{message}: {res.status_code} {res.text}")

        if res.status_code == 204 or not res.text:
            return None

        return res.json()

    # ------------------------------------------------------------------
    # URL helpers
    # ------------------------------------------------------------------

    def _contents_url(self, path: str) -> str:
        return f"{self.base_url}/contents/{path}"

    def _commits_url(self) -> str:
        return f"{self.base_url}/commits"

    def _tags_url(self) -> str:
        return f"{self.base_url}/tags"

    def _releases_url(self) -> str:
        return f"{self.base_url}/releases"

    def _issues_url(self) -> str:
        return f"{self.base_url}/issues"

    # ------------------------------------------------------------------
    # Repository
    # ------------------------------------------------------------------

    def get_repository(self) -> dict[str, Any]:
        """Get repository metadata."""
        res = self._get(self.base_url)
        return self._handle_response(res, "Failed to get repository")

    # ------------------------------------------------------------------
    # Contents API
    # ------------------------------------------------------------------

    def get_file_info(self, path: str) -> dict[str, Any] | None:
        """Get GitHub Contents API metadata for a file.

        Returns None when the path does not exist.
        """
        res = self._get(
            self._contents_url(path),
            params={"ref": self.branch},
        )

        if res.status_code == 404:
            return None

        data = self._handle_response(res, "Failed to get file information")

        if isinstance(data, list):
            raise RuntimeError(f"Path is a directory, not a file: {path}")

        return data

    def get_file_sha(self, path: str) -> str | None:
        """Get file SHA, or None when the file does not exist."""
        data = self.get_file_info(path)
        if data is None:
            return None
        return data.get("sha")

    def download_file(self, path: str) -> bytes:
        """Download a file from the repository."""
        data = self.get_file_info(path)

        if data is None:
            raise RuntimeError(f"Remote file not found: {path}")

        if data.get("type") != "file":
            raise RuntimeError(f"Path is not a file: {path}")

        encoded = data.get("content", "")
        if not encoded:
            return b""

        return base64.b64decode(encoded)

    def update_file(self, path: str, content: bytes, message: str) -> dict[str, Any]:
        """Create or update a file in the repository."""
        sha = self.get_file_sha(path)
        encoded = base64.b64encode(content).decode("utf-8")

        payload: dict[str, Any] = {
            "message": message,
            "content": encoded,
            "branch": self.branch,
        }

        if sha:
            payload["sha"] = sha

        res = self._put(self._contents_url(path), json=payload)
        return self._handle_response(res, "Failed to update file")

    # ------------------------------------------------------------------
    # Commits
    # ------------------------------------------------------------------

    def list_commits(self, limit: int = 10) -> list[dict[str, Any]]:
        """List recent commits on the configured branch."""
        if limit < 1:
            raise ValueError("limit must be greater than or equal to 1")

        res = self._get(
            self._commits_url(),
            params={
                "sha": self.branch,
                "per_page": min(limit, 100),
            },
        )
        return self._handle_response(res, "Failed to list commits")

    # ------------------------------------------------------------------
    # Tags
    # ------------------------------------------------------------------

    def list_tags(self, limit: int = 30) -> list[dict[str, Any]]:
        """List repository tags."""
        if limit < 1:
            raise ValueError("limit must be greater than or equal to 1")

        res = self._get(
            self._tags_url(),
            params={"per_page": min(limit, 100)},
        )
        return self._handle_response(res, "Failed to list tags")

    # ------------------------------------------------------------------
    # Releases
    # ------------------------------------------------------------------

    def list_releases(self, limit: int = 10) -> list[dict[str, Any]]:
        """List repository releases."""
        if limit < 1:
            raise ValueError("limit must be greater than or equal to 1")

        res = self._get(
            self._releases_url(),
            params={"per_page": min(limit, 100)},
        )
        return self._handle_response(res, "Failed to list releases")

    def create_release(
        self,
        tag_name: str,
        name: str | None = None,
        body: str | None = None,
        draft: bool = False,
        prerelease: bool = False,
        target_commitish: str | None = None,
    ) -> dict[str, Any]:
        """Create a GitHub release."""
        if not tag_name:
            raise ValueError("tag_name is required")

        payload: dict[str, Any] = {
            "tag_name": tag_name,
            "name": name or tag_name,
            "body": body or "",
            "draft": draft,
            "prerelease": prerelease,
            "target_commitish": target_commitish or self.branch,
        }

        res = self._post(self._releases_url(), json=payload)
        return self._handle_response(res, "Failed to create release")

    # ------------------------------------------------------------------
    # Issues
    # ------------------------------------------------------------------

    def create_issue(
        self,
        title: str,
        body: str | None = None,
        labels: list[str] | None = None,
    ) -> dict[str, Any]:
        """Create an issue."""
        if not title:
            raise ValueError("title is required")

        payload: dict[str, Any] = {
            "title": title,
            "body": body or "",
        }

        if labels:
            payload["labels"] = labels

        res = self._post(self._issues_url(), json=payload)
        return self._handle_response(res, "Failed to create issue")


    def list_issues(self, limit: int = 20, state: str = "open") -> list[dict[str, Any]]:
        """List repository issues."""
        if limit < 1:
            raise ValueError("limit must be greater than or equal to 1")

        res = self._get(
            self._issues_url(),
            params={
                "state": state,
                "per_page": min(limit, 100),
            },
        )
        return self._handle_response(res, "Failed to list issues")
    
    def close_issue(self, number: int) -> dict[str, Any]:
        """Close an issue by issue number."""
        if number < 1:
            raise ValueError("number must be greater than or equal to 1")

        payload: dict[str, Any] = {
            "state": "closed",
        }

        res = self._patch(
            f"{self._issues_url()}/{number}",
            json=payload,
        )
        return self._handle_response(res, "Failed to close issue")