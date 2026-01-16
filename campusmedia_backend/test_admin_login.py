import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/users"

print("=" * 60)
print("Testing Admin Login")
print("=" * 60)

# Test admin login
admin_credentials = {
    "email": "admin@gmail.com",
    "password": "admin@123",
    "role": "Admin"
}

print(f"\nAttempting admin login...")
print(f"Email: {admin_credentials['email']}")
print(f"Password: {admin_credentials['password']}")
print(f"Role: {admin_credentials['role']}")

try:
    response = requests.post(
        f"{BASE_URL}/login/",
        json=admin_credentials,
        headers={'Content-Type': 'application/json'},
        timeout=5
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("\n✅ Admin login successful!")
            print(f"Admin User: {data['user']['first_name']} ({data['user']['email']})")
        else:
            print("\n❌ Login failed!")
    else:
        print("\n❌ Login failed with status code:", response.status_code)
        
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 60)
