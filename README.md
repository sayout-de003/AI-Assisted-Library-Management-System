
# AI-Assisted Library Management System (LMS)

A comprehensive Django REST Framework-based Library Management System with AI-powered book recommendations, role-based access control, and automated book issue/return management.

---

## 🚀 Features

- **User Management**: Role-based authentication (Admin, Librarian, Member).
- **Book Management**: CRUD operations for books, categories, and members.
- **Book Issuance**: Automated book issue and return with fine calculation.
- **AI Recommendations**: ML-powered book recommendations using Sentence Transformers based on member reading history.
- **Overdue Management**: Automated overdue tracking and email notifications.
- **Automated Emails**: Welcome emails sent upon member signup and overdue reminders for unreturned books.
- **Fine Calculation**: Automatic fine assessment at $5 per overdue day upon book return.
- **Member ID Generation**: Unique membership IDs generated as "MEM" followed by a zero-padded user ID (e.g., MEM0001).
- **Management Requests**: Members can request Admin/Librarian roles.
- **JWT Authentication**: Secure token-based authentication with refresh capability.
- **RESTful API**: Complete REST API with pagination, search, and filtering.
- **Modern Frontend**: React 19+ interface with responsive design.

---

## 🛠 Tech Stack

### Backend
- **Framework**: Django 
- **API**: Django REST Framework 
- **Database**: PostgreSQL
- **Authentication**: JWT (`djangorestframework-simplejwt`)
- **AI/ML**: Sentence Transformers, PyTorch, scikit-learn
- **Email**: SMTP (Gmail)

### Frontend
- **Framework**: React 19.2.3
- **Routing**: React Router DOM
- **HTTP Client**: Axios
- **Styling**: CSS Modules / Standard CSS

---

## 📂 Backend Directory Structure

```text
websoft/
├── apps/
│   ├── ai_engine/           # AI Logic & Recommendations
│   │   ├── models.py
│   │   ├── recommender.py
│   │   ├── tasks.py
│   │   ├── views.py
│   │   └── ...
│   ├── api/                 # Central API Configuration
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── viewsets.py
│   │   └── urls.py
│   ├── core/                # Core Utilities & Abstract Models
│   │   ├── models.py
│   │   ├── pagination.py
│   │   ├── renderers.py
│   │   └── utils.py
│   ├── library/             # Main Library Business Logic
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   └── views.py
│   └── users/               # Authentication & Role Management
│       ├── managers.py
│       ├── models.py
│       ├── permissions.py
│       ├── serializers.py
│       └── views.py
├── library_lms/             # Project Settings
│   ├── settings.py
│   └── urls.py
├── scripts/
│   └── seed_data.py         # Data population script
├── tests/
├── manage.py
└── requirements.txt

```

## 📂 Frontend Directory Structure

```text
library-frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── Header.jsx
│   │   └── modals/
│   │       └── IssueReturnModal.jsx
│   ├── context/
│   │   └── AuthContext.jsx
│   ├── pages/
│   │   ├── Books.jsx
│   │   ├── Categories.jsx
│   │   ├── Login.jsx
│   │   └── Members.jsx
│   ├── services/
│   │   └── api.js
│   ├── App.js
│   ├── App.css
│   └── index.js
├── package.json
└── README.md

```

---

## ⚙️ Prerequisites

* Python 
* Node.js & npm (for frontend)
* PostgreSQL 
* Virtualenv

---

## ⚡ Backend Setup Guide

### 1. Clone the Repository

```bash
git clone (https://github.com/sayout-de003/AI-Assisted-Library-Management-System)
cd websoft

```

### 2. Environment Setup

```bash
python3 -m venv webl
source webl/bin/activate  # On Windows: webl\Scripts\activate
pip install -r requirements.txt

```

### 3. Environment Variables

Create a `.env` file in the root directory:

```env
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com

SECRET_KEY=your-secret-key-here

```

### 4. Database Initialization

```bash
# Create Database (via psql or pgAdmin)
psql -U postgres -c "CREATE DATABASE library_db;"

# Run Migrations
python manage.py makemigrations
python manage.py migrate

```

### 5. Create Superuser & Seed Data

```bash
python manage.py createsuperuser
python scripts/seed_data.py  # Populates books, categories, and embeddings

```

### 6. Start Backend Server

```bash
python manage.py runserver

```

* **API Base**: `http://127.0.0.1:8000/api/`
* **Admin Panel**: [`http://127.0.0.1:8000/admin/`](http://127.0.0.1:8000/admin/)

---

## 💻 Frontend Setup Guide

### 1. Install Dependencies

```bash
cd library-frontend
npm install

```

### 2. Start Frontend Server

```bash
npm start

```

* **App URL**: [`http://localhost:3000`](https://www.google.com/search?q=http://localhost:3000)

---

## 🔗 API to Frontend Mapping

Below is the complete list of backend API endpoints mapped to their corresponding Frontend Pages and URLs.

### 🔐 Authentication

| Action | API Endpoint | Frontend Component | Frontend URL |
| --- | --- | --- | --- |
| **Login** | `POST /api/auth/login/` | `Login.jsx` | `http://localhost:3000/` |
| **Signup** | `POST /api/auth/signup/` | `Login.jsx` | `http://localhost:3000/` |
| **Refresh** | `POST /api/auth/refresh/` | `AuthContext.jsx` | *(Background Process)* |

### 📚 Books & Library

| Action | API Endpoint | Frontend Component | Frontend URL |
| --- | --- | --- | --- |
| **List Books** | `GET /api/books/` | `Books.jsx` | `http://localhost:3000/books` |
| **Create Book** | `POST /api/books/` | `Books.jsx` | `http://localhost:3000/books` |
| **Book Details** | `GET /api/books/<id>/` | `Books.jsx` | `http://localhost:3000/books` |
| **Issue Book** | `POST /api/books/issue/` | `IssueReturnModal.jsx` | *(Modal on Books Page)* |
| **Return Book** | `POST /api/books/return/<id>/` | `IssueReturnModal.jsx` | *(Modal on Books Page)* |
| **AI Recommender** | `GET /api/books/recommend/<id>/` | `Books.jsx` | `http://localhost:3000/books` |
| **Overdue Rpt** | `GET /api/reports/overdue/` | `Books.jsx` | `http://localhost:3000/books` |

### 📂 Categories

| Action | API Endpoint | Frontend Component | Frontend URL |
| --- | --- | --- | --- |
| **List Cats** | `GET /api/categories/` | `Categories.jsx` | `http://localhost:3000/categories` |
| **Manage Cats** | `POST/PUT /api/categories/<id>/` | `Categories.jsx` | `http://localhost:3000/categories` |

### 👥 Members & Management

| Action | API Endpoint | Frontend Component | Frontend URL |
| --- | --- | --- | --- |
| **List Members** | `GET /api/members/` | `Members.jsx` | `http://localhost:3000/members` |
| **Req. Role** | `POST /api/management/request/` | `Members.jsx` | `http://localhost:3000/members` |
| **Approve Role** | `POST /api/management/approve/` | `Members.jsx` | `http://localhost:3000/members` |

---

## ℹ️ Additional Implementation Details

### Pagination

* **Backend**: Implemented using `PageNumberPagination` in `apps/core/pagination.py`.
* **Frontend**: Fully handled in `Books.jsx`, `Categories.jsx`, and `Members.jsx`.
* **Default**: 10 items per page.
* **Usage**: `?page=2` appended to API calls.

### Search & Filtering

* Supported on List endpoints.
* **Query Param**: `?search=keyword` (e.g., Book Title, ISBN, Member Name).
* **Ordering**: `?ordering=field` (e.g., `?ordering=-created_at`).

### User Roles

1. **MEMBER**: View books, view own history, request upgrades.
2. **LIBRARIAN**: Issue/Return books, Manage inventory.
3. **ADMIN**: Manage Users, Approve Roles, Full Access.

---

## 📄 License

MIT License.

