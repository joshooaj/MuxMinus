# New Template Prompt

When creating a new Django template for Mux Minus, follow these patterns:

## Base Template Structure

All templates should extend `base.html`:

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Page Title{% endblock %}

{% block extra_css %}
<style>
    /* Page-specific styles - prefer adding to style.css instead */
</style>
{% endblock %}

{% block content %}
<section class="your-section">
    <div class="container">
        <!-- Content here -->
    </div>
</section>
{% endblock %}

{% block extra_js %}
<script>
    // Page-specific JavaScript
</script>
{% endblock %}
```

## CSS Variables

Use the CSS variables defined in `static/css/style.css`:

```css
/* Colors */
var(--primary)          /* #6366f1 - Primary brand color */
var(--primary-dark)     /* #4f46e5 - Darker primary */
var(--primary-light)    /* #818cf8 - Lighter primary */
var(--secondary)        /* #10b981 - Success/secondary green */
var(--danger)           /* #ef4444 - Error/danger red */
var(--warning)          /* #f59e0b - Warning amber */

/* Backgrounds */
var(--bg-primary)       /* #0f172a - Main background */
var(--bg-secondary)     /* #1e293b - Card/section background */
var(--bg-card)          /* #1e293b - Card background */

/* Text */
var(--text-primary)     /* #f8fafc - Primary text */
var(--text-secondary)   /* #94a3b8 - Secondary text */
var(--text-muted)       /* #64748b - Muted text */

/* Border radius */
var(--radius-sm)        /* 0.375rem */
var(--radius-md)        /* 0.5rem */
var(--radius-lg)        /* 0.75rem */
var(--radius-xl)        /* 1rem */
var(--radius-full)      /* 9999px - Fully rounded */
```

## Common Components

### Card
```html
<div class="card">
    <div class="card-header">
        <h3>Card Title</h3>
    </div>
    <div class="card-body">
        <!-- Content -->
    </div>
    <div class="card-footer">
        <!-- Actions -->
    </div>
</div>
```

### Buttons
```html
<a href="{% url 'view_name' %}" class="btn btn-primary">Primary</a>
<button type="submit" class="btn btn-secondary">Secondary</button>
<a href="#" class="btn btn-outline">Outline</a>
<button class="btn btn-danger">Danger</button>
<button class="btn btn-lg">Large</button>
<button class="btn btn-sm">Small</button>
```

### Form
```html
<form method="post">
    {% csrf_token %}
    <div class="form-group">
        <label class="form-label" for="field">Label</label>
        <input type="text" id="field" name="field" class="form-input" required>
        <span class="form-text">Helper text</span>
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### Alert Messages
```html
{% if messages %}
    {% for message in messages %}
    <div class="alert alert-{{ message.tags }}">
        {{ message }}
        <button class="alert-close">&times;</button>
    </div>
    {% endfor %}
{% endif %}
```

## URL References

Always use Django's URL template tag:
```html
<a href="{% url 'view_name' %}">Link</a>
<a href="{% url 'view_with_arg' arg_value %}">Link with arg</a>
```

## Static Files

```html
{% load static %}
<img src="{% static 'images/logo.svg' %}" alt="Logo">
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/script.js' %}"></script>
```

## Checklist

- [ ] Extend `base.html`
- [ ] Load static files with `{% load static %}`
- [ ] Set page title in `{% block title %}`
- [ ] Use CSS variables for colors/spacing
- [ ] Use existing component classes (card, btn, form-*, etc.)
- [ ] Create new components or templates for any elements that might be used more than once
- [ ] Include CSRF token in forms
- [ ] Use `{% url %}` for all links
- [ ] Mobile-responsive (test at 375px width)
