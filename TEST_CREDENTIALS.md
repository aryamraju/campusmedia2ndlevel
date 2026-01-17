# Test Credentials for CampusMedia App

## Backend Test Accounts (MySQL Database)

### Admin Account
- **Email:** admin@gmail.com
- **Password:** admin@123
- **Secret Key:** ADMIN2026
- **Role:** Admin

### Principal Account
- **Email:** principal@gmail.com
- **Password:** principal@123
- **Role:** Principal

### Staff Account
- **Email:** staff@gmail.com
- **Password:** staff@123
- **Role:** Staff
- **Name:** Test Staff
- **Register Number:** STAFF001

### Student Account
- **Email:** student@test.com
- **Password:** 123456
- **Role:** Student
- **Name:** John Student

## Features Implemented

### Authentication System
- Email/password/role-based login
- Password hashing using Django's make_password
- Session management with SharedPreferences

### Student Features
- First-time login details page (class, stream, year, department)
- Details saved to MySQL database via API
- View announcements from staff in Campus Feed
- Pull-to-refresh to reload announcements

### Staff Features
- First-time login details page (qualification, subject expertise, assigned classes, experience)
- Details saved to MySQL database via API
- Create announcements visible to all students
- Staff portal with announcement management
- Manage classes stored in database

### Announcement System
- Staff/Principal/Admin can create announcements
- Students can view active announcements
- Stored in MySQL database
- Real-time updates via API

### Database Integration
- Staff details (qualification, subject, classes, experience) stored in MySQL
- Student details (class, stream, year, department) stored in MySQL
- Persistent storage across sessions
- Hybrid storage: Database + SharedPreferences for offline access

## How to Use

1. Make sure MySQL is running: `net start MySQL80`
2. Start Django backend: `cd campusmedia_backend && python manage.py runserver`
3. Launch Flutter app
4. Login with any credentials above
5. First-time staff/student users will see details collection page

You can also register new users which will be saved to the MySQL database!
