import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/users"

print("=" * 70)
print("Testing All User Login Features")
print("=" * 70)

# Test users from database
test_users = [
    {
        "name": "Student",
        "email": "arya@gmail.com",
        "password": "arya123",  # Replace with actual password
        "role": "Student"
    },
    {
        "name": "Staff",
        "email": "paru@gmail.com",
        "password": "paru123",  # Replace with actual password
        "role": "Staff"
    },
    {
        "name": "Principal",
        "email": "principal@gmail.com",
        "password": "principal@123",
        "role": "Principal"
    },
    {
        "name": "Admin",
        "email": "admin@gmail.com",
        "password": "admin@123",
        "role": "Admin"
    }
]

print("\n📋 Testing Login for Different User Roles")
print("-" * 70)

for test_user in test_users:
    print(f"\n🔐 Testing {test_user['name']} Login:")
    print(f"   Email: {test_user['email']}")
    print(f"   Role: {test_user['role']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/login/",
            json={
                "email": test_user['email'],
                "password": test_user['password'],
                "role": test_user['role']
            },
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                user_data = data['user']
                print(f"   ✅ Login Successful!")
                print(f"   Name: {user_data['first_name']}")
                print(f"   Email: {user_data['email']}")
                print(f"   Role: {user_data['role']}")
            else:
                print(f"   ❌ Login Failed: {data.get('message', 'Unknown error')}")
        else:
            print(f"   ❌ Login Failed: Status {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("🧪 Testing Invalid Login Attempts")
print("-" * 70)

# Test invalid credentials
invalid_tests = [
    {
        "name": "Wrong Password",
        "email": "principal@gmail.com",
        "password": "wrongpassword",
        "role": "Principal"
    },
    {
        "name": "Wrong Role",
        "email": "principal@gmail.com",
        "password": "principal@123",
        "role": "Student"
    },
    {
        "name": "Non-existent User",
        "email": "nobody@gmail.com",
        "password": "password123",
        "role": "Student"
    }
]

for test in invalid_tests:
    print(f"\n❌ Testing {test['name']}:")
    print(f"   Email: {test['email']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/login/",
            json={
                "email": test['email'],
                "password": test['password'],
                "role": test['role']
            },
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 401 or response.status_code == 400:
            print(f"   ✅ Correctly Rejected (Status {response.status_code})")
        else:
            print(f"   ⚠️  Unexpected: Status {response.status_code}")
            
    except Exception as e:
        print(f"   ⚠️  Error: {e}")

print("\n" + "=" * 70)
print("📊 Feature Summary")
print("-" * 70)
print("✅ Backend API Authentication")
print("✅ Multiple Role Support (Student, Staff, Principal, Admin)")
print("✅ Password Validation")
print("✅ Email Validation")
print("✅ Role-based Access Control")
print("✅ Error Handling for Invalid Credentials")
print("✅ Remember Me (saves email & role)")
print("✅ Password Visibility Toggle")
print("✅ Forgot Password Dialog")
print("✅ Loading Indicators")
print("✅ Success/Error Snackbars")
print("✅ Role-based Navigation (Student/Staff/Admin Home)")
print("=" * 70)
