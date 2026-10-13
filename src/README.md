# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Publicly view activities and participant lists
- Teacher-only signup and unregister actions

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| GET    | `/auth/session`                                                   | Verify teacher credentials                                          |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Teacher registers a student for an activity                         |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Teacher unregisters a student                                    |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.

## Teacher accounts

Copy `src/teachers.example.json` to `src/teachers.json` and add teacher accounts:

```json
{
   "teachers": [
      { "username": "teacher", "password": "choose-a-password" }
   ]
}
```

`src/teachers.json` is excluded from Git. Keep it private, use a strong password, and serve the application over HTTPS outside local development. Teacher login lasts only in the current browser page; signing out or reloading clears it.
