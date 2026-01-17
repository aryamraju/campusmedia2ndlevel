import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusmedia_backend.settings')
django.setup()

from users.models import User
from django.db import connection

print("=" * 80)
print("DATABASE STORAGE LOCATION")
print("=" * 80)

# Show database connection info
print(f"\nDatabase Engine: MySQL")
print(f"Database Name: campusmedia_db")
print(f"Host: localhost")
print(f"Table Name: users_user")

# Show the staff-specific columns
print("\n" + "=" * 80)
print("STAFF-SPECIFIC COLUMNS IN users_user TABLE")
print("=" * 80)

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'campusmedia_db' 
        AND TABLE_NAME = 'users_user'
        AND COLUMN_NAME IN ('qualification', 'subject_expertise', 'assigned_classes', 'experience_years')
        ORDER BY ORDINAL_POSITION
    """)
    
    columns = cursor.fetchall()
    print(f"\n{'Column Name':<25} {'Data Type':<15} {'Nullable':<10} {'Details':<30}")
    print("-" * 80)
    for col in columns:
        print(f"{col[0]:<25} {col[1]:<15} {col[2]:<10} {col[3]:<30}")

# Show actual stored data
print("\n" + "=" * 80)
print("ACTUAL STAFF DATA IN DATABASE")
print("=" * 80)

staff_users = User.objects.filter(role='Staff')

for staff in staff_users:
    print(f"\n{'='*80}")
    print(f"Staff ID: {staff.id}")
    print(f"Name: {staff.first_name} {staff.last_name}")
    print(f"Email: {staff.email}")
    print(f"Register Number: {staff.register_number}")
    print(f"\nPROFESSIONAL DETAILS (Stored in MySQL):")
    print(f"  • Qualification: {staff.qualification}")
    print(f"  • Subject Expertise: {staff.subject_expertise}")
    print(f"  • Assigned Classes: {staff.assigned_classes}")
    print(f"  • Experience Years: {staff.experience_years}")

print(f"\n{'='*80}")
print(f"Total Staff Records: {staff_users.count()}")
print("=" * 80)

# Show the exact SQL query to access this data
print("\n" + "=" * 80)
print("SQL QUERY TO ACCESS STAFF DETAILS")
print("=" * 80)
print("""
SELECT 
    id,
    email,
    first_name,
    last_name,
    register_number,
    qualification,
    subject_expertise,
    assigned_classes,
    experience_years
FROM users_user
WHERE role = 'Staff';
""")

print("\n" + "=" * 80)
print("STORAGE SUMMARY")
print("=" * 80)
print("""
✓ Primary Storage: MySQL Database (campusmedia_db.users_user table)
✓ Secondary Storage: SharedPreferences (for offline access on device)
✓ Backend API: http://127.0.0.1:8000/api/users/update-staff-details/
✓ Data Persistence: Permanent in MySQL
✓ Accessible by: Backend queries, API endpoints, Django admin
""")
