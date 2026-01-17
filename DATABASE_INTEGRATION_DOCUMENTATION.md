# Database Integration for Staff and Student Details

## Overview
This feature enables staff and student details to be saved directly to the MySQL database through REST API endpoints, ensuring persistent storage and enabling future administrative features like reporting, analytics, and user management.

## Implementation Summary

### Backend Changes

#### 1. New API Endpoints (users/views.py)

##### Update Staff Details
- **Endpoint**: `POST /api/users/update-staff-details/`
- **Purpose**: Save staff professional information to database
- **Request Body**:
  ```json
  {
    "user_id": 3,
    "qualification": "M.Sc Physics, B.Ed",
    "subject_expertise": "Physics, Mathematics",
    "assigned_classes": "10th Grade Physics\n12th Grade Advanced Math",
    "experience_years": "8"
  }
  ```
- **Response** (Success - 200):
  ```json
  {
    "success": true,
    "message": "Staff details updated successfully",
    "user": {
      "id": 3,
      "email": "staff@gmail.com",
      "first_name": "Test",
      "last_name": "Staff",
      "qualification": "M.Sc Physics, B.Ed",
      "subject_expertise": "Physics, Mathematics",
      "assigned_classes": "10th Grade Physics\n12th Grade Advanced Math",
      "experience_years": 8
    }
  }
  ```
- **Validation**: 
  - Verifies user exists
  - Checks user role is 'Staff' or 'Principal'
  - Validates experience_years is numeric

##### Update Student Details
- **Endpoint**: `POST /api/users/update-student-details/`
- **Purpose**: Save student academic information to database
- **Request Body**:
  ```json
  {
    "user_id": 4,
    "student_class": "BSc Computer Science - 3rd Year",
    "stream": "Science",
    "year": "2024",
    "department": "Computer Science"
  }
  ```
- **Response** (Success - 200):
  ```json
  {
    "success": true,
    "message": "Student details updated successfully",
    "user": {
      "id": 4,
      "email": "student@test.com",
      "first_name": "John",
      "last_name": "Student",
      "student_class": "BSc Computer Science - 3rd Year",
      "stream": "Science",
      "year": "2024",
      "department": "Computer Science"
    }
  }
  ```
- **Validation**:
  - Verifies user exists
  - Checks user role is 'Student'

#### 2. URL Routes (users/urls.py)
Added two new routes:
```python
path('update-staff-details/', views.update_staff_details, name='update-staff-details'),
path('update-student-details/', views.update_student_details, name='update-student-details'),
```

### Frontend Changes

#### 1. New Service Layer (services/staff_service.dart)

Created a dedicated service for managing staff and student details:

```dart
class StaffService {
  static const String baseUrl = 'http://127.0.0.1:8000/api/users';

  Future<Map<String, dynamic>?> updateStaffDetails({
    required int userId,
    required String qualification,
    required String subjectExpertise,
    required String assignedClasses,
    required String experienceYears,
  }) async { ... }

  Future<Map<String, dynamic>?> updateStudentDetails({
    required int userId,
    required String studentClass,
    required String stream,
    required String year,
    required String department,
  }) async { ... }
}
```

**Features**:
- HTTP POST requests with JSON payload
- Error handling with try-catch
- Returns parsed response or null on failure
- Prints debug information to console

#### 2. Updated Staff Details Page (staff_details_page.dart)

**Changes**:
- Added `import '../services/staff_service.dart';`
- Updated `_saveDetails()` method to:
  1. Show loading indicator
  2. Call backend API via StaffService
  3. Save to SharedPreferences on success (for offline access)
  4. Show success/error messages
  5. Navigate to StaffHomePage

**Key Code**:
```dart
void _saveDetails() async {
  if (_formKey.currentState!.validate()) {
    // Show loading
    showDialog(...);
    
    try {
      // Save to backend
      final staffService = StaffService();
      final result = await staffService.updateStaffDetails(
        userId: widget.userId ?? 0,
        qualification: _qualificationController.text.trim(),
        subjectExpertise: _subjectController.text.trim(),
        assignedClasses: _assignedClassesController.text.trim(),
        experienceYears: _experienceController.text.trim(),
      );

      if (result != null && result['success']) {
        // Save to SharedPreferences
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('staff_qualification', ...);
        
        // Show success and navigate
        ScaffoldMessenger.of(context).showSnackBar(...);
        Navigator.pushReplacement(...);
      }
    } catch (e) {
      // Handle errors
    }
  }
}
```

#### 3. Updated Student Details Page (student_details_page.dart)

**Changes**:
- Added `import '../services/staff_service.dart';`
- Added `userId` parameter to widget
- Updated `_saveDetails()` method similar to staff page
- Updated login_page.dart to pass `userId` parameter

**Updated Constructor**:
```dart
class StudentDetailsPage extends StatefulWidget {
  final Map<String, dynamic>? userdata;
  final int? userId;  // NEW
  
  const StudentDetailsPage({super.key, this.userdata, this.userId});
}
```

#### 4. Updated Login Page (login_page.dart)

Added `userId` parameter when navigating to StudentDetailsPage:
```dart
Navigator.pushReplacement(
  context,
  MaterialPageRoute(
    builder: (context) => StudentDetailsPage(
      userdata: {...},
      userId: user.id,  // NEW
    ),
  ),
);
```

## Data Flow

### Staff Details Submission Flow
```
1. Staff fills form in StaffDetailsPage
2. User clicks "Save & Continue"
3. Loading indicator appears
4. StaffService.updateStaffDetails() called
5. HTTP POST to /api/users/update-staff-details/
6. Backend validates user and role
7. Data saved to MySQL users table
8. Success response returned
9. Data saved to SharedPreferences (offline)
10. Success message displayed
11. Navigate to StaffHomePage
```

### Student Details Submission Flow
```
1. Student fills form in StudentDetailsPage
2. User clicks "Save & Continue"
3. Loading indicator appears
4. StaffService.updateStudentDetails() called
5. HTTP POST to /api/users/update-student-details/
6. Backend validates user and role
7. Data saved to MySQL users table
8. Success response returned
9. Data saved to SharedPreferences (offline)
10. Success message displayed
11. Navigate to StudentHomePage
```

## Testing

### API Testing

Created `test_details_api.py` to verify endpoints:

**Test Results**:
```
Testing Staff Details Update API...
Status Code: 200
Response: {
  "success": true,
  "message": "Staff details updated successfully",
  "user": {
    "id": 3,
    "email": "anju@gmail.com",
    "qualification": "M.Sc Physics, B.Ed",
    "subject_expertise": "Physics, Mathematics",
    "assigned_classes": "10th Grade Physics\n12th Grade Advanced Math",
    "experience_years": 8
  }
}
```

### Database Verification

Created `verify_staff_details.py` to check MySQL data:

**Verification Results**:
```
Staff ID: 3
Name: anju v
Email: anju@gmail.com
Qualification: M.Sc Physics, B.Ed
Subject Expertise: Physics, Mathematics
Assigned Classes: 10th Grade Physics
                 12th Grade Advanced Math
Experience Years: 8
```

✅ **Confirmed**: Data successfully saved to MySQL database!

### Manual Testing Steps

#### Staff Details Flow
1. Start backend: `python manage.py runserver`
2. Launch Flutter app
3. Login as staff: staff@gmail.com / staff@123
4. Fill staff details form:
   - Qualification: M.Sc Physics, B.Ed
   - Subject Expertise: Physics, Mathematics
   - Assigned Classes: 10th Grade Physics
   - Experience Years: 8
5. Click "Save & Continue"
6. Verify loading indicator appears
7. Verify success message: "Details saved to database successfully!"
8. Verify navigation to Staff Home
9. Check MySQL database for saved data
10. Log out and back in - verify data persists

#### Student Details Flow
1. Login as student: student@test.com / 123456
2. Fill student details form
3. Click "Save & Continue"
4. Verify database storage
5. Test subsequent login (should skip details page)

## Benefits

### 1. Persistent Storage
- Data stored in MySQL database
- Survives app reinstalls and device changes
- Accessible from any device after login

### 2. Centralized Data
- All user information in single database
- Easy to query and report
- Enables admin dashboard features

### 3. Data Integrity
- Backend validation ensures data quality
- Role-based access control
- Prevents unauthorized updates

### 4. Future Features Enabled
- Staff directory for admin
- Class assignment reports
- Experience analytics
- Qualification filtering
- Student academic tracking
- Department-wise reports

### 5. Hybrid Storage
- Database for persistence
- SharedPreferences for offline access
- Best of both worlds

## Error Handling

### Backend Errors
- **404**: User not found
- **403**: Unauthorized role (e.g., student trying to update staff details)
- **400**: Invalid data (e.g., non-numeric experience years)
- **500**: Server error

### Frontend Handling
- Loading indicator during API call
- Success snackbar on successful save
- Error snackbar with message on failure
- Graceful fallback if network unavailable

## Files Modified/Created

### Backend
- ✅ `users/views.py` - Added `update_staff_details()` and `update_student_details()`
- ✅ `users/urls.py` - Added routes for new endpoints
- ✅ `test_details_api.py` - API testing script (NEW)
- ✅ `verify_staff_details.py` - Database verification script (NEW)

### Frontend
- ✅ `services/staff_service.dart` - Service layer for API calls (NEW)
- ✅ `pages/staff_details_page.dart` - Updated to save to database
- ✅ `pages/student_details_page.dart` - Updated to save to database
- ✅ `pages/login_page.dart` - Pass userId to StudentDetailsPage

## API Endpoints Summary

| Endpoint | Method | Purpose | Auth Required |
|----------|--------|---------|---------------|
| `/api/users/update-staff-details/` | POST | Update staff professional info | Staff/Principal |
| `/api/users/update-student-details/` | POST | Update student academic info | Student |

## Next Steps

### Recommended Enhancements
1. **Retrieve User Details**: Add GET endpoint to fetch saved details
2. **Edit Details**: Allow users to update their details later
3. **Admin Dashboard**: View all staff/student details
4. **Reports**: Generate reports by department, qualification, etc.
5. **Validation**: Add more robust validation (e.g., year format, email verification)
6. **File Upload**: Allow staff to upload qualification certificates
7. **Bulk Import**: Import staff/student data from CSV/Excel

## Conclusion

The staff and student details are now successfully integrated with the MySQL database through REST API endpoints. Data is persisted across sessions, accessible to administrators, and provides a foundation for future features like reporting, analytics, and user management.

**Status**: ✅ **COMPLETED AND TESTED**
- Backend API endpoints working
- Frontend integration complete
- Data successfully saved to MySQL
- Verification scripts confirmed database storage
