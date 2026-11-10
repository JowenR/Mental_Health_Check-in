# Mental Health Check-In

A full-stack mental health check-in web application developed to give students a simple and convenient way to check in on their well-being, manage their account and profile, and, as the system grows, book appointments and access support resources. Student and admin access are kept separate, so each role gets its own area of the system.

The system is developed using **Django, HTML, Tailwind CSS, and JavaScript,** with a structured backend and database architecture designed to support a complete check-in and appointment workflow.

---

## Features

- **Login** with email or Student ID
- **Create Account** (name, student ID, email, password, confirm password)
- **Role-based access**
  - Students are redirected to `/home/`
  - Admins (Django `is_staff`) are redirected to `/admin-panel/`
- **Home page** with a personalized greeting ("Good Day, (student name)!")
- **Student Profile**
  - Name, email, and student ID are based on the information entered during Create Account
  - Fields are read-only by default
  - Clicking **Edit Profile** makes the name and email editable, and the button changes to **Save Changes**
  - Changes are saved to the database and a "Profile updated!" popup is shown
  - Student ID cannot be edited
- **Forgot Password** via email link (Gmail SMTP)
- **Sidebar navigation** that highlights the current page

### In progress

- Check In
- Appointments
- Resources
- Admin profile

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django (Python) |
| Frontend | Django templates, Tailwind CSS v4, Bootstrap Icons |
| Database | SQLite (development) |
| Email | Gmail SMTP |

---

## Project Structure

```
Mental_Health_Check-In/
├── apps/
│   ├── accounts/          # login, signup, profile, backends, forms
│   └── core/
├── config/                # Django settings and root URLs
├── static/
│   ├── css/               # compiled Tailwind output (output.css)
│   ├── icons/             # sidebar and UI icons
│   ├── images/
│   ├── js/                # page scripts (e.g. students_profile.js)
│   └── src/               # Tailwind input (input.css)
├── templates/
│   ├── accounts/          # login, signup, students_profile, password_reset/
│   ├── components/layout/sidebar/
│   ├── layouts/           # base.html, auth_base.html
│   └── pages/             # home, admin_home
├── manage.py
├── package.json
├── requirements.txt
└── .env.example
```

---

## Getting Started

### Prerequisites

- Python 3.x
- Node.js and npm
- Git

### 1. Clone the repository

```
git clone https://github.com/<your-username>/Mental_Health_Check-In.git
cd Mental_Health_Check-In
```

If the project is inside another folder after cloning, `cd` into the folder that contains `manage.py` and `package.json`.

### 2. Set up the Python environment

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

On macOS/Linux, use `source venv/bin/activate` instead of `venv\Scripts\activate`.

### 3. Install Tailwind and other npm packages

```
npm install
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in your values:

```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

`EMAIL_HOST_PASSWORD` must be a Gmail **App Password**, not your normal Gmail password.

> Never commit your `.env` file. It is already listed in `.gitignore`.

### 5. Set up the database

```
python manage.py migrate
python manage.py createsuperuser
```

The superuser is used as an admin account (`is_staff`).

### 6. Run the project

You need **two terminals** running at the same time.

**Terminal 1: Tailwind (watches and compiles CSS)**

```
npm run dev
```

**Terminal 2: Django server**

```
python manage.py runserver
```

Then open [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

If styles are missing, make sure `npm run dev` is running, then hard refresh the browser (`Ctrl + Shift + R`).

---

## Main Routes

| URL | Description |
|---|---|
| `/` | Login page |
| `/signup/` | Create account |
| `/logout/` | Log out |
| `/home/` | Student home |
| `/student/profile/` | Student profile |
| `/admin-panel/` | Admin home |
| `/password-reset/` | Forgot password |

---

## Common Issues

**Page has no styling or new classes are not applied**
`npm run dev` is not running, or it was run in the wrong folder. Run it in the folder that contains `package.json`.

**`npm error ENOENT ... package.json`**
You are in the wrong folder. `cd` into the folder that contains `package.json`.

**`Can't resolve 'tailwindcss'`**
Run `npm install` first.

**Forgot Password email is not sent**
Check your `.env` values and make sure you are using a Gmail App Password.

---

## Team

Savannah De Mesa
John Mark De Villa
Franz Jowen Rances
Cielo Seco
