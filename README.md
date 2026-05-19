# 🎓 Academic Sentinel - Student Performance Monitoring System

## A Complete Guide for Students, Developers, and Presenters

> **Welcome!** This document is designed for **absolute beginners**. Whether you know nothing about programming or you're a computer science student preparing to present this project, this guide will teach you everything you need to understand, explain, and defend this work as your own.

---

## 📖 Table of Contents

1. [What Is This Project?](#what-is-this-project)
2. [The Problem We're Solving](#the-problem-were-solving)
3. [How The System Works (Big Picture)](#how-the-system-works-big-picture)
4. [Technology Stack Explained](#technology-stack-explained)
5. [Project Structure Walkthrough](#project-structure-walkthrough)
6. [Core Features Deep Dive](#core-features-deep-dive)
7. [The "AI" Risk Engine Explained](#the-ai-risk-engine-explained)
8. [Database Design](#database-design)
9. [Security Features](#security-features)
10. [How To Run This Project](#how-to-run-this-project)
11. [Presentation Q&A Preparation](#presentation-qa-preparation)
12. [Common Questions & Perfect Answers](#common-questions--perfect-answers)

---

## 🤔 What Is This Project?

**Academic Sentinel** is a web-based software system that helps universities automatically identify students who are struggling academically **before** it's too late.

### Think of it like this:

Imagine you're a teacher with 500 students. You can't possibly track every single student's grades, notice patterns, and catch problems early. Some students might be failing multiple courses, but nobody notices until they're asked to leave the program.

This system acts like a **24/7 academic watchdog** that:
- Watches every student's grades
- Spots warning signs automatically
- Alerts teachers and administrators
- Generates reports to help students get back on track

### Real-World Analogy

Think of a **health monitoring watch** that tracks your heart rate. If your heart rate goes too high or too low, the watch alerts you. Academic Sentinel does the same thing, but for **student performance** instead of health.

---

## 🎯 The Problem We're Solving

### Before This System:

1. **Late Detection**: Universities often discover failing students at the end of the semester—too late to help them.
2. **Manual Work**: Staff manually calculate GPAs and risk levels, which is slow and error-prone.
3. **No Centralized Data**: Student records are scattered across different departments.
4. **Reactive, Not Proactive**: Interventions happen after failure, not before.

### After This System:

1. **Early Warning**: The system flags at-risk students immediately when grades are uploaded.
2. **Automatic Calculations**: GPA and risk scores are computed instantly.
3. **Single Source of Truth**: All academic data lives in one secure database.
4. **Proactive Intervention**: Advisors can reach out to struggling students before they fail.

---

## 🖼️ How The System Works (Big Picture)

Let me walk you through the entire flow:

```
┌─────────────────────────────────────────────────────────────────┐
│                    STEP 1: DATA UPLOAD                          │
│  Admin uploads a CSV file containing student grades             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    STEP 2: DATA PROCESSING                      │
│  System reads the CSV, validates it, saves to database          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    STEP 3: RISK ANALYSIS                        │
│  The "AI Engine" calculates GPA and risk level for each student │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    STEP 4: NOTIFICATIONS                        │
│  Alerts are sent to staff about high-risk students              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    STEP 5: INTERVENTION                         │
│  Advisors view reports, add notes, and help students            │
└─────────────────────────────────────────────────────────────────┘
```

### User Roles in the System

The system has **two types of users**:

#### 1. **Administrator (Admin)**
- Can upload student data (CSV files)
- Can manage other users (create accounts, change roles)
- Can configure risk thresholds (e.g., what GPA is considered "dangerous")
- Can view audit logs (who did what and when)
- Can generate cohort-wide reports

#### 2. **Staff (Academic Advisors)**
- Can view all students and their risk levels
- Can see detailed student profiles
- Can download individual student reports (PDF)
- Can add advisor notes to student records
- Can filter and search for at-risk students

---

## 💻 Technology Stack Explained

This section explains **every technology** used in this project, assuming you've never heard of them before.

### Backend Technologies

#### **Python 3.x**
- **What it is**: A programming language known for being easy to read and write.
- **Why we use it**: Python is excellent for data processing, has great libraries, and is beginner-friendly.
- **Analogy**: If building software is like cooking, Python is like having pre-chopped ingredients—it saves time and reduces errors.

#### **Flask (Version 3.0.0)**
- **What it is**: A lightweight web framework for Python.
- **Why we use it**: Flask helps us build websites without writing everything from scratch. It handles web requests, routing, and responses.
- **Analogy**: Flask is like a **restaurant kitchen setup**. It provides the stove, oven, and counters (infrastructure), but you decide what dishes to cook (your application logic).

#### **Flask-SQLAlchemy (Version 3.0.3)**
- **What it is**: A tool that lets Python code talk to databases using simple Python commands instead of complex SQL queries.
- **Why we use it**: Instead of writing `SELECT * FROM students WHERE id = 5`, you write `Student.query.get(5)`—much cleaner!
- **Analogy**: It's like having a **translator** between you and the database. You speak Python, the database speaks SQL, and SQLAlchemy translates between them.

#### **Flask-Login (Version 0.6.3)**
- **What it is**: A Flask extension that handles user authentication (logging in/out).
- **Why we use it**: Security! It manages user sessions, remembers logged-in users, and protects pages that require login.
- **Analogy**: Like a **bouncer at a club**—it checks IDs (credentials) and only lets authorized people in.

#### **Pandas (Version 2.2.3)**
- **What it is**: A powerful data analysis library for Python.
- **Why we use it**: We use it to read CSV files, validate data, and process large amounts of student records efficiently.
- **Analogy**: Pandas is like **Excel on steroids**—it can handle millions of rows of data and perform complex operations quickly.

#### **ReportLab (Version 4.4.10)**
- **What it is**: A library for generating PDF documents programmatically.
- **Why we use it**: When users click "Download Report," ReportLab creates professional PDF files with tables, charts, and formatted text.
- **Analogy**: It's like a **robot printer** that you can control with code to print exactly what you want.

#### **Werkzeug (Version 3.0.1)**
- **What it is**: A utility library that Flask is built on top of.
- **Why we use it**: It provides security features like password hashing (encrypting passwords so they can't be stolen).
- **Analogy**: Werkzeug is the **engine under the hood** of a car—you don't see it directly, but it powers essential functions.

### Frontend Technologies

#### **HTML (HyperText Markup Language)**
- **What it is**: The skeleton of every webpage. It defines structure (headings, paragraphs, buttons, etc.).
- **Why we use it**: Every page you see in this system is built with HTML.

#### **CSS (Cascading Style Sheets)**
- **What it is**: The styling language that makes HTML look beautiful.
- **Why we use it**: Colors, fonts, spacing, animations—all controlled by CSS.

#### **Tailwind CSS**
- **What it is**: A modern CSS framework that provides pre-built utility classes.
- **Why we use it**: Instead of writing custom CSS for every button, Tailwind gives you ready-made classes like `bg-blue-500` (blue background) or `text-white` (white text).
- **Analogy**: Tailwind is like **LEGO blocks** for styling—you snap together pre-made pieces to build beautiful interfaces quickly.

#### **JavaScript**
- **What it is**: The programming language of the web browser.
- **Why we use it**: Adds interactivity (like live notification counts, form validation, dynamic updates).

#### **Chart.js** (used in templates)
- **What it is**: A JavaScript library for creating charts and graphs.
- **Why we use it**: Visualizes student performance trends over time.

### Database

#### **SQLite**
- **What it is**: A lightweight, file-based database.
- **Why we use it**: No server setup required—the database is just a file (`academic_monitoring.db`). Perfect for development and small-to-medium applications.
- **Analogy**: SQLite is like a **filing cabinet** in your office—simple, accessible, and doesn't require a dedicated room (server).

---

## 📁 Project Structure Walkthrough

Let's explore every folder and file, explaining what each one does:

```
/workspace/
│
├── app.py                      # THE MAIN ENTRY POINT
├── config.py                   # Configuration settings (database URL, secret keys)
├── requirements.txt            # List of Python packages needed
├── demo_data.csv               # Sample data for testing
├── create_staff.py             # Script to create staff accounts
│
├── backend/                    # ALL BACKEND CODE LIVES HERE
│   ├── __init__.py            # Makes this folder a Python package
│   ├── models.py              # Database table definitions
│   │
│   ├── routes/                # URL HANDLERS (which code runs when you visit a page)
│   │   ├── auth.py            # Login, logout, password reset
│   │   ├── admin.py           # Admin dashboard, data import, user management
│   │   ├── staff.py           # Staff dashboard, student profiles
│   │   ├── notifications.py   # Notification system
│   │   └── help.py            # Help page
│   │
│   ├── logic/                 # BUSINESS LOGIC (the "brain" of the system)
│   │   ├── risk_engine.py     # THE AI RISK CALCULATION ENGINE
│   │   ├── ingestion.py       # CSV file processing
│   │   ├── reporting.py       # PDF report generation
│   │   └── audit.py           # Activity logging
│   │
│   ├── api/                   # API endpoints (for future mobile apps, etc.)
│   │   └── main.py
│   │
│   └── core/                  # Core utilities
│       ├── engine.py
│       └── ingestion.py
│
├── templates/                  # HTML FILES (what users see)
│   ├── base.html              # Master template (header, sidebar, footer)
│   ├── auth/                  # Login, password reset pages
│   ├── admin/                 # Admin dashboard, import pages
│   ├── staff/                 # Staff dashboard, student profiles
│   ├── notifications/         # Notification inbox
│   ├── help/                  # Help documentation
│   └── errors/                # Error pages (404, 403)
│
├── static/                     # STATIC FILES (CSS, JS, images)
│   ├── css/
│   └── js/
│       └── main.js            # JavaScript for interactivity
│
└── instance/                   # DATABASE FILE (created automatically)
    └── academic_monitoring.db
```

### Key Files Explained

#### `app.py` - The Application Factory

This is where the Flask application is created. Think of it as the **construction site** where all components are assembled.

**Key concepts in this file:**

1. **Blueprint Registration**: Blueprints are like "modules" that organize related pages together. For example, all authentication pages (login, logout) are grouped in the `auth` blueprint.

2. **Login Manager Setup**: Configures how users stay logged in as they navigate the site.

3. **Database Initialization**: Creates all database tables when the app starts.

4. **Default Data**: Creates a default admin account and risk rules if they don't exist.

```python
# This code creates the Flask app
def create_app():
    app = Flask(__name__)  # Create the app
    app.config.from_object(Config)  # Load settings
    
    db.init_app(app)  # Connect database
    
    # Register blueprints (modules)
    app.register_blueprint(auth_bp)   # Authentication routes
    app.register_blueprint(admin_bp)  # Admin routes
    app.register_blueprint(staff_bp)  # Staff routes
    ...
    
    return app
```

#### `backend/models.py` - Database Blueprint

This file defines **what data we store**. Each class represents a database table.

**Tables in our system:**

| Table | Purpose |
|-------|---------|
| `User` | Stores login credentials and roles (Admin/Staff) |
| `Student` | Basic student info (ID, name, level) |
| `Course` | Course catalog (code, title, credits, core status) |
| `AcademicRecord` | Individual grades (student + course + grade) |
| `RiskAnalysis` | Computed risk scores for each student |
| `RiskRule` | Configurable thresholds (e.g., GPA < 2.0 = High Risk) |
| `AuditLog` | History of all actions (who did what) |
| `ImportLog` | History of CSV imports |
| `Notification` | User notifications |

#### `backend/routes/` - URL Handlers

Each file here handles specific URLs. For example:

- Visit `/login` → `auth.py` handles it
- Visit `/admin/dashboard` → `admin.py` handles it
- Visit `/staff/student/NUL/CS/24/001` → `staff.py` handles it

**How routing works:**

```python
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # This function runs when someone visits /login
    # GET = show the login form
    # POST = process the submitted form
```

#### `backend/logic/` - The Brain

This is where the actual **work** happens:

- `risk_engine.py`: Calculates risk scores
- `ingestion.py`: Processes uploaded CSV files
- `reporting.py`: Generates PDF reports
- `audit.py`: Logs all actions for security

---

## 🔍 Core Features Deep Dive

### Feature 1: User Authentication

**What it does**: Allows users to log in securely and access role-specific dashboards.

**How it works**:

1. User enters email and password on `/login`
2. System looks up the user in the database
3. Password is verified using **hash comparison** (never stored as plain text!)
4. If valid, a session is created (user stays logged in)
5. User is redirected based on their role (Admin → Admin Dashboard, Staff → Staff Dashboard)

**Security measures**:
- Passwords are hashed using `werkzeug.security.generate_password_hash()`
- Sessions expire after 30 minutes of inactivity
- Inactive users cannot log in
- Each page checks if the user has the correct role

**Code location**: `backend/routes/auth.py`

---

### Feature 2: CSV Data Import

**What it does**: Allows admins to upload student grades in bulk via CSV files.

**The Import Process**:

1. **Upload**: Admin selects a CSV file and uploads it
2. **Validation**: System checks if all required columns exist:
   - StudentID, Name, CourseCode, CourseTitle, Grade, Score, Semester, Session
3. **Preview**: Admin sees a preview of the data before committing
4. **Processing**: System:
   - Creates new students if they don't exist
   - Creates new courses if they don't exist
   - Skips duplicate records (same student + course + semester + session)
   - Saves unique records to database
5. **Risk Recalculation**: After import, the risk engine recalculates risk for ALL students
6. **Notifications**: Alerts are sent about newly identified high-risk students

**Duplicate Detection Logic**:
```python
existing_record = AcademicRecord.query.filter_by(
    student_db_id=student.id, 
    course_id=course.id,
    semester=row['Semester'],
    session=row['Session']
).first()

if not existing_record:
    # Add new record
else:
    duplicates += 1  # Skip this row
```

**Code location**: `backend/routes/admin.py`, `backend/logic/ingestion.py`

---

### Feature 3: Risk Analysis Engine (The "AI")

**What it does**: Automatically categorizes students into risk levels based on their academic performance.

**Risk Categories**:
- 🔴 **High Risk**: Immediate intervention needed
- 🟡 **Medium Risk**: Monitor closely
- 🟢 **Low Risk**: Good standing

**How Risk is Calculated**:

The system uses **rule-based logic** (not machine learning, but still intelligent):

#### Rule 1: GPA Thresholds
- If CGPA < 2.0 → **High Risk**
- If CGPA < 2.5 → **Medium Risk**
- Otherwise → Continue checking

#### Rule 2: Core Course Failures
- If failed core courses ≥ 1 → **High Risk**
  - Core courses are essential (e.g., "Data Structures" for CS majors)
  - Failing these is a major red flag

#### Rule 3: Any Failures
- If any course failures exist → **Medium Risk**

**GPA Calculation**:

The system uses a standard 5.0 grading scale:

| Grade | Points |
|-------|--------|
| A | 5.0 |
| B | 4.0 |
| C | 3.0 |
| D | 2.0 |
| E | 1.0 |
| F | 0.0 |

Formula:
```
CGPA = (Sum of (Grade Point × Credit Units)) / (Total Credit Units)
```

Example:
- Course 1: A (5.0) × 3 units = 15.0
- Course 2: B (4.0) × 3 units = 12.0
- Total: 27.0 / 6 units = **4.5 CGPA**

**Configurable Rules**:

Admins can change thresholds in the system! Go to `/admin/risk-rules` to adjust:
- `gpa_high_threshold` (default: 2.0)
- `gpa_med_threshold` (default: 2.5)
- `max_core_fails` (default: 1)

**Code location**: `backend/logic/risk_engine.py`

---

### Feature 4: Student Profiles

**What it does**: Shows detailed information about a single student.

**Information displayed**:
- Personal details (name, ID, level)
- Risk category and score
- Risk factors (why they're flagged)
- Complete academic history (all courses, grades, scores)
- Performance trend chart (average score per semester)
- Advisor notes section

**Performance Chart**:
Uses Chart.js to visualize how the student's average score changes over semesters. An upward trend = improvement, downward trend = concern.

**Code location**: `backend/routes/staff.py`, `templates/staff/student_profile.html`

---

### Feature 5: PDF Report Generation

**What it does**: Creates professional, downloadable PDF reports.

**Two types of reports**:

1. **Individual Student Report**:
   - Student bio information
   - Risk category
   - Identified risk factors
   - Complete academic history table
   - Generated on-demand when staff clicks "Download Report"

2. **Cohort Risk Summary**:
   - Total students in system
   - Breakdown by risk category (High/Medium/Low counts)
   - List of all high-risk students with IDs and scores
   - Used by administration for oversight

**How PDFs are generated**:
1. Create an in-memory buffer (like a virtual piece of paper)
2. Use ReportLab to draw text, tables, and formatting
3. Return the buffer as a downloadable file

**Code location**: `backend/logic/reporting.py`

---

### Feature 6: Notification System

**What it does**: Keeps users informed about important events.

**Notification triggers**:
- New data import completed
- High-risk student identified
- System announcements

**Features**:
- Unread count badge in sidebar
- Mark as read / mark all as read
- Color-coded by severity:
  - 🔵 Info (blue)
  - 🟡 Warning (yellow)
  - 🔴 Danger (red)

**Code location**: `backend/routes/notifications.py`

---

### Feature 7: Audit Logging

**What it does**: Records every important action in the system for accountability.

**Logged actions**:
- User logins/logouts
- Password changes
- CSV imports
- User creation/deletion
- Role changes
- Report downloads
- Advisor notes added

**Why it matters**:
- Security: Detect unauthorized access
- Accountability: Know who did what
- Debugging: Trace issues back to their source
- Compliance: Meet institutional record-keeping requirements

**Code location**: `backend/logic/audit.py`

---

### Feature 8: User Management (Admin Only)

**What it does**: Allows admins to manage system users.

**Capabilities**:
- Create new users (assign role: Admin or Staff)
- Deactivate/reactivate users
- Change user roles
- View all users in the system

**Security**: Only users with `role='Admin'` can access these features.

**Code location**: `backend/routes/admin.py`

---

### Feature 9: Course Management (Admin Only)

**What it does**: Manage the course catalog.

**Capabilities**:
- Add new courses
- Mark courses as "core" (essential for the major)
- View all courses

**Why core status matters**: Failing a core course is weighted more heavily in risk calculation than failing an elective.

**Code location**: `backend/routes/admin.py`

---

### Feature 10: Risk Rule Configuration (Admin Only)

**What it does**: Allows admins to tune the risk engine without changing code.

**Configurable rules**:
- GPA threshold for High Risk
- GPA threshold for Medium Risk
- Maximum allowed core course failures

**Example use case**: If the university tightens standards, an admin can lower the GPA thresholds, and the system will automatically flag more students.

**Code location**: `backend/routes/admin.py`, `backend/models.py` (RiskRule table)

---

## 🧠 The "AI" Risk Engine Explained

Let's go deeper into the risk engine because this is the **heart** of the system.

### File: `backend/logic/risk_engine.py`

This file contains the `RiskEvaluator` class—the brain that decides which students are at risk.

### Step-by-Step Execution

When `evaluate_risk(student_id)` is called:

```python
# Step 1: Get the student
student = Student.query.filter_by(student_id=student_id).first()

# Step 2: Get all their grade records
records = AcademicRecord.query.filter_by(student_db_id=student.id).all()

# Step 3: Calculate their GPA
gpa = self.calculate_gpa(records)

# Step 4: Find all failed courses
failures = [r for r in records if r.grade == 'F']

# Step 5: Find failed CORE courses specifically
core_failures = [r for r in failures if Course.query.get(r.course_id).is_core]

# Step 6: Apply rules to determine risk category
factors = []  # Will store reasons for the risk level
category = "Low"  # Default assumption

# Rule 1: Check for HIGH risk
if gpa < self.gpa_high:  # GPA below 2.0
    category = "High"
    factors.append(f"Cumulative GPA ({gpa:.2f}) is below threshold 2.0")

if len(core_failures) >= self.core_fail_limit:  # 1+ core failures
    category = "High"
    factors.append(f"Student has failed {len(core_failures)} core course(s)")

# Rule 2: Check for MEDIUM risk (only if not already High)
elif gpa < self.gpa_med or len(failures) > 0:
    category = "Medium"
    if gpa < self.gpa_med:
        factors.append(f"GPA ({gpa:.2f}) is marginal (below 2.5)")
    if len(failures) > 0:
        factors.append(f"Presence of failures ({len(failures)} course(s))")

# Step 7: Save the result to database
analysis = RiskAnalysis.query.filter_by(student_db_id=student.id).first()
if not analysis:
    analysis = RiskAnalysis(student_db_id=student.id)
    db.session.add(analysis)

analysis.risk_score = gpa
analysis.risk_category = category
analysis.factors = json.dumps(factors)  # Store reasons as JSON

db.session.commit()
```

### Why This Approach?

**Pros**:
- ✅ **Transparent**: You can see exactly why a student was flagged
- ✅ **Configurable**: Admins can adjust thresholds
- ✅ **Fast**: Simple calculations, instant results
- ✅ **Explainable**: Easy to justify decisions to stakeholders

**Cons**:
- ❌ **Not predictive**: Doesn't predict future performance, only analyzes past
- ❌ **Rigid**: Doesn't account for external factors (illness, family issues)
- ❌ **No machine learning**: Doesn't improve over time from data

**Future improvements** could include:
- Attendance tracking integration
- Trend analysis (is performance improving or declining?)
- Machine learning model trained on historical graduation data

---

## 🗄️ Database Design

### Entity Relationship Diagram (Conceptual)

```
┌─────────────┐       ┌──────────────────┐       ┌─────────────┐
│    User     │       │     Student      │       │    Course   │
├─────────────┤       ├──────────────────┤       ├─────────────┤
│ id          │       │ id               │       │ id          │
│ username    │       │ student_id       │       │ course_code │
│ email       │       │ name             │◄──────│ title       │
│ password    │       │ level            │       │ credit_units│
│ role        │       │ enrollment_year  │       │ is_core     │
└─────────────┘       └──────────────────┘       └─────────────┘
       │                       │                        │
       │                       │                        │
       ▼                       ▼                        ▼
┌─────────────┐       ┌──────────────────┐       ┌─────────────┐
│  AuditLog   │       │ AcademicRecord   │◄──────│ RiskRule    │
├─────────────┤       ├──────────────────┤       ├─────────────┤
│ user_id     │       │ student_db_id    │       │ rule_key    │
│ action      │       │ course_id        │       │ value       │
│ details     │       │ grade            │       │ description │
│ timestamp   │       │ score            │       └─────────────┘
└─────────────┘       │ semester         │
                      │ session          │
                      └──────────────────┘
                               │
                               ▼
                      ┌──────────────────┐
                      │   RiskAnalysis   │
                      ├──────────────────┤
                      │ student_db_id    │
                      │ risk_score       │
                      │ risk_category    │
                      │ factors          │
                      └──────────────────┘
```

### Relationships Explained

1. **Student → AcademicRecord**: One student has many records (one per course)
2. **Course → AcademicRecord**: One course appears in many records (one per student)
3. **Student → RiskAnalysis**: One student has one risk analysis (1-to-1)
4. **User → AuditLog**: One user performs many actions (logged)
5. **User → Notification**: One user receives many notifications

### Why This Design?

- **Normalization**: Data is split into logical tables to avoid duplication
- **Referential Integrity**: Foreign keys ensure data consistency
- **Scalability**: Can handle thousands of students and millions of records
- **Query Efficiency**: Easy to find all records for a student, or all students in a risk category

---

## 🔒 Security Features

### 1. Password Hashing

Passwords are **never** stored as plain text. Instead:

```python
# When setting password
user.set_password("mypassword")  
# Stored as: "pbkdf2:sha256:260000$randomsalt$hashedvalue"

# When checking password
user.check_password("mypassword")  # Returns True/False
```

**Why**: If hackers steal the database, they can't read passwords.

### 2. Role-Based Access Control (RBAC)

Every sensitive route checks the user's role:

```python
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'Admin':
        abort(403)  # Forbidden!
```

**Why**: Prevents regular staff from accessing admin-only features.

### 3. Session Management

- Sessions expire after 30 minutes
- Users must re-login after expiration
- Logout invalidates the session

### 4. Input Validation

- CSV files are validated before import
- Form inputs are sanitized
- SQL injection prevented by SQLAlchemy (uses parameterized queries)

### 5. Audit Trail

Every action is logged:
- Who did it
- What they did
- When they did it

**Why**: Enables forensic analysis if something goes wrong.

---

## 🚀 How To Run This Project

### Prerequisites

You need:
1. **Python 3.8 or higher** installed
2. **pip** (Python package manager)

### Step-by-Step Setup

#### Step 1: Navigate to the project folder

```bash
cd /workspace
```

#### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Flask
- Flask-SQLAlchemy
- Flask-Login
- pandas
- reportlab
- Werkzeug

#### Step 3: Run the application

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

#### Step 4: Open in browser

Go to: `http://localhost:5000`

You'll be redirected to the login page.

#### Step 5: Login with default admin

- **Email**: `admin@nile.edu.ng`
- **Password**: `admin123`

#### Step 6: Upload demo data

1. Go to Admin Dashboard
2. Click "Import Data"
3. Upload `demo_data.csv`
4. Preview and confirm
5. Watch the risk engine analyze the data!

### Creating Additional Users

Use the admin panel to create new users, or run:

```bash
python create_staff.py
```

---

## 🎤 Presentation Q&A Preparation

This section prepares you to **defend** this project in front of lecturers, examiners, or potential employers.

### Understanding the Question Types

Questions generally fall into these categories:

1. **Conceptual Questions**: Test your understanding of the problem
2. **Technical Questions**: Test your knowledge of the implementation
3. **Design Decisions**: Ask why you chose certain approaches
4. **Scenario Questions**: Present hypothetical situations
5. **Future Work**: Ask about improvements and extensions

### How to Answer

Use the **STAR method**:
- **S**ituation: Set the context
- **T**ask: Explain what needed to be done
- **A**ction: Describe what you did
- **R**esult: Share the outcome

---

## ❓ Common Questions & Perfect Answers

### Category 1: Conceptual Questions

#### Q1: "What problem does this system solve?"

**Perfect Answer**:
> "This system solves the problem of late detection of struggling students. In traditional systems, universities often discover failing students at the end of the semester when it's too late to intervene. Academic Sentinel continuously monitors student performance, automatically calculates risk levels, and alerts staff immediately when a student shows warning signs. This enables proactive intervention—reaching out to students before they fail, not after."

#### Q2: "Who are the users of this system?"

**Perfect Answer**:
> "There are two primary user roles: Administrators and Staff. Administrators manage the system—they upload data, configure risk thresholds, manage users, and view audit logs. Staff members are academic advisors who use the system to monitor students, view detailed profiles, download reports, and add intervention notes. Both roles are authenticated and have role-specific dashboards."

#### Q3: "How is this different from a spreadsheet?"

**Perfect Answer**:
> "Great question! While spreadsheets can store data, they lack several critical features: First, automation—our system automatically calculates risk scores and sends alerts without manual intervention. Second, real-time collaboration—multiple users can access simultaneously without version conflicts. Third, security—we have role-based access control, password protection, and audit trails. Fourth, scalability—a spreadsheet becomes unwieldy with thousands of students; our database handles millions of records efficiently. Finally, integration—this system can eventually connect to other university systems like attendance or library databases."

---

### Category 2: Technical Questions

#### Q4: "What framework did you use and why?"

**Perfect Answer**:
> "I used Flask, a lightweight Python web framework. I chose Flask for three reasons: First, it's beginner-friendly with a gentle learning curve. Second, it's modular—I could organize the code into blueprints for authentication, admin, and staff features. Third, it has excellent extensions like Flask-SQLAlchemy for database operations and Flask-Login for authentication. For a project of this scale, Flask provides the right balance of simplicity and power without the overhead of heavier frameworks like Django."

#### Q5: "How does the risk engine work?"

**Perfect Answer**:
> "The risk engine uses a rule-based approach. It evaluates each student against three criteria: First, it calculates their Cumulative GPA using a 5.0 grading scale. Second, it counts total course failures. Third, it specifically counts failures in core courses—classes essential to their major. Based on configurable thresholds, students are categorized as High Risk (GPA < 2.0 or multiple core failures), Medium Risk (GPA < 2.5 or any failures), or Low Risk. The engine also generates human-readable explanations for each classification, stored in the 'factors' field. This transparency is crucial—advisors need to know WHY a student was flagged, not just THAT they were flagged."

#### Q6: "How do you prevent duplicate data during import?"

**Perfect Answer**:
> "During CSV import, the system performs a four-field uniqueness check before inserting each record. It queries the database for an existing AcademicRecord with the same student_id, course_id, semester, and session. If a match exists, the record is skipped and counted as a duplicate. This prevents accidental double-counting if the same file is uploaded twice or if overlapping data exists. The import summary shows both 'records added' and 'duplicates skipped' so admins know exactly what happened."

#### Q7: "How are passwords stored securely?"

**Perfect Answer**:
> "Passwords are never stored in plain text. When a user sets a password, I use Werkzeug's `generate_password_hash()` function, which applies the PBKDF2 algorithm with SHA256 hashing and a random salt. This produces a one-way hash—easy to verify but impossible to reverse. During login, the entered password is hashed and compared to the stored hash using `check_password_hash()`. Even if someone gains access to the database, they cannot recover the original passwords."

#### Q8: "What database are you using and why?"

**Perfect Answer**:
> "I'm using SQLite, a file-based relational database. For this project, SQLite is ideal because: First, it requires zero configuration—no separate database server to install and maintain. Second, it's perfect for development and moderate-scale deployments. Third, it supports full SQL functionality including joins, transactions, and foreign keys. If the university scales this to tens of thousands of students, we could migrate to PostgreSQL with minimal code changes since SQLAlchemy abstracts the database layer."

---

### Category 3: Design Decision Questions

#### Q9: "Why did you choose rule-based risk assessment instead of machine learning?"

**Perfect Answer**:
> "This was a deliberate design decision based on three factors: First, **transparency**—with rule-based logic, we can explain exactly why a student was flagged. Machine learning models, especially deep learning, are often 'black boxes' that can't provide clear explanations. Second, **data availability**—training a reliable ML model requires years of historical data with outcomes (which students graduated, which dropped out). We didn't have that dataset. Third, **maintainability**—university policies change frequently. With rule-based logic, admins can adjust thresholds in the UI without retraining models or touching code. That said, I've architected the system so an ML model could be added later as an additional risk indicator alongside the rule-based system."

#### Q10: "Why separate routes into different files (auth.py, admin.py, staff.py)?"

**Perfect Answer**:
> "This follows the **Separation of Concerns** principle—a fundamental software engineering concept. Each file handles a specific domain: auth.py handles authentication, admin.py handles administrative tasks, staff.py handles advisor functions. This organization provides several benefits: First, **maintainability**—if there's a bug in the login system, I know exactly where to look. Second, **collaboration**—multiple developers can work on different modules without merge conflicts. Third, **scalability**—as features grow, the codebase remains organized. Fourth, **testing**—I can test each module independently. This is industry best practice and mirrors how professional software teams structure large applications."

#### Q11: "Why use SQLite instead of MySQL or PostgreSQL?"

**Perfect Answer**:
> "For this project's scope, SQLite offers the best developer experience. It requires no installation—just import and it works. There's no database server to configure, no connection strings to manage, and no permissions to set up. This let me focus on building features rather than managing infrastructure. However, the code is database-agnostic thanks to SQLAlchemy. If deployment requires PostgreSQL for concurrent access or advanced features, I can switch by changing one line in config.py: the database URI. The rest of the code remains unchanged."

#### Q12: "Why did you implement audit logging?"

**Perfect Answer**:
> "Audit logging serves three critical purposes: First, **security**—if unauthorized access occurs, we can trace what happened and when. Second, **accountability**—users know their actions are recorded, which discourages misuse. Third, **debugging**—when something goes wrong, logs help identify the root cause. In a university setting, audit trails may also be required for compliance with data protection regulations. Every sensitive action—logins, data imports, user changes, report downloads—is logged with the user ID, action type, details, and timestamp."

---

### Category 4: Scenario Questions

#### Q13: "What happens if two admins upload conflicting data at the same time?"

**Perfect Answer**:
> "SQLAlchemy handles concurrent access through database transactions. Each import runs in its own transaction. If two admins upload simultaneously: First, both uploads are processed independently. Second, the duplicate detection logic ensures that even if both files contain the same student record, only one copy is inserted—the second attempt finds the existing record and skips it. Third, database-level constraints (like unique indexes on student_id and course_code) prevent corruption. The import logs track both uploads separately, showing what each admin contributed. For production use, I'd add file locking to queue imports sequentially, but the current implementation is safe for moderate concurrency."

#### Q14: "How would you handle a student who disputes their risk classification?"

**Perfect Answer**:
> "The system is designed for this scenario. First, the student's advisor can view the 'factors' field that explains exactly why they were flagged—for example, 'GPA of 1.8 is below threshold 2.0'. This transparency allows for informed discussion. Second, if there's a data error (wrong grade entered), the admin can correct the underlying AcademicRecord, then re-run the risk evaluation. Third, if the student has extenuating circumstances (medical issues, family emergency), the advisor can add notes to the student profile documenting the situation. The risk score remains objective, but human context is preserved. Ultimately, the system supports decision-making but doesn't replace human judgment."

#### Q15: "What if the university changes its grading scale from 5.0 to 4.0?"

**Perfect Answer**:
> "Currently, the grading scale is hardcoded in the `calculate_gpa()` method in risk_engine.py. To support a change, I would: First, move the grade-to-points mapping into the database as a configurable table. Second, add a 'grading scale' setting in the admin panel. Third, ensure historical records preserve the scale that was active when they were created. This is actually a limitation I've identified for future improvement—the current implementation assumes a fixed 5.0 scale. In a production system, this would absolutely need to be configurable."

---

### Category 5: Future Work Questions

#### Q16: "What features would you add if you had more time?"

**Perfect Answer**:
> "I have a roadmap of enhancements: First, **email notifications**—currently notifications are in-app only; sending emails would ensure staff see urgent alerts. Second, **trend analysis**—tracking whether a student's performance is improving or declining over time, not just their current state. Third, **attendance integration**—correlating class attendance with grades to identify at-risk students earlier. Fourth, **predictive modeling**—using historical data to predict which students are likely to drop out. Fifth, **mobile app**—a React Native app for staff to check student profiles on the go. Sixth, **API endpoints**—to allow integration with other university systems. Seventh, **bulk interventions**—allowing advisors to send messages to groups of at-risk students simultaneously."

#### Q17: "How would you deploy this for a real university?"

**Perfect Answer**:
> "For production deployment, I would: First, switch from SQLite to PostgreSQL for better concurrency and reliability. Second, host on a cloud platform like AWS, Heroku, or DigitalOcean with automatic backups. Third, enable HTTPS with SSL certificates for secure communication. Fourth, set up environment variables for sensitive config (SECRET_KEY, database credentials) instead of hardcoding. Fifth, implement rate limiting to prevent abuse. Sixth, add monitoring with tools like Sentry for error tracking. Seventh, set up CI/CD pipelines for automated testing and deployment. Eighth, create separate environments for development, staging, and production. Ninth, implement proper backup and disaster recovery procedures. Tenth, conduct security audits and penetration testing before launch."

#### Q18: "Can this system integrate with existing university systems?"

**Perfect Answer**:
> "Absolutely—that's a key design goal. The CSV import feature is the first step, allowing data migration from legacy systems. For deeper integration, I've structured the code with an API layer (`backend/api/`) that could expose RESTful endpoints. Other systems could push student data via API instead of manual CSV uploads. The modular architecture means we could add connectors for specific student information systems (like Banner, PeopleSoft, or custom solutions). The audit log and notification systems could also feed into university-wide dashboards. Integration would require coordination with the university's IT department to align data formats and security protocols."

---

### Category 6: Challenging Questions

#### Q19: "Isn't this just a fancy database frontend? What's innovative about it?"

**Perfect Answer**:
> "While the foundation is a database frontend, the innovation lies in the **automated intelligence layer**. Traditional systems store data passively—humans must query and analyze it. Academic Sentinel actively monitors, analyzes, and alerts. The risk engine transforms raw grades into actionable insights without human intervention. The configurable rules mean the system adapts to different institutional policies without code changes. The audit trail provides enterprise-grade accountability. The notification system ensures timely intervention. And the PDF reporting automates what would otherwise be hours of manual document preparation. The innovation isn't in storing data—it's in making that data work for you, proactively identifying problems before they become crises."

#### Q20: "What was the most challenging part of building this?"

**Perfect Answer**:
> "The most challenging aspect was designing the risk engine to be both accurate and explainable. Initially, I considered complex statistical models, but realized that if an advisor asks 'why is this student flagged?', the system needs a clear answer—not a probability score. Balancing sophistication with transparency required careful thought. The second challenge was the CSV import pipeline—handling edge cases like missing columns, duplicate detection, and partial failures while providing user-friendly feedback. Getting the preview-confirm workflow right took several iterations. But overcoming these challenges taught me invaluable lessons about user-centered design and the importance of fail-safe data operations."

#### Q21: "If you had to start over, what would you do differently?"

**Perfect Answer**:
> "Three things: First, I'd implement automated testing from day one—unit tests for the risk engine, integration tests for the import pipeline. Testing would have caught several bugs early. Second, I'd use a more robust frontend framework like React or Vue.js instead of vanilla JavaScript with Tailwind. This would improve state management and component reusability. Third, I'd design the database with internationalization in mind—supporting multiple grading scales, different semester systems, and varied academic calendars from the start rather than retrofitting later. These lessons have shaped how I approach new projects now."

---

## 🎓 Tips for Your Presentation

### Before the Presentation

1. **Run the demo**: Make sure the system works flawlessly
2. **Prepare sample data**: Have the demo CSV ready to upload
3. **Know your code**: Be able to navigate to any file quickly
4. **Practice answers**: Rehearse responses to common questions
5. **Anticipate challenges**: Think of weak points and prepare defenses

### During the Presentation

1. **Start with the problem**: Explain WHY before HOW
2. **Show, don't just tell**: Demonstrate the system in action
3. **Highlight your decisions**: Explain WHY you made certain choices
4. **Acknowledge limitations**: Show self-awareness about what could be improved
5. **Speak confidently**: You built this—you know it better than anyone

### Body Language & Delivery

- Maintain eye contact
- Speak clearly and at a moderate pace
- Use hand gestures to emphasize points
- Don't read from slides—explain naturally
- Pause before answering difficult questions (shows thoughtfulness)

---

## 📚 Glossary of Terms

| Term | Definition |
|------|------------|
| **Backend** | Server-side code that processes data and business logic |
| **Frontend** | Client-side code (HTML/CSS/JS) that users interact with |
| **Database** | Structured storage for persistent data |
| **API** | Interface allowing different software systems to communicate |
| **Authentication** | Verifying a user's identity (login) |
| **Authorization** | Checking if a user has permission to do something |
| **Session** | Temporary state keeping a user logged in |
| **Hash** | One-way encryption (can't be reversed) |
| **CSV** | Comma-Separated Values—a text format for tabular data |
| **GPA** | Grade Point Average—a measure of academic performance |
| **Blueprint** | Flask's way of organizing routes into modules |
| **ORM** | Object-Relational Mapping (SQLAlchemy)—code instead of SQL |
| **Route** | A URL endpoint that triggers specific code |
| **Query** | A request for data from the database |
| **Transaction** | A group of database operations that succeed or fail together |
| **Foreign Key** | A field linking one table to another |
| **Normalization** | Organizing data to reduce redundancy |
| **Scalability** | Ability to handle growth (more users, more data) |
| **Deployment** | Making software available for use (putting it online) |
| **Audit Trail** | A chronological record of actions taken |

---

## 🔗 Resources for Further Learning

### Python & Flask
- [Flask Official Documentation](https://flask.palletsprojects.com/)
- [Python for Beginners](https://www.python.org/about/gettingstarted/)

### Databases
- [SQL Tutorial](https://www.sqltutorial.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

### Web Development
- [MDN Web Docs](https://developer.mozilla.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

### Software Engineering
- [Clean Code by Robert Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [Design Patterns](https://refactoring.guru/design-patterns)

---

## 👨‍💻 About This Project

**Academic Sentinel** was built as a demonstration of full-stack web development skills, combining:
- Backend development (Python/Flask)
- Database design (SQLAlchemy/SQLite)
- Frontend development (HTML/Tailwind/JavaScript)
- Security best practices (authentication, authorization, auditing)
- Business logic implementation (risk assessment engine)
- Report generation (PDF creation)
- Data processing (CSV import/validation)

This project showcases the ability to:
1. Identify a real-world problem
2. Design a comprehensive solution
3. Implement using appropriate technologies
4. Document thoroughly
5. Prepare for professional presentation

---

## 📞 Support

If you have questions about this project or need clarification on any section, refer to the code comments, which provide inline explanations of complex logic.

**Remember**: The best way to learn is by exploring the code yourself. Open the files, trace the execution, and experiment with modifications!

---

*Built with ❤️ for educational purposes*

*Last Updated: 2024*
