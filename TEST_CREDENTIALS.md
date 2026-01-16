# Test Credentials for CampusMedia App

## Pre-seeded Test Accounts

The app now comes with pre-seeded test accounts that you can use to login immediately:

### Student Account
- **Email:** student@test.com
- **Password:** 123456
- **Role:** Student
- **Name:** John Student

### Staff Account
- **Email:** staff@test.com
- **Password:** 123456
- **Role:** Staff
- **Name:** Jane Staff

### Principal Account (Hardcoded)
- **Email:** principal@gmail.com
- **Password:** principal@123
- **Role:** Principal

## What Was Fixed

1. **Persistent Storage**: Added `shared_preferences` package to store user data permanently
2. **Pre-seeded Users**: Automatically creates test users on first launch
3. **Async Operations**: Updated all UserService methods to work asynchronously
4. **Login Fix**: The login page now properly validates against stored users

## How to Use

1. Launch the app
2. Navigate to the Login page
3. Enter any of the test credentials above
4. Select the matching role from the dropdown
5. Click "Sign In"

You can also register new users which will be saved permanently!
