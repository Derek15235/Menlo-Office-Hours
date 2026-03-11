# Menlo Office Hours

A web application for scheduling one-on-one student-teacher meetings at Menlo School. Teachers post their available time slots and students book meetings — simple, fast, and built for the Menlo community.

## Features

- **Student registration & login** — sign up with a `@menloschool.org` email
- **Teacher login** — pre-loaded accounts for 56 teachers across 8 departments
- **Availability management** — teachers create open time slots by date and time
- **Meeting booking** — students browse teachers by department, pick a slot, and add an optional description
- **Cancellation** — students can cancel their bookings; teachers can remove unbooked slots
- **Auto-cleanup** — past meetings are automatically removed

## Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Backend   | Python, Flask                       |
| Database  | SQLite via SQLAlchemy               |
| Frontend  | Jinja2 templates, Bootstrap 4, jQuery |
| Auth      | Flask session-based authentication  |

## Project Structure

```
├── app.py              # Flask routes and application logic
├── models.py           # SQLAlchemy models (Student, Teacher, Meeting)
├── database.py         # Database initialization and session config
├── setup.py            # Script to seed teachers into the database
├── templates/          # Jinja2 HTML templates
│   ├── sign_base.html          # Base layout for auth pages
│   ├── student_base.html       # Base layout for student pages
│   ├── teacher_base.html       # Base layout for teacher pages
│   ├── sign_in.html            # Login page
│   ├── sign_up.html            # Student registration
│   ├── schedule_options.html   # Browse teachers by department
│   ├── meeting_times.html      # Pick an available time slot
│   ├── student_meetings.html   # Student's upcoming meetings
│   ├── teacher_meetings.html   # Teacher's upcoming meetings
│   └── available.html          # Teacher availability entry
└── static/
    ├── images/         # Menlo logo and default profile picture
    └── styles/
        └── style.css   # Custom styles
```

## Setup

### Prerequisites

- Python 3
- `pip install flask sqlalchemy`

### First-time initialization

1. Open `setup.py` and update each teacher's default password (`"ph"`) to their desired password.
2. Run the setup script once to seed the database:
   ```bash
   python setup.py
   ```

### Running the app

```bash
python app.py
```

The server starts on `http://172.16.3.53:5001` by default (configured in `app.py`).

## How It Works

1. **Teachers** log in and post available date/time slots via the availability page.
2. **Students** sign up, browse teachers filtered by department, and book an open slot.
3. Both sides can view and manage their upcoming meetings from their dashboard.

## Departments

Arts, Computer Science, Engineering, English, History, Math, Science, World Language
