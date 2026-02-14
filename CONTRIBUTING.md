# Contributing to ChronicleMCP

Thank you for your interest in contributing to ChronicleMCP! This document outlines the process for contributing to the project.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- A GitHub account

### Setting Up Your Development Environment

1. **Fork the repository**

   Visit [chronicle-mcp](https://github.com/nikolasil/chronicle-mcp) and click the "Fork" button.

2. **Clone your fork locally**

   ```bash
   git clone https://github.com/YOUR_USERNAME/chronicle-mcp.git
   cd chronicle-mcp
   ```

3. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**

   ```bash
   pip install -e ".[dev]"
   ```

5. **Install pre-commit hooks**

   ```bash
   pre-commit install
   pre-commit install --hook-type commit-msg
   ```

## Development Workflow

1. **Create a new branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**

   Follow the code style guidelines below.

3. **Run tests**

   ```bash
   pytest
   ```

4. **Run linters and type checker**

   ```bash
   ruff check .
   ruff format .
   mypy .
   ```

5. **Commit your changes**

   We follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages:

   ```
   <type>[optional scope]: <description>

   [optional body]

   [optional footer(s)]
   ```

   Types:
   - `feat`: A new feature
   - `fix`: A bug fix
   - `docs`: Documentation only changes
   - `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
   - `refactor`: A code change that neither fixes a bug nor adds a feature
   - `perf`: A code change that improves performance
   - `test`: Adding missing tests or correcting existing tests
   - `chore`: Changes to the build process or auxiliary tools

   Example:
   ```
   feat(search): add date range filtering

   Allows users to search history within a specific date range
   using the new search_history_by_date tool.
   ```

6. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**

   Go to the [original repository](https://github.com/nikolasil/chronicle-mcp) and click "New Pull Request".

## Code Style Guidelines

### Python Code

- Follow PEP 8 (enforced by Ruff)
- Add type annotations to all function signatures
- Write docstrings for public functions and classes
- Keep line length to 100 characters maximum

Example:
```python
from typing import List, Optional


def get_browsers() -> List[str]:
    """
    Returns a list of available browser names.

    Returns:
        List of browser names detected on the system.
    """
    ...
```

### MCP Tools

- Decorate with `@mcp.tool()`
- Always return strings for AI consumption
- Include complete parameter documentation
- Validate all inputs before processing

Example:
```python
@mcp.tool()
def search_history(
    query: str,
    limit: int = 5,
    browser: str = "chrome",
) -> str:
    """
    Searches browser history for keywords.

    Args:
        query: Search term to look for in titles or URLs
        limit: Maximum number of results (1-100)
        browser: Browser to search (chrome, edge, firefox)

    Returns:
        Formatted list of matching history entries.
    """
    ...
```

### Testing

- Place tests in the `tests/` directory
- Name test files: `test_*.py`
- Use pytest fixtures for common setup
- Aim for 85%+ code coverage
- Test both success and error cases

Example:
```python
import pytest


def test_search_history_with_results(sample_chrome_db):
    """Test that search returns matching results."""
    from chronicle_mcp.core import HistoryService

    result = HistoryService.search_history("python", limit=5, browser="chrome", format_type="markdown")
    assert "python" in result["message"].lower()
```

## Reporting Bugs

1. **Search existing issues** to see if the bug has already been reported.

2. **Create a new issue** using the bug report template.

3. **Include**:
   - A clear description of the problem
   - Steps to reproduce
   - Expected behavior vs actual behavior
   - Python version, OS, and browser version
   - Any relevant error messages or logs

## Requesting Features

1. **Search existing issues** to see if the feature has been requested.

2. **Create a new issue** using the feature request template.

3. **Describe**:
   - The problem you're trying to solve
   - The proposed solution
   - Any alternatives you've considered
   - Use cases or examples

## Release Process

Releases are automated using GitHub Actions. The changelog is generated automatically from conventional commit messages using [git-cliff](https://git-cliff.org).

### Making a Release

1. Go to **Actions** → **Create Release** → **Run workflow**
2. Enter the version number (e.g., `1.4.0`)
3. Click **Run workflow**

This will automatically:
- Update version in `pyproject.toml`
- Generate changelog from commit history
- Commit and push changes
- Create a Git tag (e.g., `v1.4.0`)
- Trigger the full release workflow (builds, tests, PyPI publish, GitHub release)

### Commit Message Format

Since changelogs are auto-generated, use conventional commits:

| Type | Changelog Section |
|------|-------------------|
| `feat:` | Added |
| `fix:` | Fixed |
| `docs:` | Documentation |
| `refactor:` | Changed |
| `perf:` | Performance |
| `test:` | Testing |
| `chore:` | Miscellaneous |

Examples:
```
feat: add browser sync functionality
fix: resolve Firefox path detection on macOS
refactor: simplify CLI command structure
docs: update API documentation
```

## Questions?

- Open a [discussion](https://github.com/nikolasil/chronicle-mcp/discussions)
- Email the maintainer: iliopoulos.info@gmail.com

Thank you for contributing!
