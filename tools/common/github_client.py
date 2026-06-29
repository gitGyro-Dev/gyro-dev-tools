import base64
import requests


class GitHubClient:
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

    def get_file_sha(self, path: str) -> str | None:
        url = f"{self.base_url}/contents/{path}"
        res = requests.get(
            url,
            headers=self.headers,
            params={"ref": self.branch},
            timeout=30,
        )

        if res.status_code == 404:
            return None

        if not res.ok:
            raise RuntimeError(f"Failed to get file SHA: {res.status_code} {res.text}")

        return res.json()["sha"]

    def update_file(self, path: str, content: bytes, message: str) -> dict:
        sha = self.get_file_sha(path)

        encoded = base64.b64encode(content).decode("utf-8")

        payload = {
            "message": message,
            "content": encoded,
            "branch": self.branch,
        }

        if sha:
            payload["sha"] = sha

        url = f"{self.base_url}/contents/{path}"
        res = requests.put(url, headers=self.headers, json=payload, timeout=30)

        if not res.ok:
            raise RuntimeError(f"Failed to update file: {res.status_code} {res.text}")

        return res.json()