# Setup Steps for Copilot Coding Agent

This file provides setup instructions for the GitHub Copilot coding agent.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local development without Docker)

## Quick Start (Docker - Recommended)

```bash
# Clone the repository
git clone https://github.com/joshooaj/MuxMinus.git
cd MuxMinus

# Copy environment template and configure
cp .env.example .env

# Start all services
docker compose up -d

# View logs
docker compose logs -f
```

The application will be available at http://localhost:8000

## Local Development Setup

### Django Frontend (app/)

```bash
cd app

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Start development server
python manage.py runserver
```

### FastAPI Backend (backend/)

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the backend service
uvicorn app.main:app --reload --port 8001
```

## Environment Variables

Key environment variables for development:

```bash
DEBUG=true
SECRET_KEY=dev-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
BACKEND_URL=http://localhost:8001
SQUARE_ENVIRONMENT=sandbox
```

## Running Tests

```bash
cd app
python manage.py test
```

## Database

- **Development**: SQLite (automatic, no setup needed)
- **Production**: PostgreSQL (configure DATABASE_URL)

## Common Tasks

### Create a new Django migration

```bash
cd app
python manage.py makemigrations
python manage.py migrate
```

### Generate demo audio peaks

```bash
cd app
python manage.py generate_peaks
```

### Access Django admin
Navigate to http://localhost:8000/admin/ after creating a superuser.
