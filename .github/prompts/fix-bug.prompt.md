# Bug Fix Prompt

When debugging issues in Mux Minus, follow this systematic approach:

## Debugging Checklist

### 1. Reproduce the Issue
- [ ] Can you reproduce the issue consistently?
- [ ] What are the exact steps to reproduce?
- [ ] Does it happen in development, production, or both?

### 2. Check Common Sources

#### Django/Template Issues
- [ ] Check browser console for JavaScript errors
- [ ] Check Django server logs: `docker compose logs app`
- [ ] Verify template syntax (missing `{% endif %}`, `{% endblock %}`, etc.)
- [ ] Check URL configuration in `core/urls.py`
- [ ] Verify view function is returning correct response

#### Backend/API Issues
- [ ] Check FastAPI logs: `docker compose logs backend`
- [ ] Test endpoint directly with curl/Postman
- [ ] Verify `BACKEND_URL` environment variable
- [ ] Check `backend_client.py` for connection issues

#### Database Issues
- [ ] Check for pending migrations: `python manage.py showmigrations`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Check database connection in settings
- [ ] Verify model field types match expected data

#### Static Files Issues
- [ ] Run `python manage.py collectstatic`
- [ ] Check browser network tab for 404s
- [ ] Verify `{% load static %}` at top of template
- [ ] Clear browser cache

#### Authentication Issues
- [ ] Check `@login_required` decorator
- [ ] Verify `LOGIN_URL` setting
- [ ] Check session/cookie settings
- [ ] Test with fresh browser/incognito

### 3. Production-Specific Issues

#### CSRF Errors
- [ ] Verify `CSRF_TRUSTED_ORIGINS` includes your domain with `https://`
- [ ] Check `SECURE_PROXY_SSL_HEADER` is set for reverse proxy
- [ ] Ensure form includes `{% csrf_token %}`

#### Static Files Not Loading
- [ ] Run `collectstatic` during Docker build
- [ ] Verify WhiteNoise middleware is configured
- [ ] Check STATIC_ROOT and STATIC_URL settings

#### Payment Issues (Square)
- [ ] Sandbox uses: `https://sandbox.web.squarecdn.com/v1/square.js`
- [ ] Production uses: `https://web.squarecdn.com/v1/square.js` (NO prefix!)
- [ ] Verify `SQUARE_ENVIRONMENT` is set correctly
- [ ] Check Square dashboard for payment errors

### 4. Useful Commands

```bash
# View all logs
docker compose logs -f

# View specific service logs
docker compose logs -f frontend
docker compose logs -f backend

# Django shell for debugging
docker compose exec frontend python manage.py shell

# Check database
docker compose exec frontend python manage.py dbshell

# Restart services (rarely useful)
docker compose restart

# Full rebuild
docker compose up -d --build
```

### 5. Adding Debug Logging

```python
import logging
logger = logging.getLogger(__name__)

# In your view/function
logger.debug(f"Debug info: {variable}")
logger.info(f"Processing: {data}")
logger.warning(f"Unexpected state: {state}")
logger.error(f"Error occurred: {error}")
```

### 6. Browser DevTools Checks

- **Console**: JavaScript errors
- **Network**: Failed requests, response codes, response bodies
- **Application**: Cookies, Local Storage, Service Worker status
- **Elements**: Check rendered HTML matches expected

### 7. Web UI Testing

- **Playwright**: Use the Playwright MCP to diagnose or verify frontend changes

## Fix Verification

After fixing:
- [ ] Issue no longer reproduces
- [ ] No new errors in console/logs
- [ ] Related functionality still works
- [ ] Test on mobile viewport if UI-related
