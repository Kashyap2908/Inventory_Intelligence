# Smart Inventory Management System

AI-powered inventory management system with trend analysis, automated notifications, and multi-user support.

## System Architecture

```
smart_inventory/
├── inventory/              # Main application
│   ├── models.py          # 9 database models
│   ├── views.py           # 20+ views & business logic
│   ├── forms.py           # Form definitions
│   ├── urls.py            # URL routing (25 endpoints)
│   ├── admin.py           # Admin panel config
│   ├── trend_calculator.py # AI trend scoring
│   └── management/commands/ # CLI commands
├── templates/             # 7 HTML templates
│   ├── login.html         # Animated login page
│   ├── signup.html        # User registration
│   ├── inventory_dashboard.html  # Inventory manager view
│   ├── admin_dashboard.html      # Admin control panel
│   ├── trend_dashboard.html      # AI trend analysis
│   ├── billing.html       # Multi-product billing
│   └── base.html          # Base template
├── static/               # CSS, JS, images
│   └── css/
│       ├── style.css      # Main styles
│       └── professional.css # Dashboard styles
├── smart_inventory/      # Django settings
│   ├── settings.py       # Configuration
│   ├── urls.py           # Root URL config
│   └── wsgi.py           # WSGI config
├── manage.py             # Django CLI
├── config.py             # API keys (optional)
├── requirements.txt      # Python dependencies
├── db.sqlite3           # SQLite database
└── Setup scripts:
    ├── add_all_products.py
    ├── setup_company_stock.py
    ├── add_inventory_stock.py
    ├── create_sample_bills.py
    └── set_realistic_trend_scores.py
```

## Features

### 1. User Management
- **Admin**: Full system control, team management, notifications
- **Inventory Manager**: Stock management, billing, order requests
- Role-based access control with user profiles

### 2. Stock Management
- FEFO (First Expiry First Out) stock rotation
- Multi-user stock tracking (company warehouse + individual stores)
- Expiry date monitoring with automated alerts
- Stock transfer system between company and stores

### 3. AI Trend Analysis
- Google Gemini AI integration for product trend scoring
- Automatic trend updates every 10 minutes
- Fallback to intelligent simulation when API quota exceeded
- Trend-based recommendations (increase stock, apply discount, etc.)

### 4. Notification System
- **Targeted notifications**: Admin can send to all inventory managers or specific individual users
- **Rich content**: Notifications include product details, recommendations, priority, and timestamps
- **Real-time panel** with priority levels (low, medium, high, urgent)
- **Full message modal**: Click "View Details" to see complete notification content in a modal dialog
  - Displays full message (no truncation)
  - Shows product information
  - Priority badge with color coding
  - Timestamp
  - Acknowledge button
- **Read tracking**: 
  - Per-user read status (each user has independent read/unread state)
  - Admin sees which specific users have read each notification
  - Progress bars showing read percentage (e.g., "2/3 Read - 67%")
  - Color-coded indicators (blue=unread, yellow=partial, green=all read)
- **Automatic notifications** for:
  - Low stock alerts (when stock < 10 units)
  - Expiry warnings (7 days, 3 days, expired)
  - Order approvals (with bill details)
  - Stock transfers (from company to stores)
  - Billing transactions (multi-product sales)
- **Notification types**: Admin messages, expiry warnings, low stock, overstock, reorder needed

### 5. Billing System
- Multi-product billing with barcode scanning
- Automatic stock deduction using FEFO
- Bill history and analytics
- Store-wise revenue tracking

### 6. Order Management
- Inventory managers can request products from company warehouse
- Admin approval workflow
- Automatic bill generation on approval
- Order status tracking

## Database Models

### Core Models
- **User**: Django auth user with role-based access (admin/inventory)
- **UserProfile**: Extended user info (role, full_name, store_name, store_location, phone_number, display_name)
- **Product**: Product catalog (name, category, price, cost_price, new_price, trend_score, last_trend_update)
- **ExpiryStock**: Stock batches with expiry dates, user-specific (product, user, quantity, expiry_date, created_at)
- **SalesBill**: Sales transactions (bill_number, created_by, total_amount, created_at)
- **SalesBillItem**: Individual items in bills (bill, product, quantity, price, total)
- **OrderQueue**: Product requests from inventory to admin (product, quantity, requested_by, status, approved_quantity, bill, expected_delivery_date)
- **Notification**: System notifications with read tracking (title, message, notification_type, priority, target_user_role, target_user, product, is_read, read_by, created_at, updated_at)
- **AIRecommendation**: AI-generated recommendations (product, recommendation_type, recommendation_text, trend_score, stock_level, status, applied_by, applied_at)

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Google Gemini API (Optional)
Create `config.py`:
```python
GOOGLE_API_KEY = 'your-api-key-here'
```

### 3. Initialize Database
```bash
python manage.py migrate
```

### 4. Create Demo Accounts
```bash
python manage.py create_demo_accounts
```

Creates:
- Admin: `Riya_Tank` / `admin123`
- Stores: `mumbai_store`, `delhi_store`, `bangalore_store` / `store123`
- Company warehouse: `company_stock`

### 5. Add Sample Products
```bash
python add_all_products.py
```

### 6. Setup Company Stock
```bash
python setup_company_stock.py
```

### 7. Run Server
```bash
python manage.py runserver 8003
```

Access at: `http://127.0.0.1:8003/`

## Key Features Explained

### Complete Notification Workflow Example

**Scenario**: Admin wants to alert Mumbai store about high-demand product

1. **Admin (Riya_Tank) sends notification**:
   - Goes to Admin Panel → Actions tab
   - Fills notification form:
     - Product: "Chocolates"
     - Category: "Packaged Foods"
     - Title: "Stock Alert - High Demand"
     - Message: "Trend score is 8.5/10. Increase stock by 50 units"
     - Send To: "Mumbai Store" (or "All Inventory Managers")
     - Priority: "High"
   - Clicks "Send Notification"
   - System creates notification with detailed message

2. **Mumbai Store (mumbai_store) receives notification**:
   - Logs into Inventory Dashboard
   - Sees notification badge with count
   - Notification appears in "New Notifications" section
   - Shows: Title, preview, HIGH priority badge, timestamp

3. **Mumbai Store views details**:
   - Clicks "View Details" button
   - Modal opens showing:
     - Full message with product details
     - Stock: 45 units, Trend: 8.5/10
     - Admin recommendation
     - Priority: HIGH (orange badge)
   - Reads complete information

4. **Mumbai Store acknowledges**:
   - Clicks "Acknowledge" button in modal
   - Notification moves to "Read Notifications" section
   - Shows green "READ" badge

5. **Admin tracks status**:
   - Goes to Admin Panel → Notifications tab
   - Sees notification card with:
     - "1/1 Read" badge (if sent to Mumbai only)
     - OR "1/3 Read - 33%" (if sent to all)
     - Progress bar: 33% filled (yellow)
     - "Read by: Mumbai Store" badge
   - Card has yellow border (partial read)

6. **Other stores (if sent to all)**:
   - Delhi and Bangalore stores still see it as unread
   - When they acknowledge, admin sees:
     - "2/3 Read - 67%" → "3/3 Read - 100%"
     - Progress bar fills to 100% (green)
     - All user badges shown
     - Card border turns green

### Notification System Details

**Admin View (Notifications Tab)**:
- Lists all sent notifications with full details
- Each notification card shows:
  - Title and truncated message
  - Target (all managers or specific user)
  - Product name (if applicable)
  - Read status: "X/Y Read" badge
  - Progress bar with percentage
  - List of users who have read it (with user badges)
  - Timestamp
- Color coding:
  - Blue border: No one has read yet (0%)
  - Yellow border: Some have read (1-99%)
  - Green border: All have read (100%)

**Inventory Manager View (Notifications Tab)**:
- Two sections: "New Notifications" and "Read Notifications"
- New notifications show:
  - Title with priority badge
  - Message preview (first 15 words)
  - Product name
  - Timestamp
  - "View Details" button (opens modal)
  - "Acknowledge" button (marks as read)
- View Details modal displays:
  - Full notification title
  - Priority badge (color-coded)
  - Complete message content (formatted)
  - Product information
  - Timestamp
  - Acknowledge button
- Read notifications show:
  - Same info but in "Read" section
  - Marked with green "READ" badge

**Notification Message Format**:
```
Product Details:
• Name: [Product Name]
• Category: [Category]
• Current Stock: [X] units
• Trend Score: [Y]/10

Admin Recommendation:
[Custom message from admin]

Notification Details:
• Priority: [LEVEL]
• Sent: [Date and Time]
• From: Admin ([Username])
```

### Stock Addition Flow
1. **Admin adds stock** → Goes to company warehouse
2. **Inventory manager adds stock** → Transfers from company warehouse using FEFO
3. System creates new batches with same expiry dates
4. Admin receives notification of transfer

### Billing Flow
1. Inventory manager creates bill
2. System checks user's own stock
3. Deducts stock using FEFO (oldest expiry first)
4. Generates bill with items
5. Admin receives notification

### Order Request Flow
1. Inventory manager requests product
2. Admin sees request in pending orders
3. Admin approves with quantity
4. System generates bill automatically
5. Stock transferred from company warehouse
6. Both parties receive notifications

### Notification Flow
1. **Admin creates notification** (all users or specific user)
   - Fills form with product, title, message, priority
   - Selects target: "All Inventory Managers" or specific user
   - System creates notification with detailed content
2. **Notification appears in target users' dashboards**
   - Shows in unread section with priority badge
   - Displays truncated message preview
3. **User views notification**
   - Clicks "View Details" button
   - AJAX call fetches full notification details
   - Modal opens with complete content:
     - Full message (no truncation, preserves formatting)
     - Product details
     - Priority level with color-coded badge
     - Timestamp
   - User clicks "Acknowledge" to mark as read
4. **Notification moves to read section**
   - Only for that specific user
   - Other users still see it as unread
5. **Admin tracks read status**
   - Sees read count (e.g., "2/3 Read")
   - Progress bar shows percentage
   - List of users who have read it
   - Color-coded cards (blue → yellow → green)

## Configuration Files

### config.py
```python
GOOGLE_API_KEY = 'your-key'  # Optional, for AI features
```

### settings.py (smart_inventory/)
- Database: SQLite (default)
- Static files: `/static/`
- Media files: `/media/`
- Timezone: Asia/Kolkata

## Management Commands

### Auto Update Trends
```bash
python manage.py auto_update_trends
```
Runs continuously, updates trend scores every 10 minutes.

### Manual Trend Update
```bash
python manage.py update_trend_scores
```

### Create Demo Accounts
```bash
python manage.py create_demo_accounts
```

## API Endpoints

- `/` - Home/Login
- `/signup/` - User registration
- `/inventory/` - Inventory dashboard
- `/admin-panel/` - Admin dashboard
- `/trends/` - Trend analysis dashboard
- `/billing/` - Billing interface
- `/mark-notification-read/<id>/` - Mark notification as read
- `/api/notification/<id>/` - Get full notification details (AJAX)
- `/api/search-products/` - Product search API
- `/api/search-products-billing/` - Billing product search
- `/api/product-autocomplete/` - Product autocomplete for forms

## Technology Stack

- **Backend**: Django 4.2.7, Python 3.x
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **AI**: Google Gemini API
- **Charts**: Chart.js

## Security Features

- CSRF protection on all forms
- Password hashing (Django default)
- Role-based access control
- Session management
- SQL injection prevention (Django ORM)

## Customization Guide

### Adding New User Roles
1. Update `UserProfile.ROLE_CHOICES` in `models.py`
2. Add role-specific views in `views.py`
3. Update templates with role checks

### Modifying Trend Calculation
Edit `inventory/trend_calculator.py`:
- `calculate_trend_score()` - Main AI logic
- `calculate_simulated_trend_score()` - Fallback logic

### Changing Notification Types
Update `Notification.NOTIFICATION_TYPES` in `models.py`

### Adjusting Stock Alerts
Modify thresholds in `generate_notifications()` in `views.py`

## Troubleshooting

### Notifications Not Showing
- **Check user role**: Only inventory users see inventory notifications
- **Check target**: Notification must be sent to "all" or specific user
- **Check read status**: Notification won't show if already acknowledged
- **Refresh page**: New notifications appear after page refresh
- **Check browser console**: Look for JavaScript errors

### Notification Content Empty
- Ensure all form fields are filled (product, category, title, message)
- Check that product exists in database
- Verify notification was created (check admin notifications tab)

### Read Status Not Updating
- Ensure user clicked "Acknowledge" button
- Check that mark-notification-read endpoint is accessible
- Verify CSRF token is present
- Check browser console for AJAX errors

### View Details Not Working
- Ensure Bootstrap 5 is loaded
- Check browser console for JavaScript errors
- Verify modal HTML is being generated
- Try refreshing the page

## Production Deployment

1. Change `DEBUG = False` in settings.py
2. Set `ALLOWED_HOSTS` in settings.py
3. Use PostgreSQL instead of SQLite
4. Configure static files with WhiteNoise or CDN
5. Use Gunicorn/uWSGI for WSGI server
6. Setup HTTPS with SSL certificate
7. Configure environment variables for secrets

## Support & Maintenance

### Database Backup
```bash
python manage.py dumpdata > backup.json
```

### Database Restore
```bash
python manage.py loaddata backup.json
```

### Clear Old Notifications
```python
from inventory.models import Notification
from datetime import timedelta
from django.utils import timezone
old = timezone.now() - timedelta(days=30)
Notification.objects.filter(created_at__lt=old, is_read=True).delete()
```

## License

Educational project - Free to use and modify

## Recent Updates

### Notification System Enhancements
- ✅ Individual user targeting in notification dropdown
- ✅ Full message display in modal (no truncation)
- ✅ AJAX-based notification details fetching
- ✅ Per-user read tracking with ManyToMany field
- ✅ Admin read status dashboard with progress bars
- ✅ Color-coded notification cards (blue/yellow/green)

### System Improvements
- ✅ Cleaned up debug statements
- ✅ Removed unnecessary documentation files
- ✅ Consolidated all docs into single README
- ✅ Fixed trend score calculation with fallback
- ✅ Enhanced error handling throughout

## Contributors

Developed for academic project submission
