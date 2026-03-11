# Menlo Office Hours

A full-stack web application for scheduling one-on-one student-teacher meetings. Teachers post available time slots, students browse by department and book meetings — built to solve a real scheduling problem for a community of 56+ teachers across 8 departments.

## Tech Stack

| Layer        | Technology                              | Details                                                                 |
|--------------|-----------------------------------------|-------------------------------------------------------------------------|
| **Backend**  | Python, Flask                           | RESTful route handling, server-side session management, role-based access control |
| **Database** | SQLite, SQLAlchemy ORM                  | 3 relational models with foreign keys and `relationship()` back-references |
| **Frontend** | Jinja2, Bootstrap 4, jQuery             | Template inheritance across role-specific base layouts, responsive grid system |
| **Auth**     | Flask sessions                          | Dual-role authentication (student vs. teacher) with email domain validation |
| **Styling**  | Custom CSS, Google Fonts                | Branded UI with card-based layouts, gradient backgrounds, and mobile-responsive navbar |

## Features

- **Role-based authentication** — students register with domain-validated emails; teachers use pre-loaded accounts
- **Department filtering** — browse 56 teachers across 8 departments (Arts, CS, Engineering, English, History, Math, Science, World Language)
- **Availability management** — teachers create and remove open time slots by date and time
- **Meeting booking** — students select a teacher, pick an available slot, and add an optional description
- **Dashboard views** — separate meeting dashboards for students and teachers with upcoming appointments
- **Cancellation logic** — students can cancel bookings (frees the slot); teachers can delete unbooked slots
- **Auto-cleanup** — past meetings are automatically purged on page load

## Architecture

```
├── app.py              # Flask routes, session logic, and CRUD operations
├── models.py           # SQLAlchemy models — Student, Teacher, Meeting
├── database.py         # Engine config, scoped session, and Base class
├── setup.py            # Database seeding script (56 real teacher records)
├── templates/
│   ├── sign_base.html          # Base layout for auth pages
│   ├── student_base.html       # Base layout for student-facing pages
│   ├── teacher_base.html       # Base layout for teacher-facing pages
│   ├── sign_in.html            # Login form
│   ├── sign_up.html            # Student registration form
│   ├── schedule_options.html   # Teacher directory with department filter
│   ├── meeting_times.html      # Available time slot picker
│   ├── student_meetings.html   # Student meeting dashboard
│   ├── teacher_meetings.html   # Teacher meeting dashboard
│   └── available.html          # Teacher availability management
└── static/
    ├── images/                 # Logo and default profile assets
    └── styles/
        └── style.css           # Custom component styles
```

## Data Model

```
Student (1) ──── (*) Meeting (*) ──── (1) Teacher
   id                   id                  id
   first_name           date                first_name
   last_name            time                last_name
   email                description         email
   password             teacher_id (FK)     password
                        student_id (FK)     img_link
                                            department
```

Meetings act as the join between students and teachers. A meeting is created by a teacher (with no student attached), then claimed by a student during booking.

## What I Learned

- **Relational database design** — modeled real-world entities with SQLAlchemy ORM, using foreign keys and bidirectional relationships to connect students, teachers, and meetings
- **Server-side rendering** — built a multi-page app with Jinja2 template inheritance, creating role-specific base templates that share a consistent layout while varying navigation and permissions
- **Session-based auth** — implemented login flows for two distinct user roles with Flask sessions, including email domain validation and duplicate-account prevention
- **Full CRUD lifecycle** — handled create, read, update, and delete operations across the meeting entity, managing state transitions (open slot → booked meeting → cancelled)
- **Responsive UI** — used Bootstrap 4's grid system and custom CSS to build a card-based teacher directory, date-grouped time pickers, and mobile-friendly navigation

## Setup

### Prerequisites

- Python 3
- Flask and SQLAlchemy (`pip install flask sqlalchemy`)

### Running locally

```bash
# Seed the database with teacher data (first time only)
python setup.py

# Start the server
python app.py
```
