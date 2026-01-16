# Flutter ↔️ Django Backend Integration Complete! ✅

## What Changed

Your Flutter app now connects to the Django backend instead of using local storage.

### Updated Files:
1. **user_service.dart** - Now makes HTTP requests to Django API
2. **pubspec.yaml** - Added `http` package

---

## How It Works Now

### Registration Flow:
1. User fills registration form in Flutter
2. Flutter sends POST request to `http://127.0.0.1:8000/api/users/register/`
3. Django saves user to database
4. Django returns success/error response
5. Flutter shows appropriate message

### Login Flow:
1. User enters credentials in Flutter
2. Flutter sends POST request to `http://127.0.0.1:8000/api/users/login/`
3. Django checks credentials against database
4. Django returns user data if valid
5. Flutter navigates to appropriate home page

---

## Testing Steps

### 1. **Make Sure Django Server is Running**
```bash
cd campusmedia_backend
python manage.py runserver
```
Should see: `Starting development server at http://127.0.0.1:8000/`

### 2. **Run Flutter App**
```bash
cd campusmedia_frontend
flutter run
```

### 3. **Test Registration**
- Click "Sign Up" in Flutter app
- Fill in all fields:
  - First Name: Test
  - Last Name: User
  - Email: test@example.com
  - Register Number: TEST123
  - Phone: 1234567890
  - Role: Student
  - Password: test123
- Click "Sign Up"
- ✅ User should be saved to Django database

### 4. **Test Login**
- Go to Login page
- Enter:
  - Email: test@example.com
  - Password: test123
  - Role: Student
- Click "Sign In"
- ✅ Should login and navigate to Student Home

### 5. **Verify in Django Admin** (Optional)
```bash
# Create superuser if you haven't
python manage.py createsuperuser

# Visit http://127.0.0.1:8000/admin/
# Login and check Users table
```

---

## Important URLs

| Description | URL |
|------------|-----|
| Django Server | http://127.0.0.1:8000 |
| API Users List | http://127.0.0.1:8000/api/users/ |
| Register Endpoint | http://127.0.0.1:8000/api/users/register/ |
| Login Endpoint | http://127.0.0.1:8000/api/users/login/ |
| Django Admin | http://127.0.0.1:8000/admin/ |

---

## Device-Specific Backend URLs

### Current Configuration:
```dart
static const String baseUrl = 'http://127.0.0.1:8000/api/users';
```

### If Testing on Physical Device:
1. Find your computer's IP address:
   - Windows: `ipconfig` (look for IPv4 Address)
   - Mac/Linux: `ifconfig` or `ip addr`

2. Update in `user_service.dart`:
```dart
static const String baseUrl = 'http://YOUR_IP:8000/api/users';
// Example: 'http://192.168.1.100:8000/api/users'
```

3. Update Django settings to allow connections:
```python
# In campusmedia_backend/settings.py
ALLOWED_HOSTS = ['*']  # Or add your IP specifically
```

### If Testing on Android Emulator:
```dart
static const String baseUrl = 'http://10.0.2.2:8000/api/users';
```

---

## Troubleshooting

### ❌ "Connection refused" or "Failed to connect"
**Solutions:**
1. Check Django server is running: `python manage.py runserver`
2. Check URL matches (127.0.0.1 for desktop, 10.0.2.2 for emulator)
3. Check firewall isn't blocking port 8000

### ❌ "CORS Error" (if you see in logs)
**Already configured!** Django has CORS enabled in settings.py

### ❌ "Invalid credentials" but user was just registered
**Check:**
1. Did registration succeed? Check Django server logs
2. Is email, password, and role exactly the same?
3. Check Django admin panel to see if user exists

### ❌ Flutter app freezes on login
**Check:**
1. Is Django server running?
2. Check Flutter console for error messages
3. Try increasing timeout in user_service.dart

---

## Backend API Reference

### Register User
```http
POST /api/users/register/
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "register_number": "STU001",
  "phone": "1234567890",
  "role": "Student",
  "password": "secure123"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    ...
  }
}
```

### Login User
```http
POST /api/users/login/
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "secure123",
  "role": "Student"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "first_name": "John",
    ...
  }
}
```

---

## Next Steps

1. ✅ Registration saves to backend database
2. ✅ Login authenticates against backend
3. 🔲 Add loading indicators during API calls
4. 🔲 Add proper error handling for network failures
5. 🔲 Add token-based authentication (JWT)
6. 🔲 Store logged-in user session
7. 🔲 Add password reset functionality

---

## Testing Script

Want to test the backend directly? Run this:
```bash
cd campusmedia_backend
python test_api.py
```

This will test registration and login endpoints programmatically.
