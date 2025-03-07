# Parrot Backend

## 📖 Overview
Parrot is a language learning platform focused on improving pronunciation through AI-driven feedback. This repository contains the backend API and associated services for managing users, exercises, lessons, analytics, and more.

## 📂 Project Structure
```
.
├── app/                    # Main application logic
│   ├── admin/              # Admin panel and analytics
│   ├── crud/               # Database repositories (CRUD operations)
│   ├── models/             # Database models
│   ├── routers/            # API route handlers
│   ├── schemas/            # Pydantic schemas for request validation
│   ├── services/           # Business logic layer
│   ├── middleware/         # Middleware components
│   ├── utils/              # Utility functions
│   ├── resources/          # JSON files and static resources
│   ├── redis.py            # Redis caching setup
│   ├── database.py         # Database connection setup
│   ├── main.py             # FastAPI entry point
├── tests/                  # Unit and integration tests
├── data/                   # Language datasets (e.g., English, Portuguese)
├── Dockerfile              # Docker build file
├── docker-compose.yml      # Docker Compose setup
├── Makefile                # Makefile for common tasks
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Project metadata and dependencies
└── README.md               # This file
```

### Running Tests
To run tests using Docker:
```sh
make test
```

### API Documentation
Once the server is running, visit:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🛠 Development
### Running Development Mode
```sh
make dev
```

### Formatting & Linting
```sh
pre-commit run --all-files
```
