import requests
import json

# Test staff details update
print("Testing Staff Details Update API...")
print("-" * 50)

# Staff user ID (from our created staff user)
staff_user_id = 3  # Adjust this based on your database

# Test data
staff_data = {
    "user_id": staff_user_id,
    "qualification": "M.Sc Physics, B.Ed",
    "subject_expertise": "Physics, Mathematics",
    "assigned_classes": "10th Grade Physics\n12th Grade Advanced Math",
    "experience_years": "8"
}

# Make POST request
response = requests.post(
    'http://127.0.0.1:8000/api/users/update-staff-details/',
    headers={'Content-Type': 'application/json'},
    data=json.dumps(staff_data)
)

print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

print("\n" + "=" * 50 + "\n")

# Test student details update
print("Testing Student Details Update API...")
print("-" * 50)

# Student user ID (adjust based on your database)
student_user_id = 4  # Adjust this

# Test data
student_data = {
    "user_id": student_user_id,
    "student_class": "BSc Computer Science - 3rd Year",
    "stream": "Science",
    "year": "2024",
    "department": "Computer Science"
}

# Make POST request
response = requests.post(
    'http://127.0.0.1:8000/api/users/update-student-details/',
    headers={'Content-Type': 'application/json'},
    data=json.dumps(student_data)
)

print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
