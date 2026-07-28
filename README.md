# fastapi-example

A FastAPI example project.

## Getting Started

### Prerequisites

- Python 3.11 or higher

### Setup

1. **Create and activate a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**

   ```bash
   # Production dependencies only
   make install

   # Development dependencies (includes pytest, ruff, pre-commit hooks)
   make dev
   ```

3. **Configure environment variables:**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` as needed. Available variables:

   | Variable | Default | Description |
   |----------|---------|-------------|
   | `APP_ENV` | `dev` | Application environment (`dev` or `prod`) |
   | `APP_HOST` | `0.0.0.0` | Server bind address |
   | `APP_PORT` | `8000` | Server port |
   | `APP_WORKERS` | `4` | Number of worker processes (prod only) |

4. **Run the application:**

   ```bash
   make run
   # or directly:
   bash run.sh
   ```

   In `dev` mode the server starts with hot-reload enabled.
