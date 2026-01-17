# MySQL Database Migration Guide

## Step 1: Install MySQL Server

### Option A: Using MySQL Installer (Recommended)
1. Download MySQL Installer from: https://dev.mysql.com/downloads/installer/
2. Choose "mysql-installer-community-8.0.x.msi"
3. Run installer and select "Server only" or "Full" installation
4. During setup:
   - Set root password (or leave empty for no password)
   - Keep default port: 3306
   - Start MySQL as Windows Service

### Option B: Using XAMPP (Easier)
1. Download XAMPP from: https://www.apachefriends.org/
2. Install XAMPP
3. Open XAMPP Control Panel
4. Start MySQL service

## Step 2: Verify MySQL Installation

Open PowerShell and test MySQL connection:

```powershell
# If using MySQL Installer, add to PATH or use full path
cd "C:\Program Files\MySQL\MySQL Server 8.0\bin"
.\mysql.exe -u root -p

# If using XAMPP
cd "C:\xampp\mysql\bin"
.\mysql.exe -u root -p
```

## Step 3: Create Database

After connecting to MySQL, run:

```sql
CREATE DATABASE IF NOT EXISTS campusmedia_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
SHOW DATABASES;
EXIT;
```

Or using command line directly:

```powershell
# MySQL Installer
"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -e "CREATE DATABASE campusmedia_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# XAMPP
"C:\xampp\mysql\bin\mysql.exe" -u root -e "CREATE DATABASE campusmedia_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

## Step 4: Update Django Settings

✅ **Already Done!** Your settings.py has been updated to:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'campusmedia_db',
        'USER': 'root',
        'PASSWORD': '',  # Change if you set a password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

**If you set a MySQL root password**, update the settings:
```python
'PASSWORD': 'your_mysql_password',
```

## Step 5: Run Migrations

```powershell
cd "c:\Users\Lenovo PC-4\Desktop\MES PRO\campus media project\fahad\campusmedia_backend"
python manage.py migrate
```

## Step 6: Import Data from SQLite

Your data has been backed up to `data_backup.json`. Import it:

```powershell
python manage.py loaddata data_backup.json
```

## Step 7: Verify Data Migration

```powershell
# Check if users are migrated
python manage.py shell
```

In Python shell:
```python
from users.models import User
print(f"Total users: {User.objects.count()}")
for user in User.objects.all():
    print(f"{user.email} - {user.role}")
exit()
```

## Step 8: Restart Server

```powershell
python manage.py runserver
```

---

## Troubleshooting

### Error: "Access denied for user 'root'"
- Check MySQL password in settings.py
- Test connection: `mysql -u root -p`

### Error: "Can't connect to MySQL server"
- Verify MySQL service is running
- Check port 3306 is not blocked
- For XAMPP: Start MySQL in XAMPP Control Panel
- For MySQL Service: Start service in Windows Services

### Error: "mysqlclient installation failed"
- Already installed ✅
- If issues: `pip install pymysql` then add to settings.py:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### Error: "Database doesn't exist"
- Create database manually using MySQL command line
- Or use phpMyAdmin (XAMPP includes this)

---

## Current Database Contents (SQLite Backup)

Your data backup includes:
- 5 users (admin, principal, students, staff)
- All user roles and permissions
- Registration data

This data will be preserved and imported to MySQL!

---

## Quick Commands Reference

```powershell
# Create database
mysql -u root -e "CREATE DATABASE campusmedia_db;"

# Backup SQLite data (already done)
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 4 -o data_backup.json

# Run migrations
python manage.py migrate

# Load data
python manage.py loaddata data_backup.json

# Create superuser (if needed)
python manage.py createsuperuser

# Run server
python manage.py runserver
```

---

## What Changed

1. ✅ Database engine: SQLite → MySQL
2. ✅ Settings updated in settings.py
3. ✅ Data backed up to data_backup.json
4. ✅ mysqlclient package installed
5. ⏳ Waiting for MySQL installation
6. ⏳ Need to create MySQL database
7. ⏳ Need to run migrations
8. ⏳ Need to import data

---

## Next Steps

1. **Install MySQL** (XAMPP is easiest for Windows)
2. **Start MySQL service**
3. **Create database** using commands above
4. **Run**: `python manage.py migrate`
5. **Import data**: `python manage.py loaddata data_backup.json`
6. **Test**: Login with existing users

All your data will remain intact! 🎉
