# Contributing

Thank you for contributing to this project! This guide covers the conventions and workflow we follow.

## Getting Started

1. Fork and clone the repository.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt -r requirements-dev.txt
   ```
3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Commit Message Format

This project uses **conventional commits**. Every commit message must follow this format:

```
<type>: <short description>
```

### Allowed Types

| Type    | Purpose                                      |
|---------|----------------------------------------------|
| `feat`  | A new feature                                |
| `fix`   | A bug fix                                    |
| `test`  | Adding or updating tests                     |
| `docs`  | Documentation changes                        |
| `refactor` | Code restructuring without behavior change |
| `chore` | Maintenance, tooling, or dependency updates  |

### Examples

```
feat: implement EC2 resource CRUD router
fix: correct pagination offset in user listing
test: add unit tests for Redis resource endpoints
docs: update README with setup instructions
```

## Pull Request Workflow

1. Create a feature branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes with conventional commit messages.
3. Ensure all checks pass:
   ```bash
   ruff check .
   ruff format --check .
   pytest
   ```
4. Push your branch and open a pull request against `main`.
5. Fill out the PR template completely.

## Code Style

- Code is linted and formatted with [Ruff](https://docs.astral.sh/ruff/).
- Pre-commit hooks enforce formatting and linting automatically on each commit.
- Run `ruff format .` to auto-format and `ruff check --fix .` to auto-fix lint issues.

## Testing

- Tests use [pytest](https://docs.pytest.org/).
- Place tests in the `tests/` directory mirroring the source structure.
- Aim to cover both happy paths and edge cases.

## Issues

- Use the **Bug Report** template for reporting bugs.
- Use the **Feature Request** template for proposing new features.
