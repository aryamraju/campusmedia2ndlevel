import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusmedia_backend.settings')
django.setup()

from users.models import User

# Update existing users who have filled details
print("=" * 60)
print("Updating profile_completed flag for existing users")
print("=" * 60)

updated_count = 0

# Update students who have filled their details
students = User.objects.filter(role='Student')
for student in students:
    # If student has filled class details, mark profile as completed
    if student.student_class and student.student_class.strip():
        if not student.profile_completed:
            student.profile_completed = True
            student.save()
            print(f"✅ Updated {student.first_name} {student.last_name} (Student) - profile_completed = True")
            updated_count += 1
    else:
        print(f"⚠️  {student.first_name} {student.last_name} (Student) - No details filled yet")

# Update staff who have filled their details
staff = User.objects.filter(role__in=['Staff', 'Principal'])
for staff_member in staff:
    # If staff has filled qualification details, mark profile as completed
    if staff_member.qualification and staff_member.qualification.strip():
        if not staff_member.profile_completed:
            staff_member.profile_completed = True
            staff_member.save()
            print(f"✅ Updated {staff_member.first_name} {staff_member.last_name} ({staff_member.role}) - profile_completed = True")
            updated_count += 1
    else:
        print(f"⚠️  {staff_member.first_name} {staff_member.last_name} ({staff_member.role}) - No details filled yet")

print("\n" + "=" * 60)
print(f"✅ Update complete! {updated_count} user(s) updated.")
print("=" * 60)

# Show current profile completion status
print("\nCurrent profile completion status:")
print("-" * 60)
all_users = User.objects.all().order_by('role', 'first_name')
for user in all_users:
    status = "✅ Completed" if user.profile_completed else "⏳ Pending"
    print(f"{user.first_name} {user.last_name} ({user.role}): {status}")
