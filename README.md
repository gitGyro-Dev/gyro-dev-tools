# Gyro Dev Tools

Developer Toolkit for GitHub Automation and OSS Development

Gyro Dev Tools is a Python-based toolkit for automating GitHub operations through the GitHub REST API.

The project aims to provide reusable command-line tools and libraries for repository management, release automation, documentation maintenance, and future publication workflows.

Although developed alongside the Gyro projects, this toolkit is completely independent and can be used for any GitHub repository.

---

# Features

Current

- Update files via GitHub REST API
- Secure authentication using GitHub Fine-grained Personal Access Tokens
- Shared GitHub client library
- Environment-based configuration

Planned

- Download files
- Repository information
- Commit history
- File diff
- Release creation
- Tag management
- Issue creation
- Pull Request creation
- GitHub Assets upload
- Repository management

Future

- Zenodo publication support
- Jxiv publication support
- AI-assisted development workflow
- Claude Code integration
- Codex integration
- GitHub Actions support

---

# Project Structure

```text
gyro-dev-tools/

├── docs/
│   └── setup_github_pat.md
│
├── tools/
│   ├── github_update.py
│   ├── github_download.py
│   ├── github_diff.py
│   ├── github_commit.py
│   ├── github_release.py
│   ├── github_tag.py
│   ├── github_repo.py
│   │
│   └── common/
│       ├── github_client.py
│       ├── config.py
│       └── util.py
│
├── .env.example
├── requirements.txt
└── README.md
```

---

# Requirements

- Python 3.11 or later
- requests
- python-dotenv

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

Copy

```text
.env.example
```

to

```text
.env
```

Example

```text
GITHUB_OWNER=gitGyro-Dev
GITHUB_REPO=gyro-dev-tools
GITHUB_BRANCH=main
```

For security, it is recommended to provide the Personal Access Token through an environment variable.

PowerShell

```powershell
$env:GITHUB_TOKEN="github_pat_xxxxxxxxx"
```

See

```
docs/setup_github_pat.md
```

for the required GitHub permission settings.

---

# Usage

Update a file

```powershell
python tools/github_update.py README.md
```

Specify a commit message

```powershell
python tools/github_update.py README.md --message "Update README"
```

Future versions will support specifying repositories directly.

Example

```powershell
python tools/github_update.py README.md --repo gyroauth
```

---

# Design Principles

- GitHub REST API v3
- Shared client library
- Reusable architecture
- CLI-first design
- GUI-ready architecture
- Maintainability over complexity
- Secure authentication
- Minimal external dependencies

---

# Roadmap

## Phase 1

- ✅ GitHub Update
- GitHub Download
- GitHub Diff

## Phase 2

- Commit management
- Repository management
- Release automation
- Tag management

## Phase 3

- Issue automation
- Pull Request automation
- GitHub Assets

## Phase 4

- Zenodo support
- Jxiv support

## Phase 5

- AI development assistants
- Claude Code
- Codex
- GitHub Actions

---

# License

MIT License

---

# Vision

The long-term goal of Gyro Dev Tools is to provide a reusable Developer Toolkit capable of performing nearly all GitHub operations through simple command-line tools.

```text
python tools/<command>.py
```

The toolkit is designed not only for the Gyro projects but also for general OSS development and future AI-assisted software engineering workflows.