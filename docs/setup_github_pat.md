# GitHub Fine-grained PAT Setup

This document explains the minimum GitHub Personal Access Token settings required for Gyro Dev Tools.

## Required token type

Use a GitHub Fine-grained Personal Access Token.

## Repository access

Recommended:

- All repositories

Alternative:

- Only selected repositories
- Include the target repository, for example:
  - gitGyro-Dev/gyro-dev-tools
  - gitGyro-Dev/gyrologic
  - gitGyro-Dev/gyroos
  - gitGyro-Dev/gyroauth

## Required repository permissions

Minimum required permission:

| Permission | Access |
|---|---|
| Contents | Read and write |
| Metadata | Read-only |

## Important note

Selecting repositories is not enough.

You must also add repository permissions.

If no repository permissions are added, GitHub API read requests may succeed, but update requests such as PUT `/contents/{path}` can fail with `404 Not Found`.

## PowerShell setup

```powershell
$env:GITHUB_TOKEN="github_pat_xxxxx"
Verification
python -c "from tools.common.config import GITHUB_TOKEN, GITHUB_OWNER, GITHUB_REPO, GITHUB_BRANCH; print(GITHUB_OWNER, GITHUB_REPO, GITHUB_BRANCH); print(GITHUB_TOKEN[:15])"

Expected result:

gitGyro-Dev gyro-dev-tools main
github_pat_xxxx
Test update
python tools/github_update.py README.md
