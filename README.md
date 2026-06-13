# SpendWise
## Spend wisely. Track confidently.

SpendWise is a mindful personal finance tracker built on Django and PostgreSQL. It helps users align their spending with the 50/30/20 budgeting framework — Fixed costs (50%), Fun spending (30%), and Future savings (20%) — with clear monthly tracking, visual feedback, and personalised targets.

This is the second iteration of this project. The first version was built in Flask and is available at [github.com/RichieG78/intentional-spending-tracker_db](https://github.com/RichieG78/intentional-spending-tracker_db). SpendWise represents a full architectural migration to Django, with meaningful feature extensions that demonstrate clear progression in framework maturity, design depth, and software engineering practice.

---

**Examiner test login:**
- Username: `richietester`
- Password: `test1111`
Use this for both the local sqlite and external logins.

---

## Live Application

- **Render URL:** https://django-spending-tracker.onrender.com
- **Repository:** https://github.com/RichieG78/django_spending_tracker.git
- **Render deployment walkthrough video:** https://www.loom.com/share/f0bf740933c24687a8c61532d0565fc7

> **Examiner note:** Please visit `https://django-spending-tracker.onrender.com/about/` first. This page explains the 50/30/20 budgeting method and provides step-by-step usage guidance.
>
> **Inspiration basis:** The app's core framing was inspired by the referenced video on the about page: https://www.youtube.com/watch?v=K4kDVLycBgk, especially its emphasis on intentional budgeting, category-based spending discipline, and planning ahead.

[1] YouTube (n.d.) *Video source for budgeting-method inspiration*. Available at: https://www.youtube.com/watch?v=K4kDVLycBgk (Accessed: 13 June 2026).

---

## Project Summary

SpendWise is a Django web application backed by PostgreSQL. It provides authenticated, per-user access to a personal finance dashboard where users can:

- record income sources with frequency and gross/net settings,
- log expenses across Fixed, Fun, and Future categories,
- set recurrence for each expense (weekly, monthly, yearly, one-off),
- track spending against personalised percentage targets per category,
- navigate monthly data with previous/next month controls,
- view a pie chart breakdown of total spend by category,
- view annual performance with a monthly bar chart and top expense table,
- receive smart recommendations generated from yearly spending patterns,
- update their profile, preferred currency (EUR/USD/GBP), and custom 50/30/20 targets,
- upload a profile picture that is automatically resized on save,
- reset forgotten passwords via a full email-based reset flow,
- access the Django Admin for direct data inspection and management.

---

## How to Use SpendWise

1. Register at `/register/` or log in at `/login/`.
2. Visit `/about` to read the budgeting methodology and watch the reference video.
3. Add at least one income source via the **Dashboard** using the Add Income button.
4. Add expenses across the Fixed, Fun, and Future columns via the **Spending Tracker** page.
5. Watch the progress bars — they compare your actual spend percentage against your target percentage. Bars turn red when a category exceeds its goal.
6. Use the **month navigation arrows** on the Spending Tracker to review past months.
7. View the **pie chart** on the Spending Tracker for a share-of-spend breakdown.
8. Return to the **Dashboard** for the annual performance section — monthly bar chart, biggest single expenses, and tailored recommendations.
9. Visit **Preferences** to update your username, email, profile picture, preferred currency, and custom spending targets.

---

## What Changed from Flask to Django

The Flask version was a functional proof of concept. SpendWise rebuilds it from the ground up using Django's architecture and extends the feature set in meaningful ways. The table below summarises the key differences.

| Area | Flask Version | Django (SpendWise) |
|---|---|---|
| **Framework** | Flask with manual wiring | Django with MTV architecture |
| **Authentication** | Flask-Login with custom routes | Django's built-in auth system — `LoginView`, `LogoutView`, `UserCreationForm`, `LoginRequiredMixin`, `UserPassesTestMixin` |
| **Password reset** | Not implemented | Full four-step email reset flow using Django's built-in `PasswordResetView` chain |
| **User model** | Custom SQLAlchemy `User` table | Django's built-in `User` with a `Profile` model via `OneToOneField` and signals |
| **Database ORM** | SQLAlchemy with manual session management | Django ORM with migrations, `ForeignKey`, `choices`, `DecimalField`, validators |
| **Views** | Function-based views only | Class-based views (`TemplateView`, `CreateView`, `UpdateView`, `DeleteView`, `DetailView`) plus mixins |
| **Forms** | Raw HTML form elements | Django `ModelForm` classes with field-level validation and crispy forms rendering |
| **CSRF protection** | Manually managed | Automatic via Django middleware and `{% csrf_token %}` |
| **Admin** | Not present | Django Admin with `list_display`, `list_filter`, `search_fields` for all models |
| **Ownership checks** | Not present | `UserPassesTestMixin` on all detail/update/delete views — users cannot access each other's data |
| **Profile / preferences** | Not implemented | Full preferences page: username, email, profile picture, currency, custom spending targets |
| **Currency** | EUR hardcoded | User-selectable: EUR, USD, GBP — applied globally via profile |
| **Custom targets** | Hardcoded 50/30/20 | User-defined percentages stored on Profile, validated to sum to 100 |
| **Month navigation** | Not present | Previous/next month navigation on dashboard and spending tracker |
| **Pie chart** | Not present | Chart.js doughnut showing share of total spend across Fixed, Fun, Future |
| **Left-to-allocate** | Not present | Per-category remaining budget shown on Spending Tracker |
| **Testing** | 4 basic tests | 18 behaviour-focused tests across dashboard and users test suites |
| **Signals** | Not present | `post_save` signals to auto-create and auto-save Profile on User creation |
| **Static files** | Served by Flask | Django staticfiles with `collectstatic` for production |
| **Deployment** | gunicorn only | gunicorn + whitenoise for static files, environment variable configuration |

---

## Assignment Requirements — Distinction Evidence

### 1. Django Concepts

**Distinction criterion:** Demonstrates strong ability to apply the key concepts of Django.

Evidence in this project:

- **MTV architecture** followed throughout: models in `models.py`, templates in `templates/`, views in `views.py` — clear separation of concerns.
- **Class-based views** used across all CRUD operations: `TemplateView`, `CreateView`, `UpdateView`, `DeleteView`, `DetailView`.
- **Mixins** applied for code reuse: `LoginRequiredMixin`, `UserPassesTestMixin`, and a custom `MonthlyFinanceContextMixin` that centralises all dashboard context logic.
- **URL namespacing** via named routes (`name='dashboard-home'`, `name='spending-tracker'`), referenced consistently with `{% url %}` tags.
- **Django template system** used throughout: `{% extends %}`, `{% block %}`, `{% load static %}`, `{% url %}`, `{% csrf_token %}`, `{% if %}`, `{% for %}`, template filters including `|date`, `|floatformat`, `|json_script`.
- **Django signals** (`post_save`) used to auto-create and auto-save a `Profile` record whenever a `User` is created or saved.
- **Django messages framework** provides flash message feedback after form submissions.
- **`reverse_lazy`** used as the `success_url` in CBVs to safely defer URL resolution.
- **App configuration** via `DashboardConfig` and `UsersConfig` in `apps.py`, with `ready()` used to import signals at startup.
- **`RedirectView`** used to preserve the legacy `/performance/` URL while pointing it at the new spending tracker route.
- **`json_script` template filter** used to safely pass Python data to JavaScript for Chart.js rendering without exposing unescaped data.

---

### 2. Database Integration in Django

**Distinction criterion:** Demonstrates strong ability to apply key concepts and principles of database integration in Django.

Evidence in this project:

- **Django ORM models** defined with full field types: `CharField`, `DecimalField`, `DateTimeField`, `ForeignKey`, `OneToOneField`, `ImageField`.
- **`choices` parameter** used on `Expense.type` and `Profile.preferred_currency` to enforce valid values at the database and form layer.
- **`DecimalField`** used for all monetary amounts — correct for financial data as it avoids floating-point precision errors.
- **Validators** applied to `Profile` target percentages via `MinValueValidator(0)` and `MaxValueValidator(100)`.
- **Relational schema with three models:**
  - `User` (Django built-in)
  - `Profile` — `OneToOneField` to `User`, auto-created via signal
  - `Expense` — `ForeignKey` to `User` with `CASCADE` delete
  - `Income` — `ForeignKey` to `User` with `CASCADE` delete
- **`db_table` Meta option** used on `Expense` and `Income` to maintain table name compatibility with the Flask schema.
- **Migrations** tracked across four dashboard migrations and four users migrations — full history preserved.
- **Query filtering** by user, month, and year using Django ORM: `.filter(user=self.request.user, date__month=selected_month, date__year=selected_year)`.
- **Aggregation** performed in Python using `sum()` with generator expressions over ORM querysets, maintaining `Decimal` precision throughout.
- **Django Admin** registered for `Expense`, `Income`, and `Profile` — an examiner can inspect all records directly at `/admin/`.
- **PostgreSQL** used in production; SQLite used in tests for isolation and speed.
- **`SQLALCHEMY_DATABASE_URI` replaced** with Django's `DATABASES` dict, configured from environment variables for both local and hosted environments.

---

### 3. Authentication and Authorisation

**Distinction criterion:** Demonstrates a strong understanding of integrating Authentication and Authorisation with Django.

Evidence in this project:

- **Django's built-in auth system** used throughout — no third-party auth library required.
- **`LoginRequiredMixin`** applied to every protected CBV in `views.py` — unauthenticated access redirects to `/login/`.
- **`@login_required`** decorator applied to function-based views in `users/views.py`.
- **`UserPassesTestMixin`** applied to all detail, update, and delete views with a `test_func` that checks both ownership (`request.user == object.user`) and in some cases type (`expense.type == self.get_expense_type()`). Users cannot read or modify another user's records — a 403 is returned.
- **`UserCreationForm`** extended with an email field for registration (`UserRegisterForm`).
- **`LoginView` and `LogoutView`** used from `django.contrib.auth.views` — no custom login/logout logic written.
- **Full password reset flow** implemented using Django's built-in four-step chain:
  - `PasswordResetView` — user submits email
  - `PasswordResetDoneView` — confirms email sent
  - `PasswordResetConfirmView` — user sets new password via token link
  - `PasswordResetCompleteView` — confirms reset complete
- **Email backend** configured in `settings.py` with SMTP settings read from environment variables.
- **`LOGIN_REDIRECT_URL`** and `LOGIN_URL` set in `settings.py` to control redirect behaviour after login and when redirecting unauthenticated users.
- **User profile update** (`/preferences/`) allows users to change username, email, profile picture, preferred currency, and spending targets — with both forms validated before saving.
- **CSRF protection** active on every POST form via Django middleware and `{% csrf_token %}` — explicitly noted in templates.
- **Password hashing** handled entirely by Django's auth system using PBKDF2 — no manual hashing code required.
- **`form.instance.user = self.request.user`** pattern used in all `CreateView` subclasses to ensure records are always assigned to the authenticated user, never trusting form input for ownership.

---

### 4. Clean Code Structure

**Distinction criterion:** Demonstrates a strong ability to create a clean code structure, including HTML templates, Bootstrap and JavaScript.

**File structure:**

```
django_spending_tracker/
├── dashboard/
│   ├── models.py          # Expense, Income models
│   ├── views.py           # CBVs, MonthlyFinanceContextMixin
│   ├── forms.py           # ExpenseCreateForm, IncomeCreateForm
│   ├── urls.py            # All dashboard URL routes
│   ├── admin.py           # Admin registrations
│   ├── tests.py           # 14 behaviour-focused tests
│   ├── migrations/        # 4 tracked migrations
│   ├── static/dashboard/
│   │   ├── main.css           # Full design system with CSS variables
│   │   ├── chart_layout.js    # Shared bar/target position logic
│   │   ├── dashboard_home.js  # Dashboard Chart.js bar chart
│   │   └── spending_tracker.js # Spending Tracker Chart.js pie chart
│   └── templates/dashboard/
│       ├── base.html          # Shared layout, navigation, messages
│       ├── home.html          # Dashboard page
│       ├── spending_tracker.html
│       ├── add_expense.html
│       ├── add_income.html
│       ├── expense_detail/form/confirm_delete.html
│       ├── income_detail/form/confirm_delete.html
│       └── about.html
├── users/
│   ├── models.py          # Profile model with OneToOneField
│   ├── views.py           # register, preferences, profile
│   ├── forms.py           # UserRegisterForm, UserUpdateForm, ProfileUpdateForm
│   ├── signals.py         # post_save handlers for Profile creation
│   ├── admin.py           # Profile registration
│   ├── tests.py           # 4 form-focused tests
│   ├── migrations/        # 4 tracked migrations
│   └── templates/users/
│       ├── login.html
│       ├── logout.html
│       ├── register.html
│       ├── profile.html
│       └── password_reset*.html (4 templates)
└── django_spending_tracker/
	 ├── settings.py
	 ├── urls.py
	 └── wsgi.py
```

**Code quality highlights:**

- `MonthlyFinanceContextMixin` centralises all shared dashboard context — income totals, expense totals, percentages, over-target flags, month navigation, chart data, and recommendations — in one reusable class rather than duplicating it across views.
- `ExpenseTypedMixin` and `ExpenseTypeCreateView` provide typed expense routes (fixed/fun/future) without duplicating view logic — each typed view is a one-liner subclass.
- JavaScript is separated by responsibility: `chart_layout.js` handles positional calculations shared across pages; `dashboard_home.js` owns the bar chart; `spending_tracker.js` owns the pie chart. No generic `scripts.js` filename.
- CSS custom properties (`--accent`, `--danger`, `--surface`, `--ink-muted` etc.) defined in `:root` — colours and shadows are consistent across every component without hardcoding.
- `ProfileUpdateForm.clean()` performs cross-field validation to ensure the three target percentages always sum to 100 before saving.
- All model `__str__` methods implemented for readable representation in Admin and shell.
- Docstrings on every class, method, and module.
- `{% csrf_token %}` present on every form — not added as an afterthought but applied consistently from the start.
- `crispy_forms` with `bootstrap5` pack used for form rendering — consistent, accessible form layout without duplicating HTML.
- `json_script` filter used to embed server data for Chart.js — avoids unsafe inline variable injection.

---

### 5. Hosted, Accessible, and Functional Web Application

**Distinction criterion:** Demonstrates strong evidence of a hosted Django app that is fully functional and accessible.

Evidence in this project:

- Application deployed on Render and publicly accessible at the URL above.
- `gunicorn django_spending_tracker.wsgi` used as the start command.
- `whitenoise` middleware configured for static file serving in production — no separate static server required.
- `python manage.py collectstatic` run as part of the Render build command.
- `DEBUG=False` and `ALLOWED_HOSTS` configured for production.
- `DATABASE_URL`, `SECRET_KEY`, `EMAIL_HOST_USER`, and `EMAIL_HOST_PASSWORD` set as environment variables in the Render dashboard — never hardcoded.
- Django migrations run as part of the Render build command.
- Superuser created via Render shell for Django Admin access.
- All core routes verified post-deployment: login, register, dashboard, spending tracker, add income, add expense, preferences, about, admin.

---

## Technical Stack

- Python 3
- Django 4.2
- PostgreSQL (production) / SQLite (tests)
- Django ORM
- Django Auth (`LoginView`, `LogoutView`, `UserCreationForm`, password reset chain)
- HTML + Django Templates (Jinja2-style)
- CSS with custom properties (no external CSS framework for core design)
- Bootstrap 4/5 (form layout via crispy_forms)
- JavaScript (Chart.js for bar and pie charts)
- Pillow (profile image resizing)
- gunicorn (deployment)
- whitenoise (static files in production)
- crispy_forms + crispy_bootstrap5

---

## Route Overview

**Public / auth:**
- `/login/` — sign in
- `/logout/` — sign out
- `/register/` — create account
- `/about/` — budgeting method and usage guide
- `/password-reset/` — request password reset
- `/password-reset/done/` — reset email sent
- `/reset/<uidb64>/<token>/` — set new password
- `/reset/complete/` — reset confirmed

**App pages (login required):**
- `/` — dashboard with income summary, target chart, annual performance, recommendations
- `/spending-tracker/` — monthly expense tracker with pie chart and month navigation
- `/preferences/` — update username, email, picture, currency, and spending targets

**Income CRUD:**
- `/add-income/` — create income
- `/income/<pk>/` — income detail
- `/income/<pk>/update/` — edit income
- `/income/<pk>/delete/` — delete income

**Expense CRUD (per type):**
- `/expenses/fixed/add/` — add fixed expense
- `/expenses/fixed/<pk>/` — fixed expense detail
- `/expenses/fixed/<pk>/update/` — edit fixed expense
- `/expenses/fixed/<pk>/delete/` — delete fixed expense
- *(same pattern for `/expenses/fun/` and `/expenses/future/`)*

**Admin:**
- `/admin/` — Django Admin for all models

---

## Automated Testing

Tests are split across two files:

**`dashboard/tests.py` — 14 tests across 4 test classes:**
- `DashboardViewTests`: auth redirect, template rendering, spending tracker rendering, legacy performance redirect, percentage context values, over-target flags, month filtering, and month navigation rollover across year boundary.
- `ExpenseTypedRouteTests`: typed route creates correct expense type, success flash message appears after create, fixed route rejects fun expense (403), and fun route rejects other user's expense (403).
- `IncomeModelTests`: `__str__` output includes the income name.
- `CreateMessageTests`: success flash message appears after income creation.

**`users/tests.py` — 4 tests:**
- Registration form accepts a valid new user payload.
- Update form saves and persists username changes.
- Profile form rejects non-image file uploads.
- Profile form rejects oversized uploads.

**Run tests locally:**

```bash
cd spend_wise
DATABASE_URL= DEBUG=True python manage.py test
```

Expected result: 18 tests run, all passing.

---

## Local Run Instructions

1. Clone the repository:
	```bash
	git clone https://github.com/RichieG78/django_spending_tracker.git
	cd django_spending_tracker/spend_wise
	```

2. Create and activate a virtual environment:
	```bash
	python -m venv venv
	source venv/bin/activate   # Windows: venv\Scripts\activate
	```

3. Install dependencies:
	```bash
	pip install -r requirements.txt
	```

4. Create a `.env` file in the `spend_wise/` directory:
	```
	SECRET_KEY=your-secret-key-here
	DATABASE_URL=postgres://user:password@localhost:5432/spendwise
	DEBUG=True
	EMAIL_HOST_USER=your-email@gmail.com
	EMAIL_HOST_PASSWORD=your-app-specific-password
	```

5. Apply migrations:
	```bash
	python manage.py migrate
	```

6. Create a superuser for admin access:
	```bash
	python manage.py createsuperuser
	```

7. Run the development server:
	```bash
	python manage.py runserver
	```

8. Open the app at `http://127.0.0.1:8000`

---

## Deploy and Access on Render

### 1. Push code to GitHub

Ensure the latest code is committed and pushed. Confirm the repository includes:
- `spend_wise/manage.py`
- `spend_wise/requirements.txt`
- `spend_wise/dashboard/`
- `spend_wise/users/`
- `spend_wise/django_spending_tracker/settings.py`

### 2. Create a PostgreSQL database on Render

1. Log in to Render.
2. Click **New +** → **PostgreSQL**.
3. Set a name and region.
4. After provisioning, copy the **Internal Database URL**.

### 3. Create the web service on Render

1. Click **New +** → **Web Service**.
2. Connect your GitHub repository.
3. Configure:
	- **Environment:** Python
	- **Root Directory:** `spend_wise`
	- **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
	- **Start Command:** `gunicorn django_spending_tracker.wsgi`
4. Choose your region, instance type, and branch.
5. Click **Create Web Service**.

### 4. Add required environment variables

In **Web Service Settings → Environment**, add:

| Key | Value |
|---|---|
| `SECRET_KEY` | A long random string (see below) |
| `DATABASE_URL` | Render PostgreSQL Internal Database URL |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app.onrender.com` |
| `EMAIL_HOST_USER` | Your Gmail address |
| `EMAIL_HOST_PASSWORD` | Your Gmail app-specific password |

Generate a secure `SECRET_KEY`:
```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

> Do not wrap values in quotes in the Render dashboard. Do not use your local `.env` file on Render.

### 5. Create an admin superuser on Render

After the first deploy succeeds, open the **Render Shell** for your web service and run:
```bash
python manage.py createsuperuser
```

### 6. Verify after deployment

Run this quick smoke test:

1. Open `/about` — confirm content loads.
2. Open `/dashboard` while logged out — confirm redirect to `/login/`.
3. Register a new account — confirm redirect to login.
4. Log in — confirm redirect to dashboard.
5. Add one income and one expense — confirm they display on the dashboard.
6. Navigate to a previous month — confirm month label and totals change.
7. Open `/admin/` with superuser credentials — confirm Expense, Income, and Profile records are visible.
8. Request a password reset at `/password-reset/` — confirm the reset email flow completes.

### 7. Common Render issues

| Symptom | Fix |
|---|---|
| 502/503 at startup | Check start command is exactly `gunicorn django_spending_tracker.wsgi` |
| Static files not loading | Confirm `whitenoise` is in `MIDDLEWARE` and `collectstatic` is in build command |
| Database errors | Recheck `DATABASE_URL` in Render environment — copy from PostgreSQL dashboard |
| Login redirect loop | Confirm `LOGIN_URL` and `LOGIN_REDIRECT_URL` are set in `settings.py` |
| Email reset not sending | Confirm `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are set and Gmail app passwords are enabled |

---

## Dependencies

Defined in `requirements.txt`:

- `django`
- `psycopg2-binary`
- `gunicorn`
- `whitenoise`
- `pillow`
- `django-crispy-forms`
- `crispy-bootstrap5`
- `python-dotenv`
- `dj-database-url`

---

## Examiner Note on Environment Variables and Secret Key

The `.env` file is added to `.gitignore` and is not stored in the repository. A copy of the `.env` file is included in the zipped submission folder so the examiner can verify that `SECRET_KEY`, `DATABASE_URL`, and email credentials are configured via environment variables and not hardcoded anywhere in the codebase.

---

## Distinction Positioning Summary

This submission targets distinction across all five rubric criteria by:

- using Django's built-in systems correctly and idiomatically rather than recreating Flask patterns inside Django,
- implementing the full Django auth stack including password reset, ownership enforcement, and user profile management,
- applying class-based views and mixins to eliminate repetition and demonstrate architectural understanding,
- building a relational schema with signals, validators, and migrations that show ORM depth beyond basic model definition,
- writing 18 behaviour-focused tests that verify auth, data isolation, percentage logic, month filtering, form validation, and user-facing success messages,
- extending the Flask feature set with month navigation, a personalised preferences system, currency selection, custom targets, and a pie chart — features that show clear progression and genuine product thinking,
- deploying a fully functional hosted application with proper static file handling, environment variable configuration, and a verified post-deployment smoke test.

---

## Comparison with Previous Flask Version

The Flask version demonstrated that the core budgeting concept worked. SpendWise demonstrates that the same concept can be built properly — with the framework doing the heavy lifting on auth, data integrity, form validation, and admin tooling — while the developer focuses on the product features that make it genuinely useful.

The previous Flask project is available for direct comparison at:
[github.com/RichieG78/intentional-spending-tracker_db](https://github.com/RichieG78/intentional-spending-tracker_db)