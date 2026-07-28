# FastAPI Example

A RESTful API service built with FastAPI for managing cloud infrastructure resources and application entities. The project provides CRUD endpoints for AWS-style resources (EC2 instances, RDS databases, Redis clusters, Subnets) alongside application-level entities (Projects, Users, Todos), with in-memory storage for rapid prototyping and testing.

## Features

### Cloud Infrastructure Resources

- **EC2 Instances** (`/api/v1/ec2`) — Create, list, retrieve, update, and delete virtual machine instances with attributes such as instance type, state, region, networking (VPC, IPs), and tags.
- **RDS Instances** (`/api/v1/rds`) — Manage relational database instances including engine type/version, storage, multi-AZ configuration, and connection endpoints.
- **Redis Clusters** (`/api/v1/redis`) — Manage Redis cache clusters with shard/replica topology, node types, and connection details.
- **Subnets** (`/api/v1/subnets`) — Manage VPC subnets with CIDR blocks, availability zones, IP capacity, and a dedicated tag management sub-API (GET/PUT/PATCH/DELETE on tags).

### Application Entities

- **Projects** (`/api/v1/projects`) — Manage projects with status tracking and membership. Supports adding/removing users as project members.
- **Users** (`/api/v1/users`) — User management with username, email, and phone uniqueness constraints. Includes a sub-endpoint to list a user's project memberships.
- **Todos** (`/api/v1/todos`) — Simple task tracking with title and completion status.

### Common Capabilities

- Paginated list endpoints with configurable page/size parameters
- Consistent error responses with structured error codes
- Input validation via Pydantic v2 schemas
- Health check endpoint at `/health`

## Technology Stack

| Component        | Technology                |
|------------------|---------------------------|
| Framework        | FastAPI ≥ 0.110           |
| Data Validation  | Pydantic ≥ 2.0           |
| ASGI Server      | Uvicorn ≥ 0.29 (standard) |
| Python           | ≥ 3.11                   |
| Testing          | pytest + HTTPX           |
| Linting          | Ruff                     |

## Quick Start

```bash
# Install dependencies
pip install -e .

# Run the development server
uvicorn app.main:app --reload

# Run tests
pip install -e ".[dev]"
pytest
```

The interactive API documentation is available at `/docs` (Swagger UI) and `/redoc` (ReDoc) when the server is running.
