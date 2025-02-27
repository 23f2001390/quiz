# Quiz Master

A multi-user quiz application built with Flask for Modern Application Development I (MAD I). This platform allows administrators to create and manage quizzes across different subjects and chapters, while users can attempt these quizzes and track their progress.

## Features

### User Features
- User registration and authentication
- Subject and chapter-based quiz organization
- Timed quiz attempts with auto-submission
- Visual timer with color warning in last 5 minutes
- Detailed score tracking and performance analytics
- Subject-wise and month-wise performance visualization
- Search functionality for subjects and quizzes
- View attempted quiz details with correct answers
- Performance dashboard with:
  - Total quizzes attempted
  - Average score
  - Highest score
  - Subject-wise quiz distribution
  - Monthly attempt trends

### Admin Features
- Create and manage subjects
- Add chapters to subjects
- Create timed quizzes with multiple-choice questions
- Set quiz date and duration
- View all users and their performance
- Search across users, subjects, and quizzes
- Analytics dashboard with:
  - Subject-wise top scores
  - User participation visualization
  - Total users, quizzes, and attempts tracking

## Tech Stack
- Backend: Flask 3.0.2
- Frontend: HTML, CSS, Bootstrap 3.3.7
- Database: SQLite with SQLAlchemy
- Authentication: Flask-Login
- Forms: Flask-WTF
- Charts: Chart.js (Python-configured)

## Project Structure
```
quiz_master/
├── app.py                  # Application entry point
├── init_db.py             # Database initialization
├── requirements.txt       # Project dependencies
├── quiz_utils.py          # Quiz timer utilities
│
├── /controllers          # Route handlers and business logic
│   ├── __init__.py
│   ├── admin.py         # Admin routes and quiz management
│   ├── auth.py          # Authentication and user management
│   ├── user.py          # User routes and quiz attempts
│   └── api.py           # API endpoints for dynamic updates
│
├── /models              # Database models and utilities
│   ├── __init__.py     # Database initialization
│   ├── user.py         # User model and authentication
│   ├── quiz.py         # Quiz, Subject, Chapter models
│   ├── score.py        # Score tracking model
│   └── chart_data.py   # Chart configurations and data processing
│
├── /forms              # Form definitions
│   ├── __init__.py
│   ├── admin.py       # Admin forms (quiz/subject management)
│   ├── auth.py        # Authentication forms
│   ├── quiz.py        # Quiz attempt forms
│   └── user.py        # User search forms
│
├── /templates         # Jinja2 HTML templates
│   ├── base.html     # Base template with common layout
│   │
│   ├── /admin        # Admin interface templates
│   │   ├── dashboard.html    # Admin main page
│   │   ├── statistics.html   # Analytics dashboard
│   │   ├── users.html        # User management
│   │   ├── subject_form.html # Subject creation/editing
│   │   ├── chapter_form.html # Chapter management
│   │   ├── quiz_form.html    # Quiz creation/editing
│   │   ├── question_form.html # Question management
│   │   ├── view_quiz.html    # Quiz details view
│   │   └── search.html       # Admin search interface
│   │
│   ├── /auth         # Authentication templates
│   │   ├── login.html
│   │   └── register.html
│   │
│   └── /user         # User interface templates
│       ├── dashboard.html       # User homepage
│       ├── scores.html          # Performance tracking
│       ├── attempt_quiz.html    # Quiz taking interface
│       ├── quiz_result.html     # Quiz results
│       ├── view_quiz_attempt.html # Review attempts
│       ├── view_quiz.html       # Quiz details
│       └── search.html          # User search interface
│
└── /static           # Static assets
    └── /css
        └── style.css # Custom styles
```

## Setup Instructions

1. (Optional)Create a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   python init_db.py
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the application:
   - Open your browser and go to `http://localhost:5000`
   - For admin access, use:
     - Email: admin@quizmaster.com
     - Password: admin123

# If the above shows any error use:

1. ```bash
   uv venv
   ```
2. ```bash
   uv pip install -r requirements.txt
   ```
3. ```bash
   uv run init_db.py
   ```
4. ```bash
   uv run app.py
   ```
5. Access the application:
   - Open your browser and go to `http://localhost:5000`
   - For admin access, use:
     - Email: admin@quizmaster.com
     - Password: admin123
    
## Usage Guide

### For Administrators
1. Log in with admin credentials
2. Create subjects from the admin dashboard
3. Add chapters to subjects
4. Create quizzes within chapters
5. Add multiple-choice questions to quizzes
6. Set quiz date and duration
7. View user performance and analytics

### For Users
1. Register a new account
2. Browse available subjects and chapters
3. View upcoming quizzes
4. Start a quiz when ready
5. Submit answers within the time limit
6. View results and correct answers
7. Track performance in the dashboard

## Key Components

### Models
- User: User authentication and profile
- Subject/Chapter: Course organization
- Quiz/Question: Quiz content and settings
- Score: Attempt tracking and performance

### Controllers
- Admin: Quiz management endpoints
- Auth: Login/registration handling
- User: Quiz attempt processing
- API: JSON endpoints for dynamic updates

### Features
- Timed quiz attempts with auto-submission
- Real-time timer with visual warnings
- Performance analytics and visualizations
- Search functionality
- User attempt tracking
- Detailed score analysis 
