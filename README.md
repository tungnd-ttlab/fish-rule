# Fish rule

## 🎯 Features

- **Clean Architecture** design
- **SOLID** principles implementation with focus on Dependency Inversion
- **FastAPI** framework for high-performance API development
- **Session-based authentication** with secure password handling
- **SQLAlchemy** with async support for database operations
- **Dishka** for dependency injection
- **Alembic** for database migrations
- **Poetry** for dependency management
- **Docker** support for containerization
- **Pre-commit hooks** with Ruff for code quality

## 🏗️ Project Structure

```
src/
├── application/          # Application business rules
│   ├── interactors/      # Use cases implementation
│   ├── interfaces/       # Abstract interfaces (ports)
│   └── validators.py     # Validation rules
├── domain/               # Enterprise business rules
│   ├── entities/         # Business entities
│   └── exceptions.py     # Domain exceptions
├── infrastructure/       # External frameworks and tools
│   ├── adapters/         # Implementation of interfaces (adapters)
│   └── database/         # Database related code (SQLAlchemy)
├── main/                 # Application configuration
│   ├── ioc/              # Dependency injection setup
│   └── config.py         # Configuration management
└── presentation/         # Controllers and exception handlers
    └── controllers/      # API endpoints
```

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- Poetry
- Docker and Docker Compose (optional)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/fastapi-clean-architecture.git
cd fastapi-clean-architecture
```

2. Install dependencies:

```bash
#set poetry 
poetry config virtualenvs.in-project true
```

```bash
poetry install
```

3. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run migrations:

```bash
poetry run alembic upgrade head
```

### Running the Application

```bash
# Option 1: Using the run script (easiest)
./run.sh
./dev.sh #Run + watch  
# Option 2: Using PYTHONPATH directly
PYTHONPATH=./src poetry run uvicorn src.main.app:create_application --factory

# Option 3: With custom host and port
PYTHONPATH=./src poetry run uvicorn src.main.app:create_application --factory --host 0.0.0.0 --port 8000
```

**Note:** The `PYTHONPATH=./src` is required because the project uses `package-mode = false` in Poetry, so the `src` directory needs to be added to Python's module search path.

#### Using Docker:

```bash
docker-compose up -d
```

## 🔒 Authentication

The template includes session-based authentication with the following features:

- User registration with email and password
- Password validation and secure hashing with bcrypt
- User login with session creation
- Session management (creation, validation, deactivation)
- Integration with request handling

## 📖 API Documentation

Once the application is running, you can access:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔧 Configuration

Configuration is managed through environment variables and pydantic settings. Key configuration options:

- `APPLICATION_TITLE`: Application name
- `APPLICATION_DEBUG`: Debug mode flag
- `SESSION_*`: Session settings
- `POSTGRES_*`: Database connection settings
- `REDIS_*`: Redis connection settings

## 🧪 Architecture

This template strictly adheres to the Clean Architecture principles:

1. **Independence of frameworks**: Business logic is independent of the delivery mechanism (FastAPI)
2. **Testability**: Business rules can be tested without external elements
3. **Independence of UI**: The API can change without changing the business rules
4. **Independence of database**: You can swap SQLAlchemy for another ORM
5. **Independence of external agencies**: Business rules don't know about the outside world

The dependency flow follows the Dependency Inversion Principle:

- Domain layer has no dependencies
- Application layer depends only on the Domain layer
- Infrastructure and Presentation layers depend on the Application layer interfaces