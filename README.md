# Inventory Intelligence

AI-powered inventory management system built with Django. Supports multi-user stock tracking, FEFO-based billing, automated notifications, and trend-score analysis using either a built-in simulation engine or the Google Gemini AI API.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Architecture](#architecture)
4. [Technology Stack](#technology-stack)
5. [Database Models](#database-models)
6. [Setup](#setup)
7. [Running the Server](#running-the-server)
8. [Management Commands](#management-commands)
9. [Trend Analysis & AI Integration](#trend-analysis--ai-integration)
10. [API Endpoints](#api-endpoints)
11. [Security](#security)
12. [Project Structure](#project-structure)

---

## Project Overview

Inventory Intelligence is a full-stack Django application designed for retail inventory management. It provides:

- A role-based multi-user system (admin and inventory managers)
- Expiry-aware (FEFO) stock control with per-user tracking
- A billing module with automatic stock deduction
- An order-request workflow with admin approval
- A notification system with per-user read tracking
- A trend analysis dashboard powered by simulation (default) or Google Gemini AI (optional)

---

## Key Features

### User Management
- **Admin** — Full system control: manage users, approve orders, send notifications, view all stock
- **Inventory Manager** — Stock management, billing, order requests from the company warehouse
- Role-based access control enforced at every view

### Stock Management
- **FEFO (First Expiry First Out)** — Stock deducted oldest-expiry-first on every sale and transfer
- **Multi-user stock tracking** — Company warehouse and individual store inventories are kept separate
- **Expiry monitoring** — Automated alerts at 7 days, 3 days, and on expiry
- **Stock transfers** — Managers request stock; admin approves and transfers from the company warehouse

### Trend Analysis
See [Trend Analysis & AI Integration](#trend-analysis--ai-integration) for full details.

### Notification System
- Admin can send targeted notifications to all inventory managers or a specific user
- Notifications include product details, priority level, and a full message body
- Per-user read/unread tracking; admin sees a progress bar (e.g., "2/3 Read — 67%")
- Automatic notifications for low stock, expiry warnings, order approvals, transfers, and billing

### Billing System
- Multi-product billing with product search
- FEFO stock deduction on checkout
- Bill history with store-wise revenue tracking

### Order Management
- Inventory managers submit product requests to the company warehouse
- Admin reviews, approves a quantity, and the system auto-generates a bill and transfers stock

---

## Architecture

```
Inventory_Intelligence/
├── inventory/                    # Main Django application
│   ├── models.py                 # 9 database models
│   ├── views.py                  # 20+ views and business logic
│   ├── forms.py                  # Django form definitions
│   ├── urls.py                   # URL routing (25+ endpoints)
│   ├── admin.py                  # Django admin configuration
│   ├── trend_calculator.py       # Trend-score engine (simulation + AI)
│   └── management/commands/      # Custom CLI management commands
├── templates/                    # 7 HTML templates
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   ├── inventory_dashboard.html
│   ├── admin_dashboard.html
│   ├── trend_dashboard.html
│   └── billing.html
├── static/
│   └── css/
│       ├── style.css
│       └── professional.css
├── smart_inventory/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── add_all_products.py           # Seed script: product catalogue
└── setup_company_stock.py        # Seed script: company warehouse stock
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| Backend | Django 4.2.7, Python 3.x |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | HTML5, CSS3, Bootstrap 5, JavaScript |
| Charts | Chart.js |
| AI (optional) | Google Gemini API (`google-genai`) |

---

## Database Models

| Model | Description |
|---|---|
| `UserProfile` | Extends Django `User` with role, store name, location, and phone number |
| `Product` | Product catalogue: name, category, prices, ABC class, trend score, last update |
| `ExpiryStock` | Per-user stock batches with expiry dates and quantities |
| `SalesBill` | Sales transaction header (bill number, creator, total, timestamp) |
| `SalesBillItem` | Line items for each bill (product, quantity, price, subtotal) |
| `OrderQueue` | Stock requests from inventory managers to admin, with approval workflow |
| `Notification` | System notifications with priority, targeting, and per-user read tracking |
| `AIRecommendation` | AI-generated action recommendations linked to products |

---

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Apply Migrations

```bash
python manage.py migrate
```

### 3. Create Demo Accounts

```bash
python manage.py create_demo_accounts
```

This creates a set of demo users (admin and inventory manager roles) so you can explore the system immediately after setup.

### 4. Add Sample Products

```bash
python add_all_products.py
```

### 5. Set Up Company Stock

```bash
python setup_company_stock.py
```

---

## Running the Server

```bash
python manage.py runserver 8003
```

Access the application at `http://127.0.0.1:8003/`.

---

## Management Commands

### Continuous Trend Score Updater

```bash
# Simulation mode (default) — no API key required
python manage.py auto_update_trends

# AI mode — requires a valid GOOGLE_API_KEY in config.py
python manage.py auto_update_trends --use-ai

# Custom interval (default is 10 minutes)
python manage.py auto_update_trends --interval 30

# Run a single update cycle and exit
python manage.py auto_update_trends --once
```

The command runs as a long-lived process and updates all product trend scores on each cycle. Press **Ctrl+C** to stop gracefully.

### One-Shot Trend Score Update

```bash
# Simulation mode
python manage.py update_trend_scores

# AI mode
python manage.py update_trend_scores --use-ai
```

### Create Demo Accounts

```bash
python manage.py create_demo_accounts
```

### Database Utilities

```bash
# Backup
python manage.py dumpdata > backup.json

# Restore
python manage.py loaddata backup.json
```

---

## Trend Analysis & AI Integration

### How It Works

Trend scores (0–10 scale) reflect estimated product demand and drive recommendations such as "Increase Stock", "Apply Discount", or "Monitor". Scores are updated automatically when the Trend Dashboard is loaded and can also be refreshed on a schedule using `auto_update_trends`.

### Default: Simulation Mode

The system ships with an intelligent simulation engine (`trend_calculator.py`) that produces realistic, varied scores (3.0–9.0) without any external API calls. It factors in:

- **Category base score** — Electronics, Beverages, Dairy, etc. each have a baseline
- **Seasonal adjustments** — Beverages score higher in summer; snacks score higher during festival months
- **Stock-level signals** — Low stock implies high demand; oversupply depresses the score
- **Randomised variation** — Adds realistic spread so products do not converge to the same score

Simulation mode works offline, consumes no API quota, and is the recommended default.

### Optional: Google Gemini AI Mode

To use real AI-powered scoring:

1. **Create `config.py`** in the project root (it is already listed in `.gitignore`):
   ```python
   GOOGLE_API_KEY = "your-api-key-here"
   ```
   Obtain a key from <https://makersuite.google.com/app/apikey>.

2. **Pass `--use-ai`** to any trend command:
   ```bash
   python manage.py auto_update_trends --use-ai
   python manage.py update_trend_scores --use-ai
   ```
   The Trend Dashboard can also be switched to AI mode by changing `calculate_trend_score(product)` to `calculate_trend_score(product, force_ai=True)` in `inventory/views.py`.

> **Important:** `config.py` is listed in `.gitignore` and must **never** be committed to version control. Do not expose your API key in any tracked file.

If no valid key is present, the system falls back to simulation automatically — no crash, no data loss.

---

## API Endpoints

| Endpoint | Description |
|---|---|
| `/` | Login page |
| `/signup/` | User registration |
| `/inventory/` | Inventory manager dashboard |
| `/admin-panel/` | Admin control panel |
| `/trends/` | Trend analysis dashboard |
| `/billing/` | Billing interface |
| `/mark-notification-read/<id>/` | Mark a notification as read |
| `/api/notification/<id>/` | Fetch full notification details (AJAX) |
| `/api/search-products/` | Product search |
| `/api/search-products-billing/` | Billing-specific product search |
| `/api/product-autocomplete/` | Product autocomplete for forms |

---

## Security

- **CSRF protection** on all state-changing requests
- **Password hashing** via Django's default PBKDF2-based backend
- **Role-based access control** enforced at the view layer
- **Session management** handled by Django's session framework
- **SQL injection prevention** through Django ORM parameterised queries
- **API key isolation** — `config.py` is git-ignored; no secrets in tracked files

---

## Project Structure

```
inventory/
├── models.py              # Data layer: 8 models
├── views.py               # Business logic: 20+ views
├── forms.py               # Validated input forms
├── urls.py                # URL dispatch
├── admin.py               # Django admin registration
├── trend_calculator.py    # Simulation + Gemini AI trend engine
└── management/
    └── commands/
        ├── auto_update_trends.py    # Scheduled trend-score updater
        ├── create_demo_accounts.py  # Demo user seeder
        └── update_trend_scores.py  # One-shot trend updater
```

---

## License

MIT — free to use and modify.
