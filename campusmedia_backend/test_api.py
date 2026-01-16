import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/users"

def test_user_registration():
    """Test user registration endpoint"""
    print("=" * 60)
    print("Testing User Registration API")
    print("=" * 60)
    
    # Test data matching the Flutter registration form
    test_user = {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@campus.edu",
        "register_number": "TEST001",
        "phone": "1234567890",
        "role": "Student",
        "password": "testpass123"
    }
    
    print("\n1. Registering new user...")
    print(f"Data: {json.dumps(test_user, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/register/", json=test_user)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("✅ User registered successfully!")
        user_id = response.json()['user']['id']
        return user_id
    else:
        print("❌ Registration failed!")
        return None


def test_user_login(email, password, role):
    """Test user login endpoint"""
    print("\n" + "=" * 60)
    print("Testing User Login API")
    print("=" * 60)
    
    login_data = {
        "email": email,
        "password": password,
        "role": role
    }
    
    print(f"\nLogin Data: {json.dumps(login_data, indent=2)}")
    
    response = requests.post(f"{BASE_URL}/login/", json=login_data)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✅ Login successful!")
    else:
        print("❌ Login failed!")


def test_get_all_users():
    """Test get all users endpoint"""
    print("\n" + "=" * 60)
    print("Testing Get All Users API")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/")
    print(f"\nStatus Code: {response.status_code}")
    data = response.json()
    print(f"Total Users: {data['count']}")
    print(f"Response: {json.dumps(data, indent=2)}")
    
    if response.status_code == 200:
        print("✅ Successfully retrieved users!")
    else:
        print("❌ Failed to retrieve users!")


if __name__ == "__main__":
    # Test 1: Register a new user
    user_id = test_user_registration()
    
    # Test 2: Try to login with the registered user
    if user_id:
        test_user_login("testuser@campus.edu", "testpass123", "Student")
    
    # Test 3: Get all users
    test_get_all_users()
    
    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)
