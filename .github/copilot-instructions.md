# Mux Minus Project Architecture and Standards

## Overview

Mux Minus is an open-source web application and API on top of the demucs project
created by Facebook Research. Read more about demucs at https://github.com/facebookresearch/demucs.

In short, demucs accepts a music file in any common format and using an AI model
it will separate one or more elements of the song into two or more files. For
example, a two-stem output might produce one file with just the vocals from the
original file, and the second file would contain everything else. And a four-stem
output would produce files for vocals, bass, drums, and "other" containing the
remaining audio elements that could not be classified. There is also a six-stem
model capable of isolating the wave forms for guitar and piano in addition to the
other elements.

The Mux Minus application sits on top of demucs and includes a traditional
product landing page at the root of the website explaining what you can do and
demonstrating it with a sample song that has already been processed into both
two stems isolating vocals, and six stems.

Users must register with an email address, and new accounts are provided with
three free credits allowing them to process three music files. If they like the
tool, they can purchase additional credits in packs of 5, 25, or 100 at a price
of $1.00, $4.00, and $15.00 respectively.

## Current Implementation Status

### Completed Features
- Landing page with feature highlights, pricing, and call-to-action
- User registration and authentication (email/password)
- User dashboard showing job history and credit balance
- Job creation with file upload, model selection, and stem configuration
- Job detail page with waveform audio players (WaveSurfer.js)
- Demo page showcasing pre-processed sample audio with interactive waveform players
- Credit system with Square payment integration
- Profile management (change password, delete account)
- PWA support (manifest.json, service worker, installable on mobile)
- Social card / Open Graph meta tags
- Favicon and PWA icons

### Not Yet Implemented
- REST API for programmatic access
- Social sign-on (GitHub, Facebook, etc.)
- API token generation in user profile
- Automatic file cleanup after 24 hours (cron job or scheduled task)

## Architecture

### Frontend (Django App)

Located in `app/` directory:

- **Framework**: Django 5.x with server-side templates
- **Static Files**: `app/static/` - CSS, JavaScript, images, PWA assets
- **Templates**: `app/templates/` - Jinja2-style Django templates
- **Styling**: Custom CSS with CSS variables for theming (`static/css/style.css`)
- **Audio Playback**: WaveSurfer.js for waveform visualization and playback

Key files:
- `app/core/views.py` - All view functions (landing, auth, jobs, payments)
- `app/core/models.py` - User, Job, CreditPackage models
- `app/core/forms.py` - Django forms for registration, login, job creation
- `app/core/payments.py` - Square payment integration
- `app/core/backend_client.py` - HTTP client for FastAPI backend
- `app/core/urls.py` - URL routing
- `app/muxminus/settings.py` - Django settings (uses environment variables)

### Backend (FastAPI Service)

Located in `backend/` directory:

- **Framework**: FastAPI
- **Purpose**: Internal service that wraps the demucs CLI
- **Job Queue**: Manages concurrent job processing with configurable limits

Key files:
- `backend/app/main.py` - FastAPI application and endpoints
- `backend/app/separator.py` - Demucs CLI wrapper
- `backend/app/queue.py` - Job queue management
- `backend/app/models.py` - Pydantic models for API requests/responses
- `backend/app/config.py` - Configuration settings

### Database

- **Production**: PostgreSQL (configured via DATABASE_URL environment variable)
- **Development**: SQLite (`app/db.sqlite3`)

### Key Models

```python
# User model (extends AbstractUser)
- email (unique, used for login)
- credits (integer, default 3)

# Job model
- id (UUID primary key)
- user (ForeignKey to User)
- original_filename
- model_name (htdemucs, htdemucs_6s)
- stem_type (for 2-stem jobs: vocals, drums, bass)
- output_format (mp3, wav)
- status (queued, processing, completed, failed)
- created_at, completed_at
- error_message (if failed)

# CreditPackage model
- name, credits, price_cents
- Pre-seeded via migration: Starter (5/$1), Popular (25/$4), Pro (100/$15)
```

## Environment Variables

The Django app uses these environment variables (see `docker-compose.yml`):

```
DEBUG=false                          # Set to false in production
SECRET_KEY=<random-string>           # Django secret key
ALLOWED_HOSTS=muxminus.com           # Comma-separated list
CSRF_TRUSTED_ORIGINS=https://muxminus.com  # Required behind reverse proxy
DATABASE_URL=postgres://user:pass@host:port/db
BACKEND_URL=http://backend:8000      # Internal FastAPI service URL
SQUARE_ACCESS_TOKEN=<token>          # Square API access token
SQUARE_LOCATION_ID=<location>        # Square location ID
SQUARE_APP_ID=<app-id>               # Square application ID
SQUARE_ENVIRONMENT=sandbox|production  # Square environment
```

## Deployment

### Docker Compose

The project uses docker-compose with three services:

1. **app** - Django frontend (port 8000)
2. **backend** - FastAPI service (port 8000, internal only)
3. **db** - PostgreSQL database

Shared volumes:
- `uploads` - User uploaded files
- `outputs` - Demucs output stems

### Production Setup

- Runs behind Traefik reverse proxy
- Uses `SECURE_PROXY_SSL_HEADER` to trust X-Forwarded-Proto header
- WhiteNoise serves static files
- Service worker and manifest.json served from root URLs

## Payment System

Payments are processed through Square Web Payments SDK:

- **Sandbox URL**: `https://sandbox.web.squarecdn.com/v1/square.js`
- **Production URL**: `https://web.squarecdn.com/v1/square.js` (no prefix!)
- Integration in `app/core/payments.py` using `squareup` Python SDK
- Payment form in `app/templates/core/purchase.html`

## File Structure

```
├── app/                    # Django frontend application
│   ├── core/              # Main Django app
│   ├── muxminus/          # Django project settings
│   ├── static/            # CSS, JS, images, PWA assets
│   │   ├── css/style.css  # Main stylesheet
│   │   ├── js/            # JavaScript (waveform-player.js)
│   │   ├── images/        # Logos, favicons, social card
│   │   │   └── pwa/       # PWA icons (multiple sizes)
│   │   ├── demo/          # Demo audio peaks JSON files
│   │   ├── manifest.json  # PWA manifest
│   │   └── sw.js          # Service worker
│   ├── templates/         # Django templates
│   │   ├── base.html      # Base template with navbar, footer, meta tags
│   │   └── core/          # Page templates
│   └── media/             # User uploads and outputs
├── backend/               # FastAPI backend service
│   └── app/              # FastAPI application
├── docker-compose.yml     # Production compose file
└── docker-compose.override.yml  # Development overrides
```

## Coding Standards

### Django Templates
- Extend `base.html` for consistent layout
- Use `{% load static %}` for static file URLs
- Use Django template tags for URLs: `{% url 'view_name' %}`

### CSS
- Use CSS variables defined in `:root` for colors, spacing, etc.
- Follow BEM-like naming for component classes
- Mobile-first responsive design with media queries

### JavaScript
- Vanilla JS preferred over frameworks
- Use `data-` attributes for JavaScript hooks
- Service worker provides offline caching for static assets

### Python
- Follow PEP 8 style guidelines
- Use type hints where practical
- Environment variables for all configuration