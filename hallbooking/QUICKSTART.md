# Quick Start Guide - College Hall Booking System

## 🚀 Get Up and Running in 5 Minutes

### Step 1: Install Dependencies
```bash
cd c:\Users\Tejal\Desktop\HMS\hallbooking
pip install -r requirements.txt
```

### Step 2: Set Up Database
```bash
python manage.py migrate
```

### Step 3: Create Admin Account
```bash
python manage.py createsuperuser
# Follow the prompts to create your admin account
```

### Step 4: Initialize Sample Halls
```bash
python init_db.py
```

### Step 5: Start the Server
```bash
python manage.py runserver
```

**Access the application:**
- 🏠 Homepage: http://localhost:8000/
- 🔐 Admin Panel: http://localhost:8000/admin/

---

## 📋 What You Can Do

### As a User
- ✅ Browse available halls
- ✅ View hall details and amenities
- ✅ Book a hall (requires login)
- ✅ Track your bookings
- ✅ Cancel pending bookings

### As an Admin
- ✅ Approve/Reject booking requests
- ✅ Manage halls and amenities
- ✅ View booking statistics
- ✅ Manage user accounts

---

## 🎨 UI Features

- **Modern Design**: Clean, professional interface
- **Responsive**: Works on desktop, tablet, and mobile
- **Fast Navigation**: Quick access to key features
- **Real-time Updates**: AJAX-based availability checking
- **Status Tracking**: Visual indicators for booking status

---

## 🔑 Default Test Accounts

After running `init_db.py`, you can use these test accounts:

**Admin Account:**
- Username: `admin`
- Password: (use the one you created with `createsuperuser`)

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `manage.py` | Django management tool |
| `requirements.txt` | Python dependencies |
| `init_db.py` | Initialize sample halls |
| `hallbooking/settings.py` | Application configuration |
| `bookings/models.py` | Database models |
| `bookings/views.py` | Application logic |
| `static/css/style.css` | Styling |
| `static/js/main.js` | JavaScript functionality |

---

## ⚙️ Common Commands

```bash
# Run the development server
python manage.py runserver

# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run tests
python manage.py test

# Access Django shell
python manage.py shell

# Collect static files (for production)
python manage.py collectstatic
```

---

## 🛠️ Customization

### Change the Hall Capacity
Edit `init_db.py` before running it, modify the `halls_data` list.

### Customize Colors
Edit `static/css/style.css` - Look for CSS variables at the top:
```css
:root {
    --primary: #6366f1;    /* Main color */
    --success: #10b981;    /* Success color */
    --danger: #ef4444;     /* Error color */
    /* ... */
}
```

### Add New Halls
Use the Django admin panel at `/admin/` → Bookings → Halls → Add Hall

---

## 🐛 Troubleshooting

**Issue: Port 8000 already in use**
```bash
python manage.py runserver 8001
```

**Issue: Static files not loading**
```bash
python manage.py collectstatic --noinput
```

**Issue: Need to reset database**
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python init_db.py
```

---

## 📞 Support

For detailed documentation, see `README.md`

**Features included:**
- Hall management (4 halls)
- User authentication
- Booking system with approval workflow
- Admin interface
- Modern responsive UI
- Availability checking
- Real-time validation

Enjoy your College Hall Booking System! 🎉
