# Mental_Health_Check-in

# Mental Health Check-In

A hybrid app that helps users record how they feel each day and reflect on their mood over time.

> **Important:** This app is a self-reflection tool. It is **not** a medical device and does not give a diagnosis or replace a licensed professional. If you or someone you know is in crisis or in danger, contact local emergency services or a crisis hotline in your area right away: **Nationwide: 1553
Nationwide landline: 1800 1888 1553
Smart and TNT: 0919 057 1553
Globe and TM: 0917 899 8727 or 0966 351 4518**.

## Features

- Daily mood check-in (e.g., mood scale, short notes)
- [History or calendar of past check-ins]
- [Mood trends or charts]
- [Reminders or notifications]
- [Resources page with support contacts]
- Account registration and login

## Tech Stack

- Backend: [e.g., Django / Node.js]
- Frontend: [e.g., HTML, Tailwind CSS, JavaScript / React]
- Database: [e.g., SQLite for development, PostgreSQL for production]
- Other: [e.g., email service]

## Getting Started

### Prerequisites

- [Python 3.x / Node.js x.x]
- Git

### Installation

```bash
git clone https://github.com/[your-username]/[repo-name].git
cd [repo-name]

# create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows

pip install -r requirements.txt
```

### Environment variables

Copy `.env.example` to `.env` and fill in your own values:

```
SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

Never commit your real `.env` file or share its values.

### Run the project

```bash
python manage.py migrate
python manage.py runserver
```

Then open `http://127.0.0.1:8000/`.

## Project Structure

```
[repo-name]/
├── apps/          # feature modules
├── config/        # settings and main URLs
├── templates/     # HTML templates
├── static/        # CSS, JS, images
└── manage.py
```

## Privacy and Data Safety

Check-ins can contain sensitive personal information, so:

- Passwords are hashed and never stored in plain text.
- Each user can only see their own entries.
- Use fake or sample data when testing. Never use real people's entries.
- [State who can access the data, and how users can delete their account and entries.]

## Team and Roles

| Name | Role |
|------|------|
| [Cielo Seco] | [_] |
| [Franz Jowen Rances] | [_] |
| [Savannah De Mesa] | [[_] |
| [JM De Villa] | [_] |

## Contributing

1. Create a branch from `main`: `git switch -c feature/your-feature`
2. Commit your changes with a clear message
3. Push your branch and open a pull request for review



## License

[Add a license, or "For academic use only."]
