# CampusMedia Backend API Documentation

## Server URL
`http://127.0.0.1:8000`

## API Endpoints

### 1. Register User
**Endpoint:** `POST /api/users/register/`

**Request Body:**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@campus.edu",
    "register_number": "STU001",
    "phone": "1234567890",
    "role": "Student",
    "password": "password123"
}
```

**Success Response (201):**
```json
{
    "success": true,
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@campus.edu",
        "register_number": "STU001",
        "phone": "1234567890",
        "role": "Student",
        "is_active": true,
        "created_at": "2026-01-16T10:47:00Z",
        "updated_at": "2026-01-16T10:47:00Z"
    }
}
```

**Error Response (400):**
```json
{
    "success": false,
    "message": "Email already registered"
}
```

---

### 2. Login User
**Endpoint:** `POST /api/users/login/`

**Request Body:**
```json
{
    "email": "john.doe@campus.edu",
    "password": "password123",
    "role": "Student"
}
```

**Success Response (200):**
```json
{
    "success": true,
    "message": "Login successful",
    "user": {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@campus.edu",
        "register_number": "STU001",
        "phone": "1234567890",
        "role": "Student",
        "is_active": true,
        "created_at": "2026-01-16T10:47:00Z",
        "updated_at": "2026-01-16T10:47:00Z"
    }
}
```

**Error Response (401):**
```json
{
    "success": false,
    "message": "Invalid credentials"
}
```

---

### 3. Get All Users
**Endpoint:** `GET /api/users/`

**Success Response (200):**
```json
{
    "success": true,
    "count": 2,
    "users": [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@campus.edu",
            "register_number": "STU001",
            "phone": "1234567890",
            "role": "Student",
            "is_active": true,
            "created_at": "2026-01-16T10:47:00Z",
            "updated_at": "2026-01-16T10:47:00Z"
        }
    ]
}
```

---

### 4. Get User by ID
**Endpoint:** `GET /api/users/<id>/`

**Success Response (200):**
```json
{
    "success": true,
    "user": {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@campus.edu",
        "register_number": "STU001",
        "phone": "1234567890",
        "role": "Student",
        "is_active": true,
        "created_at": "2026-01-16T10:47:00Z",
        "updated_at": "2026-01-16T10:47:00Z"
    }
}
```

**Error Response (404):**
```json
{
    "success": false,
    "message": "User not found"
}
```

---

## Testing the API

### Using curl:

**Register a user:**
```bash
curl -X POST http://127.0.0.1:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@campus.edu",
    "register_number": "TEST001",
    "phone": "1234567890",
    "role": "Student",
    "password": "testpass123"
  }'
```

**Login:**
```bash
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@campus.edu",
    "password": "testpass123",
    "role": "Student"
  }'
```

**Get all users:**
```bash
curl http://127.0.0.1:8000/api/users/
```

---

## Flutter Integration

Update your Flutter `UserService` to call these endpoints instead of using in-memory storage.

### Example:

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class UserService {
  static const String baseUrl = 'http://127.0.0.1:8000/api/users';
  
  Future<bool> registerUser(User user) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/register/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(user.toJson()),
      );
      
      if (response.statusCode == 201) {
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }
  
  Future<User?> loginUser(String email, String password, String role) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/login/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': email,
          'password': password,
          'role': role,
        }),
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return User.fromJson(data['user']);
      }
      return null;
    } catch (e) {
      return null;
    }
  }
}
```

---

## Running the Server

```bash
cd campusmedia_backend
python manage.py runserver
```

Server will run at: `http://127.0.0.1:8000`

Browse API at: `http://127.0.0.1:8000/api/users/`
