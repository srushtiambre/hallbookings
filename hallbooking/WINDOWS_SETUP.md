# Windows Setup Instructions for College Hall Booking System

## 🪟 Windows-Specific Guide

This guide is optimized for Windows users (PowerShell and Command Prompt).

---

## ✅ Prerequisites Check

### 1. Verify Python Installation
Open PowerShell and run:
```powershell
python --version
```

**Expected output**: Python 3.8 or higher

If not installed:
1. Download from https://www.python.org/
2. Run installer
3. **Important**: Check "Add Python to PATH"
4. Restart PowerShell after installation

### 2. Verify pip
```powershell
pip --version
```

Should show pip version and Python location.

---

## 📂 Project Location

Your project is here:
```
c:\Users\Tejal\Desktop\HMS\hallbooking\
```

---

## 🚀 Step-by-Step Installation

### Step 1: Open PowerShell in Project Directory

1. Press `Win + X` and select "Windows PowerShell" or "Terminal"
2. Navigate to project:
```powershell
cd c:\Users\Tejal\Desktop\HMS\hallbooking
```

Verify you're in the right place:
```powershell
dir
```

You should see: manage.py, requirements.txt, README.md, etc.

### Step 2: Create Virtual Environment (Recommended)

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

**Important Notes**:
- You should see `(venv)` at the start of your PowerShell prompt
- If you get execution policy error, run:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- This ensures Python packages don't interfere with system Python

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

**What this installs**:
- Django 4.2.7
- python-dateutil 2.8.2

Wait for "Successfully installed" message.

### Step 4: Initialize Database

```powershell
python manage.py migrate
```

Creates the SQLite database with all tables.

**Expected output**:
```
Operations to perform:
  Apply all migrations: admin, auth, bookings, contenttypes, sessions
Running migrations:
  ... several lines of migration output ...
```

### Step 5: Create Admin Account

```powershell
python manage.py createsuperuser
```

Follow the prompts:
- Username: `admin` (or your choice)
- Email: `admin@college.edu` (or your email)
- Password: (choose a strong password)
- Password (again): (confirm)

### Step 6: Initialize Sample Halls

```powershell
python init_db.py
```

**Expected output**:
```
✓ Created hall: Auditorium A
✓ Created hall: Conference Hall B
✓ Created hall: Seminar Room C
✓ Created hall: Banquet Hall D

✓ Database initialization complete!
```

### Step 7: Start the Development Server

```powershell
python manage.py runserver
```

**Expected output**:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
April XX, 20XX - XX:XX:XX
Django version 4.2.7, using settings 'hallbooking.settings'
Starting development server at http://127.0.0.1:8000/
```

---

## 🌐 Access the Application

Once the server is running:

### Homepage
```
http://localhost:8000/
or
http://127.0.0.1:8000/
```

### Admin Panel
```
http://localhost:8000/admin/
```

Login with the credentials you created in Step 5.

---

## 🛑 Stopping the Server

In PowerShell:
```powershell
Ctrl + C
```

Then confirm: `Y` or `yes`

---

## ⚙️ Common Windows Issues & Solutions

### Issue 1: Python Not Recognized

**Error**: `python : The term 'python' is not recognized`

**Solution**:
1. Uninstall Python
2. Reinstall from https://www.python.org/
3. **Check**: "Add Python to PATH" during installation
4. Restart PowerShell

### Issue 2: Execution Policy Error

**Error**: `cannot be loaded because running scripts is disabled`

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 3: Port 8000 Already in Use

**Error**: `Address already in use`

**Solution**:
```powershell
python manage.py runserver 8001
```

Then visit: `http://localhost:8001/`

### Issue 4: Static Files Not Loading (CSS/Images Missing)

**Solution**:
```powershell
python manage.py collectstatic --noinput
```

### Issue 5: Database Locked Error

**Solution**:
```powershell
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python init_db.py
```

### Issue 6: Module Not Found Error

**Solution**:
1. Make sure virtual environment is activated (`(venv)` in prompt)
2. Reinstall dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

---

## 📝 Useful PowerShell Commands

### Navigate to Project
```powershell
cd c:\Users\Tejal\Desktop\HMS\hallbooking
```

### List Files
```powershell
dir
# or
ls
```

### Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### Deactivate Virtual Environment
```powershell
deactivate
```

### Check Python Version
```powershell
python --version
```

### Check Django Version
```powershell
python -m django --version
```

### View Database
```powershell
python manage.py shell
>>> from bookings.models import Hall
>>> Hall.objects.all()
<QuerySet [<Hall: ...>, ...]>
```

### Run Tests
```powershell
python manage.py test
```

---

## 🔄 Daily Workflow

Once set up, daily workflow is simple:

### Starting Development
```powershell
cd c:\Users\Tejal\Desktop\HMS\hallbooking
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

### Stopping
```powershell
Ctrl + C
```

### Deactivating Virtual Environment
```powershell
deactivate
```

---

## 💾 Backup & Reset

### Backup Database
```powershell
Copy-Item db.sqlite3 db.sqlite3.backup
```

### Restore Database
```powershell
Copy-Item db.sqlite3.backup db.sqlite3
```

### Reset Everything
```powershell
Remove-Item db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python init_db.py
python manage.py runserver
```

---

## 🚀 Next: Using the Application

1. Visit http://localhost:8000/
2. Browse available halls
3. Create a test account or use admin account
4. Try booking a hall
5. Approve booking in admin panel (/admin/)

---

## 📚 Documentation Files

Located in `c:\Users\Tejal\Desktop\HMS\hallbooking\`:

- **QUICKSTART.md** - 5-minute setup
- **README.md** - Feature documentation
- **SETUP_GUIDE.md** - Advanced setup
- **PROJECT_SUMMARY.md** - Project overview
- **This file** - Windows-specific guide

---

## 💡 Tips for Windows Users

1. **Use PowerShell**: More features than Command Prompt
2. **Virtual Environment**: Always use `venv` to avoid conflicts
3. **Path Issues**: Use forward slashes or raw strings
4. **File Permissions**: Run PowerShell as Administrator if needed
5. **Antivirus**: May slow down first-time migrations

---

## ✨ You're Ready!

Your setup should now be complete. 

**Quick Test**:
```powershell
python manage.py runserver
```

Visit: `http://localhost:8000/`

See the hall listing? Success! 🎉

---

## 📞 Troubleshooting Checklist

- [ ] Python installed and in PATH
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (pip install -r requirements.txt)
- [ ] Database migrated (python manage.py migrate)
- [ ] Superuser created
- [ ] Sample halls initialized (python init_db.py)
- [ ] Server running (python manage.py runserver)
- [ ] Can access http://localhost:8000/
- [ ] Can log in to admin panel

If all checked ✓, you're ready to go!

---

**Windows Setup Complete!** 🎊

Happy hall booking! 🏛️
