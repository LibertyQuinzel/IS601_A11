IS601 Application – Modules 10 & 11

This repository contains a FastAPI application that manages Users and Calculations
with secure password handling, validation, database integration, and a full CI/CD pipeline.

It builds upon previous modules (Module 8, Module 10) and implements the
Calculation model with Pydantic validation and optional factory pattern.

--------------------------------------------------
Features

Secure User Model:
- SQLAlchemy model with hashed passwords (bcrypt)
- Unique constraints for username and email
- Pydantic schemas: UserCreate, UserRead
- Unit + integration tests

Calculation Model:
- SQLAlchemy model with fields a, b, type, result, user_id
- Supported operations: Add, Subtract, Multiply, Divide
- Pydantic schemas: CalculationCreate, CalculationRead
- Factory pattern to perform calculations
- Unit + integration tests
- Validation: no division by zero

CI/CD Pipeline:
- GitHub Actions workflow runs tests automatically on push or pull requests
- Spins up PostgreSQL service for integration tests
- Builds Docker image on successful tests
- Pushes Docker image to Docker Hub

--------------------------------------------------
Getting Started

1. Clone the Repository
> git clone https://github.com/LibertyQuinzel/IS601_A11.git
> cd IS601_A11

2. Install Dependencies
> python -m pip install --upgrade pip
> pip install -r requirements.txt

3. Set up PostgreSQL
- Local PostgreSQL server or Docker:
> docker run --name appdb -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=appdb -p 5432:5432 -d postgres:14

- Update DATABASE_URL if needed:
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/appdb

4. Run Tests
> pytest -q

- Tests are auto-discovered in the tests/ folder
- Integration tests use PostgreSQL database

--------------------------------------------------
Docker

Build Docker Image Locally:
> docker build -t your-dockerhub-username/module-app:latest .

Run Docker Container:
> docker run -d -p 8000:8000 your-dockerhub-username/module-app:latest

- The app should now be running on http://localhost:8000

--------------------------------------------------
CI/CD

- GitHub Actions workflow runs automatically on push/pull request to main
- PostgreSQL service runs during tests
- Docker image is built and pushed to Docker Hub after tests pass
- Ensure secrets are set in GitHub for:
  - DOCKERHUB_USERNAME
  - DOCKERHUB_TOKEN

--------------------------------------------------


