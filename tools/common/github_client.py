import base64
from typing import Any

import requests


class GitHubClient:
    """
    Minimal GitHub REST API client for Gyro Dev Tools.

    This client focuses on repository and Contents API operations.
    CLI tools should call this class instead of using requests directly.
    """

    def __init__(self, token: str, owner: str, repo: str, branch: str = "main"):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}"

        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def _request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        """
        Send an HTTP request to the GitHub API.
        """
        return requests.request(
            method=method,
            url=url,
            headers=self.headers,
            timeout=30,
            **kwargs,
        )

    def _get(self, url: str, **kwargs: Any) -> requests.Response:
        return self._request("GET", url, **kwargs)

    def _put(self, url: str, payload: dict[str, Any]) -> requests.Response:
        return self._request("PUT", url, json=payload)

    def _contents_url(self, path: str) -> str:
        return f"{self.base_url}/contents/{path}"

    def _raise_for_response(self, res: requests.Response, action: str) -> None:
        if not res.ok:
            raise RuntimeError(f"{action} failed: {res.status_code} {res.text}")

    def get_repository(self) -> dict[str, Any]:
        """
        Get repository metadata.
        """
        res = self._get(self.base_url)
        self._raise_for_response(res, "Get repository")
        return res.json()

    def get_file_info(self, path: str) -> dict[str, Any] | None:
        """
        Get file metadata from the GitHub Contents API.

        Returns None when the path does not exist.
        """
        res = self._get(
            self._contents_url(path),
            params={"ref": self.branch},
        )

        if res.status_code == 404:
            return None

        self._raise_for_response(res, "Get file info")

        data = res.json()

        if data.get("type") != "file":
            raise RuntimeError(f"Path is not a file: {path}")

        return data

    def get_file_sha(self, path: str) -> str | None:
        """
        Get the SHA of a repository file.
        """
        file_info = self.get_file_info(path)
        if file_info is None:
            return None
        return file_info["sha"]

    def download_file(self, path: str) -> bytes:
        """
        Download a repository file as bytes.
        """
        file_info = self.get_file_info(path)

        if file_info is None:
            raise RuntimeError(f"File not found: {path}")

        encoded = file_info.get("content", "")
        return base64.b64decode(encoded)

    def update_file(self, path: str, content: bytes, message: str) -> dict[str, Any]:
        """
        Create or update a repository file.
        """
        sha = self.get_file_sha(path)
        encoded = base64.b64encode(content).decode("utf-8")

        payload: dict[str, Any] = {
            "message": message,
            "content": encoded,
            "branch": self.branch,
        }

        if sha:
            payload["sha"] = sha

        res = self._put(self._contents_url(path), payload)
        self._raise_for_response(res, "Update file")
        return res.json()
