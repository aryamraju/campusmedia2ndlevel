# Staff Details Page Documentation

## Overview
The Staff Details Page is a first-time login screen that collects professional information from staff members when they log in for the first time. This ensures that all staff profiles are complete with relevant professional details.

## Feature Description

### Purpose
- Collect professional details from staff members on their first login
- Store information locally using SharedPreferences
- Create a complete staff profile for campus administration

### Collected Information
1. **Qualification**: Educational qualifications (e.g., M.Sc Physics, B.Ed, Ph.D)
2. **Subject Expertise**: Areas of teaching expertise (e.g., Mathematics, Physics, Chemistry)
3. **Assigned Classes**: Classes currently teaching (e.g., 10th Grade Math, BSc Physics)
4. **Years of Experience**: Total years of teaching experience

## Implementation Details

### Backend Changes

#### Database Schema (users/models.py)
Added 4 new fields to the User model:
```python
# Staff-specific fields
qualification = models.CharField(max_length=200, blank=True, null=True)
subject_expertise = models.CharField(max_length=200, blank=True, null=True)
assigned_classes = models.TextField(blank=True, null=True)
experience_years = models.IntegerField(blank=True, null=True)
```

#### Migration
- **Migration File**: `0007_user_assigned_classes_user_experience_years_and_more.py`
- **Status**: Successfully applied to MySQL database
- **Command Used**: 
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

### Frontend Implementation

#### File Structure
```
campusmedia_frontend/lib/pages/
├── staff_details_page.dart   (New file)
├── login_page.dart            (Updated with routing logic)
└── staff_home_page.dart       (Target destination)
```

#### Staff Details Page (staff_details_page.dart)
- **Widget Type**: StatefulWidget
- **Dependencies**: 
  - `shared_preferences` for local storage
  - `staff_home_page.dart` for navigation

**Key Features:**
- Modern UI with gradient app bar (green theme)
- Profile header showing staff name and register number
- Form with 4 text fields for professional information
- Input validation for all fields
- "Save & Continue" button to save and navigate
- "Skip for now" option to proceed without filling details

**Props:**
- `userdata`: Map containing user information from login
- `userId`: Integer ID of the logged-in staff member

#### Login Flow Update (login_page.dart)
Added staff details check similar to students:

```dart
if (role == 'Staff') {
  // Check if staff has filled details
  final hasDetails = await prefs.getString('staff_qualification');
  
  if (hasDetails == null || hasDetails.isEmpty) {
    // First time login - go to details page
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (context) => StaffDetailsPage(
          userdata: {...},
          userId: user.id,
        ),
      ),
    );
  } else {
    // Details already filled - go to home
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(
        builder: (context) => StaffHomePage(userId: user.id),
      ),
    );
  }
}
```

#### Route Configuration (main.dart)
Added new route:
```dart
'/staff-details': (context) => const StaffDetailsPage(),
```

## User Flow

### First-Time Staff Login
1. Staff member enters credentials on Login Page
2. Backend validates email/password/role
3. App checks SharedPreferences for `staff_qualification` key
4. If not found → Navigate to **StaffDetailsPage**
5. Staff fills in professional information
6. Clicks "Save & Continue"
7. Data saved to SharedPreferences
8. Navigate to **StaffHomePage**

### Subsequent Logins
1. Staff member enters credentials
2. Backend validates credentials
3. App finds existing `staff_qualification` in SharedPreferences
4. Directly navigate to **StaffHomePage** (skip details page)

## Data Storage

### SharedPreferences Keys
- `staff_qualification`: Educational qualifications
- `staff_subject`: Subject expertise
- `staff_classes`: Assigned classes
- `staff_experience`: Years of experience

### Storage Location
Data is stored locally on the device using Flutter's `shared_preferences` plugin. This persists across app sessions.

## UI/UX Design

### Color Scheme
- **Primary**: Green (#4CAF50)
- **Secondary**: Dark Green (#2E7D32)
- **Background**: Light Gray (#F5F6FA)
- **Text**: Dark Gray (#2D3142)

### Components
1. **Gradient App Bar**: Green gradient with "Staff Details" title
2. **Profile Header Card**: 
   - Staff icon with gradient background
   - Staff name and register number
   - "Staff" role badge
3. **Form Fields**:
   - Qualification (school icon)
   - Subject Expertise (book icon)
   - Assigned Classes (class icon, multi-line)
   - Years of Experience (work icon, numeric)
4. **Action Buttons**:
   - Green "Save & Continue" button
   - "Skip for now" text button

## Testing

### Test Staff Account
Created via `create_staff.py`:
- **Email**: staff@gmail.com
- **Password**: staff@123
- **Role**: Staff
- **Name**: Test Staff
- **Register Number**: STAFF001

### Manual Testing Steps
1. Start Django backend: `python manage.py runserver`
2. Launch Flutter app
3. Navigate to Login Page
4. Enter staff credentials:
   - Email: staff@gmail.com
   - Password: staff@123
   - Role: Staff
5. Click "Sign In"
6. Verify navigation to Staff Details Page
7. Fill in all fields:
   - Qualification: "M.Sc Physics, B.Ed"
   - Subject Expertise: "Physics, Mathematics"
   - Assigned Classes: "10th Grade Physics\n12th Grade Advanced Math"
   - Years of Experience: "8"
8. Click "Save & Continue"
9. Verify success message
10. Verify navigation to Staff Home Page
11. Log out and log back in
12. Verify direct navigation to Staff Home (details page skipped)

### Edge Cases
- **Empty Fields**: Validation prevents submission
- **Skip Option**: Allows proceeding without filling details
- **Subsequent Logins**: Checks for existing data to skip form

## Future Enhancements

### Backend API Integration
Currently, staff details are only stored locally. Future enhancement:
1. Create API endpoint: `POST /api/users/update-staff-details`
2. Send staff details to backend on save
3. Store in MySQL database User model fields
4. Retrieve and pre-fill on subsequent sessions

### Additional Fields
Consider adding:
- Department affiliation
- Office hours
- Contact preferences
- Profile photo upload
- Certifications and awards
- Research interests

### Admin Features
- Staff directory view for admin
- Filter staff by subject expertise
- View staff assignments
- Generate staff reports

## Files Modified/Created

### New Files
- `campusmedia_frontend/lib/pages/staff_details_page.dart`
- `campusmedia_backend/create_staff.py`

### Modified Files
- `campusmedia_frontend/lib/main.dart` (added route)
- `campusmedia_frontend/lib/pages/login_page.dart` (updated routing logic)
- `campusmedia_backend/users/models.py` (added staff fields)
- `TEST_CREDENTIALS.md` (updated with staff account info)

### Migration Files
- `0007_user_assigned_classes_user_experience_years_and_more.py`

## Related Documentation
- [Student Details Page Documentation](STUDENT_HOME_PAGE_DOCUMENTATION.md)
- [Backend Setup Guide](campusmedia_backend/BACKEND_SETUP_COMPLETE.md)
- [API Documentation](campusmedia_backend/API_DOCUMENTATION.md)
- [Test Credentials](TEST_CREDENTIALS.md)

## Summary
The Staff Details Page provides a seamless onboarding experience for staff members, collecting essential professional information on their first login. It integrates smoothly with the existing authentication flow and stores data locally for quick access on subsequent logins. The feature is fully implemented with a modern, user-friendly UI and proper validation.
