# New Django View Prompt

When creating a new Django view for Mux Minus, follow these patterns:

## View Structure

```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpRequest, HttpResponse

@login_required
def view_name(request: HttpRequest) -> HttpResponse:
    """
    Brief description of what this view does.
    
    Args:
        request: The HTTP request object
        
    Returns:
        Rendered template or redirect response
    """
    # View logic here
    
    context = {
        'key': 'value',
    }
    return render(request, 'core/template_name.html', context)
```

## Checklist

- [ ] Add type hints for request and return type
- [ ] Include docstring with description
- [ ] Use `@login_required` for authenticated views
- [ ] Use `messages.success/error/info` for user feedback
- [ ] Add URL pattern to `core/urls.py`
- [ ] Create corresponding template in `templates/core/`

## URL Pattern

```python
# In core/urls.py
path('your-path/', views.view_name, name='view_name'),
```

## Template

Templates should extend `base.html`:

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Page Title{% endblock %}

{% block content %}
<div class="container">
    <!-- Content here -->
</div>
{% endblock %}
```

## JSON API Endpoint

For API endpoints returning JSON:

```python
@login_required
@require_http_methods(["GET", "POST"])
def api_endpoint(request: HttpRequest) -> JsonResponse:
    """API endpoint description."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Process data
            return JsonResponse({'success': True, 'data': result})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'data': 'value'})
```
