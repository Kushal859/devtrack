# DevTrack — Engineering Issue Tracker API

A minimal backend API for tracking engineering bugs and tasks, built with Django.

---

## How to Run

1. Clone the repository:
   git clone https://github.com/Kushal859/devtrack.git
   cd devtrack

2. Create and activate virtual environment:
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies:
   pip install django

4. Start the server:
   python manage.py runserver

API is available at: http://127.0.0.1:8000/

---

## Endpoints

### Reporter Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/reporters/ | Create a new reporter |
| GET | /api/reporters/ | Get all reporters |
| GET | /api/reporters/?id=1 | Get reporter by ID |

### Issue Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/issues/ | Create a new issue |
| GET | /api/issues/ | Get all issues |
| GET | /api/issues/?id=1 | Get issue by ID |
| GET | /api/issues/?status=open | Filter issues by status |

---

## Sample Requests

### POST /api/reporters/
Request body:
{
    "id": 1,
    "name": "Kushal Zambare",
    "email": "kushalzambare@1999.com",
    "team": "backend"
}

Response 201:
{
    "id": 1,
    "name": "Kushal Zambare",
    "email": "kushalzambare@1999.com",
    "team": "backend"
}

### POST /api/issues/
Request body:
{
    "id": 1,
    "title": "Login button not working on mobile",
    "description": "Users on iOS 17 cannot tap the login button",
    "status": "open",
    "priority": "critical",
    "reporter_id": 1
}

Response 201:
{
    "id": 1,
    "title": "Login button not working on mobile",
    "description": "Users on iOS 17 cannot tap the login button",
    "status": "open",
    "priority": "critical",
    "reporter_id": 1,
    "created_at": "2026-03-28 23:20:47.289582",
    "message": "[URGENT] Login button not working on mobile — needs immediate attention"
}

### Error Responses

400 Bad Request (validation failure):
{ "error": "Title cannot be empty" }

404 Not Found:
{ "error": "Issue not found" }

---

## Design Decision

**JSON files instead of a database.**

Data is stored in reporters.json and issues.json instead of SQLite or PostgreSQL.
This makes the data immediately visible and readable without any database tools,
and requires zero migration setup. The tradeoff is no indexing or concurrent
write safety, which is acceptable for a learning project.

**OOP class hierarchy in models.py.**

All business logic lives in models.py — BaseEntity, Reporter, Issue,
CriticalIssue, and LowPriorityIssue. Views stay thin and only handle
HTTP parsing and responses. This separation makes the logic easy to
test and understand independently of Django.
```

Save with `Ctrl + S`, then push:
```
git add README.md
git commit -m "Add README with endpoints and design decisions"
git push origin main