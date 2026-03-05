# Contributing

Thank you for your interest in contributing to **FastAPI Global Exception Handling**! This document outlines the process and guidelines to follow when contributing.

---

## Table of Contents

- [Contributing](#contributing)
  - [Table of Contents](#table-of-contents)
  - [Code of Conduct](#code-of-conduct)
  - [Getting Started](#getting-started)
  - [Development Setup](#development-setup)
    - [Prerequisites](#prerequisites)
    - [Install Dependencies](#install-dependencies)
    - [Install Pre-commit Hooks](#install-pre-commit-hooks)
    - [Run the Development Server](#run-the-development-server)
  - [Project Structure](#project-structure)
  - [Making Changes](#making-changes)
  - [Commit Convention](#commit-convention)
    - [Types](#types)
    - [Examples](#examples)
  - [Pull Request Guidelines](#pull-request-guidelines)
    - [PR Title Format](#pr-title-format)
  - [Code Quality Standards](#code-quality-standards)
    - [Key requirements](#key-requirements)
  - [Running Tests](#running-tests)
  - [Discussions](#discussions)
  - [Reporting Issues](#reporting-issues)

---

## Code of Conduct

Please be respectful and constructive in all interactions. We are committed to providing a welcoming and inclusive environment for everyone.

---

## Getting Started

1. **Fork** the repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/your-username/fastapi-global-exception-handling.git
   cd fastapi-global-exception-handling
   ```
3. Add the upstream remote:
   ```bash
   git remote add upstream https://github.com/mouakos/fastapi-global-exception-handling.git
   ```

---

## Development Setup

### Prerequisites

- Python **3.13+**
- [uv](https://docs.astral.sh/uv/) — package and environment manager

### Install Dependencies

```bash
uv sync
```

### Install Pre-commit Hooks

```bash
uv run pre-commit install
```

This installs Ruff (lint + format) and Mypy checks that run automatically on every `git commit`.

### Run the Development Server

```bash
uv run uvicorn app.main:app --reload
```

---

## Project Structure

```
app/
├── api.py                  # API routes
├── exception_handlers.py   # Global exception handlers
├── exceptions.py           # Custom exception hierarchy
├── logging.py              # Loguru setup
├── main.py                 # App entry point
├── middleware.py           # Request logging middleware
├── schemas.py              # Pydantic models
└── utils.py                # Shared utilities
tests/
├── conftest.py             # Shared fixtures
└── test_error_routes.py    # Integration tests
```

---

## Making Changes

1. **Sync** your fork with upstream before starting:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create a branch** with a descriptive name:
   ```bash
   # For a new feature
   git checkout -b feat/add-rate-limit-error

   # For a bug fix
   git checkout -b fix/validation-error-details

   # For documentation
   git checkout -b docs/update-readme
   ```

3. **Make your changes** — keep them focused and atomic.

4. **Write or update tests** for any changed behaviour.

5. **Run the full quality check** before committing:
   ```bash
   uv run pre-commit run --all-files
   uv run pytest tests/ -v
   ```

---

## Commit Convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short description>
```

### Types

| Type       | Description                                             |
| ---------- | ------------------------------------------------------- |
| `feat`     | New feature                                             |
| `fix`      | Bug fix                                                 |
| `docs`     | Documentation only                                      |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `test`     | Adding or updating tests                                |
| `chore`    | Tooling, dependencies, config changes                   |
| `perf`     | Performance improvement                                 |

### Examples

```
feat(exceptions): add RateLimitError with 429 status
fix(handlers): return correct status code for http_exception_handler
docs(readme): update exception handler table
test(routes): add integration test for conflict error
refactor(schemas): simplify ErrorDetail model
```

---

## Pull Request Guidelines

- **Target the `main` branch** for all pull requests
- **Fill in the PR template** — describe what changed and why
- **Keep PRs small and focused** — one concern per PR
- **Ensure all checks pass** (pre-commit, tests, mypy) before requesting review
- **Link related issues** in the PR description using `Closes #issue-number`
- **Do not commit** `.venv/`, `__pycache__/`, `.mypy_cache/`, or other generated files

### PR Title Format

Follow the same Conventional Commits format:
```
feat(exceptions): add RateLimitError
fix(handlers): handle missing request client gracefully
```

---

## Code Quality Standards

All contributions must pass the following checks:

| Tool   | Purpose                | Command                   |
| ------ | ---------------------- | ------------------------- |
| Ruff   | Linting                | `uv run ruff check .`     |
| Ruff   | Formatting             | `uv run ruff format .`    |
| Mypy   | Type checking (strict) | `uv run mypy`             |
| pytest | Tests                  | `uv run pytest tests/ -v` |

### Key requirements

- All public functions and classes must have **Google-style docstrings**
- All functions must have **type annotations** (strict mypy mode is enforced)
- No unused imports, variables, or arguments
- Line length is managed by Ruff (max 100 characters)

---

## Running Tests

```bash
# Run all tests
uv run pytest
```

When adding a new exception or handler, add corresponding integration tests in `tests/test_error_routes.py` covering:
- Correct HTTP status code
- Correct `error.code` in the response body
- Expected `error.details` fields (if applicable)
- JSON `Content-Type` header

---

## Discussions

For questions, ideas, or open-ended feedback that are **not** bug reports, please use GitHub Discussions rather than opening an issue.

Use discussions for:

- **Questions** — "How do I extend the exception hierarchy?"
- **Ideas** — "Would it make sense to add a rate-limit error?"
- **Show & tell** — Share how you are using or extending this project
- **General feedback** — Suggestions that are not yet concrete enough for an issue

Keep issues reserved for confirmed bugs and actionable feature requests.

👉 [Open a Discussion](https://github.com/mouakos/fastapi-global-exception-handling/discussions/new)

---

## Reporting Issues

When opening a bug report, please include:

- Python version (`python --version`)
- FastAPI version (`uv run python -c "import fastapi; print(fastapi.__version__)"`)
- Minimal reproduction steps
- Expected vs actual behaviour
- Relevant log output

👉 [Open an Issue](https://github.com/mouakos/fastapi-global-exception-handling/issues/new)

---

Thank you for contributing! 🎉
