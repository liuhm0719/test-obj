# FastAPI Example

A RESTful API built with FastAPI providing CRUD operations for managing cloud infrastructure resources and application entities. Designed as a reference project for building structured, testable Python APIs.

## Features

- **Todos** — Create, read, update, and delete todo items
- **Users** — User registration and management
- **Projects** — Project CRUD with user membership associations
- **EC2 Instances** — Manage EC2 instance records (create, list, get, update, delete)
- **RDS Instances** — Manage RDS database instance records
- **Redis Instances** — Manage Redis cache instance records
- Health check endpoint at `GET /health`
- Automatic interactive API docs at `/docs` (Swagger UI)

## Requirements

- Python >= 3.11

## Installation

```bash
# Clone the repository
git clone https://github.com/liuhm0719/test-obj.git
cd test-obj

# Install in development mode with dev dependencies
pip install -e '.[dev]'
```

## Make Targets

A Makefile wraps common development commands for discoverability:

```bash
make help      # Show all available targets
make install   # Install production dependencies
make dev       # Install dev dependencies and set up pre-commit hooks
make test      # Run the test suite
make lint      # Run ruff linter checks
make format    # Auto-format code with ruff
make run       # Start the development server
```

## Configuration

Copy the example environment file and adjust values as needed:

```bash
cp .env.example .env
```

Available environment variables:

| Variable      | Default   | Description                          |
|---------------|-----------|--------------------------------------|
| `APP_ENV`     | `dev`     | Application environment (dev / prod) |
| `APP_HOST`    | `0.0.0.0` | Server bind address                 |
| `APP_PORT`    | `8000`    | Server port                          |
| `APP_WORKERS` | `4`       | Uvicorn worker count (prod only)     |

## Running the Server

Using the included startup script (recommended):

```bash
bash run.sh
```

Or directly with uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive documentation.

## Running Tests

```bash
pytest
```

Tests are located in the `tests/` directory and cover all resource routers, health checks, and startup behavior.

## Pre-commit Hooks

This project uses [pre-commit](https://pre-commit.com/) to run ruff linting and formatting checks before each commit. The hooks mirror the `[tool.ruff]` configuration in `pyproject.toml`.

```bash
pip install pre-commit
pre-commit install
```

After installation, ruff will automatically check staged files on every `git commit`. To run the hooks manually against all files:

```bash
pre-commit run --all-files
```

## Project Structure

```
app/
├── main.py          # FastAPI application entry point
├── models/          # Data models (todo, user, ec2, rds, redis, project, membership)
├── routers/         # API route handlers
└── schemas/         # Pydantic request/response schemas
tests/               # Test suite
Makefile             # Development task runner (make help for targets)
run.sh               # Server startup script
pyproject.toml       # Project metadata and dependencies
.env.example         # Environment variable template
```

## API Endpoints

All resource endpoints are prefixed with `/api/v1`. Each resource supports standard CRUD operations:

| Resource   | Base Path             |
|------------|-----------------------|
| Todos      | `/api/v1/todos`       |
| Users      | `/api/v1/users`       |
| EC2        | `/api/v1/ec2`         |
| RDS        | `/api/v1/rds`         |
| Redis      | `/api/v1/redis`       |
| Projects   | `/api/v1/projects`    |

## License

This project is provided as-is for demonstration and learning purposes.
