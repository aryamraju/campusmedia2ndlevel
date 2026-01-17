@echo off
echo ========================================
echo   CampusMedia SQLite to MySQL Migration
echo ========================================
echo.

echo Step 1: Starting MySQL Service...
echo Please start MySQL from XAMPP Control Panel
echo (The control panel should now be open)
echo.
pause

echo.
echo Step 2: Creating MySQL Database...
"C:\xampp\mysql\bin\mysql.exe" -u root -e "CREATE DATABASE IF NOT EXISTS campusmedia_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
if %errorlevel% == 0 (
    echo ✓ Database created successfully!
) else (
    echo ✗ Failed to create database. Make sure MySQL is running.
    pause
    exit /b 1
)

echo.
echo Step 3: Showing databases...
"C:\xampp\mysql\bin\mysql.exe" -u root -e "SHOW DATABASES;"

echo.
echo Step 4: Running Django migrations...
cd "c:\Users\Lenovo PC-4\Desktop\MES PRO\campus media project\fahad\campusmedia_backend"
python manage.py migrate

if %errorlevel% == 0 (
    echo ✓ Migrations completed successfully!
) else (
    echo ✗ Migration failed!
    pause
    exit /b 1
)

echo.
echo Step 5: Importing data from SQLite backup...
python manage.py loaddata data_backup.json

if %errorlevel% == 0 (
    echo ✓ Data imported successfully!
) else (
    echo ✗ Data import failed!
    pause
    exit /b 1
)

echo.
echo Step 6: Verifying data...
python -c "from django.core.management import execute_from_command_line; import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusmedia_backend.settings'); import django; django.setup(); from users.models import User; print(f'\n✓ Total users migrated: {User.objects.count()}'); [print(f'  - {user.email} ({user.role})') for user in User.objects.all()]"

echo.
echo ========================================
echo   Migration Completed Successfully! 🎉
echo ========================================
echo.
echo All your data has been migrated from SQLite to MySQL
echo.
echo Next steps:
echo 1. Restart your Django server: python manage.py runserver
echo 2. Test login with existing users
echo.
pause
