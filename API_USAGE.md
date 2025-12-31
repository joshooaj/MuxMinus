# REST API Setup and Usage

This document explains how to set up and use the Mux Minus REST API.

## Database Migration

Before using the API feature, you need to run the database migration to add the `api_key` column:

```bash
# Copy migration script to backend container
docker compose cp backend/migration_add_api_key.py backend:/app/

# Run the migration
docker compose exec backend python migration_add_api_key.py
```

Alternatively, the migration can be run from within the container:

```bash
docker compose exec backend bash
python migration_add_api_key.py
exit
```

## Generating an API Key

### Via Web Interface

1. Log in to your Mux Minus account
2. Click the "API" button in the navigation menu
3. Click "Generate API Key"
4. Copy your API key and store it securely

**Important:** API keys provide full access to your account. Keep them secure and never share them publicly.

### Managing Your API Key

From the API page, you can:

- **Copy:** Copy your API key to the clipboard
- **Regenerate:** Create a new API key (invalidates the old one)
- **Delete:** Remove your API key entirely

## Using the API

### Authentication

Include your API key in the `Authorization` header of all requests:

```
Authorization: Bearer YOUR_API_KEY
```

API keys start with `sk_` prefix (e.g., `sk_abc123...`).

### Example: Upload a File

```bash
curl -X POST https://muxminus.com/upload \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@song.mp3" \
  -F "model=htdemucs" \
  -F "stem_count=4"
```

Response:
```json
{
  "id": "abc-123-def",
  "filename": "song.mp3",
  "model": "htdemucs",
  "status": "pending",
  "cost": 1.0,
  "created_at": "2025-01-01T12:00:00"
}
```

### Example: Check Job Status

```bash
curl https://muxminus.com/jobs/abc-123-def \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Response:
```json
{
  "id": "abc-123-def",
  "filename": "song.mp3",
  "model": "htdemucs",
  "status": "completed",
  "created_at": "2025-01-01T12:00:00",
  "completed_at": "2025-01-01T12:05:00"
}
```

### Example: Download Stems

```bash
# Download individual stem
curl https://muxminus.com/download/abc-123-def/vocals.wav \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -o vocals.wav

# Download all stems as ZIP
curl https://muxminus.com/download/abc-123-def \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -o stems.zip
```

### Example: List All Jobs

```bash
curl https://muxminus.com/jobs \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Response:
```json
{
  "jobs": [
    {
      "id": "abc-123-def",
      "filename": "song.mp3",
      "model": "htdemucs",
      "status": "completed",
      "created_at": "2025-01-01T12:00:00"
    }
  ]
}
```

## API Documentation

Complete API documentation is available in the web interface:

1. Log in to your account
2. Navigate to API → View Full API Documentation
3. Browse all endpoints, parameters, and response formats

Or visit: `https://muxminus.com/api-docs` (requires login)

## Supported Endpoints

All endpoints support both JWT (web UI) and API key authentication:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload` | Upload audio file for processing |
| GET | `/jobs` | List all jobs |
| GET | `/jobs/{job_id}` | Get specific job details |
| GET | `/jobs/{job_id}/stems` | List available stems |
| GET | `/download/{job_id}` | Download all stems (ZIP) |
| GET | `/download/{job_id}/{stem}` | Download individual stem |
| DELETE | `/jobs` | Delete multiple jobs |
| POST | `/jobs/{job_id}/retry` | Retry a failed job |
| POST | `/jobs/{job_id}/cancel` | Cancel a pending job |

## Python Example

```python
import requests

API_KEY = "YOUR_API_KEY"
BASE_URL = "https://muxminus.com"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# Upload a file
with open("song.mp3", "rb") as f:
    files = {"file": f}
    data = {"model": "htdemucs", "stem_count": 4}
    response = requests.post(f"{BASE_URL}/upload", headers=headers, files=files, data=data)
    job = response.json()
    job_id = job["id"]
    print(f"Job created: {job_id}")

# Check status
response = requests.get(f"{BASE_URL}/jobs/{job_id}", headers=headers)
status = response.json()
print(f"Status: {status['status']}")

# Download when complete
if status["status"] == "completed":
    response = requests.get(f"{BASE_URL}/download/{job_id}", headers=headers)
    with open("stems.zip", "wb") as f:
        f.write(response.content)
    print("Downloaded stems.zip")
```

## Rate Limits

Currently, no rate limits are enforced. Each job consumes 1 credit regardless of whether it's submitted via web UI or API.

## Troubleshooting

### 401 Unauthorized
- Check that your API key is correct
- Ensure the `Authorization` header includes "Bearer " prefix
- Verify your API key hasn't been regenerated or deleted

### 402 Payment Required
- Your account has insufficient credits
- Purchase more credits via the web interface

### 404 Not Found
- Job ID doesn't exist or doesn't belong to your account
- Check the job ID is correct

## Security Best Practices

1. **Never commit API keys to version control**
2. **Use environment variables** to store API keys
3. **Regenerate keys** if you suspect they've been compromised
4. **Use HTTPS** for all API requests
5. **Rotate keys periodically** for production applications

## Support

For issues or questions:
- GitHub Issues: [https://github.com/joshooaj/MuxMinus/issues](https://github.com/joshooaj/MuxMinus/issues)
- API Documentation: Built into the web interface
