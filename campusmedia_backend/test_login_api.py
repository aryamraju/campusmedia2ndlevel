import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/users"

# Test login with the new student
print("=" * 60)
print("Testing Login API for New Student")
print("=" * 60)

login_data = {
    "email": "anu@gmail.com",
    "password": "123456",
    "role": "Student"
}

print(f"\nLogin Data: {json.dumps(login_data, indent=2)}")

response = requests.post(f"{BASE_URL}/login/", json=login_data)
print(f"\nStatus Code: {response.status_code}")
print(f"\nResponse Body:")
print(json.dumps(response.json(), indent=2))

if response.status_code == 200:
    user_data = response.json()['user']
    print("\n" + "=" * 60)
    print("✅ Login Successful!")
    print("=" * 60)
    print(f"User ID: {user_data['id']}")
    print(f"Name: {user_data['first_name']} {user_data['last_name']}")
    print(f"Role: {user_data['role']}")
    print(f"Profile Completed: {user_data.get('profile_completed', 'KEY NOT FOUND!')}")
    print("=" * 60)
else:
    print("\n❌ Login Failed!")
