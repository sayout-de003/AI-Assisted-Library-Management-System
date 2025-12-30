# Library Management System (LMS)

A comprehensive Django REST Framework-based Library Management System with AI-powered book recommendations, role-based access control, and automated book issue/return management.

## Features

- **User Management**: Role-based authentication (Admin, Librarian, Member)
- **Book Management**: CRUD operations for books, categories, and members
- **Book Issuance**: Automated book issue and return with fine calculation
- **AI Recommendations**: ML-powered book recommendations based on member reading history
- **Overdue Management**: Automated overdue tracking and email notifications
- **Management Requests**: Members can request Admin/Librarian roles
- **JWT Authentication**: Secure token-based authentication
- **RESTful API**: Complete REST API with pagination, search, and filtering

## Tech Stack

- **Backend**: Django 6.0
- **API**: Django REST Framework 3.16.1
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL
- **AI/ML**: Sentence Transformers, PyTorch, scikit-learn
- **Task Queue**: Celery (optional)
- **Email**: SMTP (Gmail)

## Prerequisites

- Python 3.12+
- PostgreSQL 12+
- pip
- virtualenv (recommended)

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <https://github.com/sayout-de003/AI-Assisted-Library-Management-System>
cd websoft
```

### 2. Create Virtual Environment

```bash
python3 -m venv webl
source webl/bin/activate  # On Windows: webl\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root directory:

```bash
# Database Configuration
DB_NAME=library_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration (for overdue notifications)
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com

# Django Secret Key (generate a new one for production)
SECRET_KEY=your-secret-key-here
```

**Note**: For Gmail, you'll need to use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

### 5. Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE library_db;

# Exit PostgreSQL
\q
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 8. Seed Initial Data (Optional)

```bash
python scripts/seed_data.py
```

This will create:
- Sample categories (Science Fiction, Fantasy, History, Technology, Mathematics)
- Sample books with embeddings
- Sample members

### 9. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## API Documentation

Base URL: `http://127.0.0.1:8000/api/`

### Authentication

All endpoints (except signup and login) require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Authentication Endpoints

#### 1. User Signup
- **URL**: `/api/auth/signup/`
- **Method**: `POST`
- **Authentication**: Not required
- **Request Body**:
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "securepassword123"
}
```
- **Response**: `201 Created`
```json
{
  "message": "Signup successful"
}
```

#### 2. User Login
- **URL**: `/api/auth/login/`
- **Method**: `POST`
- **Authentication**: Not required
- **Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```
- **Response**: `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 3. Refresh Token
- **URL**: `/api/auth/refresh/`
- **Method**: `POST`
- **Authentication**: Not required
- **Request Body**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
- **Response**: `200 OK`
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### 4. User Logout
- **URL**: `/api/auth/logout/`
- **Method**: `POST`
- **Authentication**: Required
- **Request Body**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```
- **Response**: `205 Reset Content`
```json
{
  "message": "Logged out successfully"
}
```

### Management Endpoints

#### 5. Request Management Role
- **URL**: `/api/management/request/`
- **Method**: `POST`
- **Authentication**: Required
- **Permission**: Any authenticated user
- **Request Body**:
```json
{
  "requested_role": "LIBRARIAN"  // or "ADMIN"
}
```
- **Response**: `201 Created`
```json
{
  "message": "Management request submitted"
}
```

#### 6. Approve Management Request
- **URL**: `/api/management/approve/<request_id>/`
- **Method**: `POST`
- **Authentication**: Required
- **Permission**: Admin only
- **Response**: `200 OK`
```json
{
  "message": "Management request approved"
}
```

#### 7. Reject Management Request
- **URL**: `/api/management/reject/<request_id>/`
- **Method**: `POST`
- **Authentication**: Required
- **Permission**: Admin only
- **Response**: `200 OK`
```json
{
  "message": "Management request rejected"
}
```

### Book Management Endpoints

#### 8. List/Create Books
- **URL**: `/api/books/`
- **Methods**: `GET`, `POST`
- **Authentication**: Required
- **Query Parameters** (for GET):
  - `search`: Search in title, author, ISBN
  - `ordering`: Order by field (e.g., `title`, `-title`)
  - `page`: Page number (pagination)
- **GET Response**: `200 OK`
```json
{
  "count": 10,
  "next": "http://127.0.0.1:8000/api/books/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Dune",
      "author": "Frank Herbert",
      "isbn": "9780441013593",
      "category": 1,
      "total_copies": 5,
      "available_copies": 3,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```
- **POST Request Body**:
```json
{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "isbn": "9780743273565",
  "category": 1,
  "total_copies": 10,
  "available_copies": 10
}
```

#### 9. Retrieve/Update/Delete Book
- **URL**: `/api/books/<id>/`
- **Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Authentication**: Required
- **GET Response**: `200 OK` (Book object)
- **PUT/PATCH Response**: `200 OK` (Updated book object)
- **DELETE Response**: `204 No Content`

### Category Endpoints

#### 10. List/Create Categories
- **URL**: `/api/categories/`
- **Methods**: `GET`, `POST`
- **Authentication**: Required
- **POST Request Body**:
```json
{
  "name": "Mystery"
}
```

#### 11. Retrieve/Update/Delete Category
- **URL**: `/api/categories/<id>/`
- **Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Authentication**: Required

### Member Endpoints

#### 12. List/Create Members
- **URL**: `/api/members/`
- **Methods**: `GET`, `POST`
- **Authentication**: Required
- **POST Request Body**:
```json
{
  "name": "Jane Doe",
  "membership_id": "MEM-000001",
  "email": "jane@example.com",
  "is_active": true
}
```

#### 13. Retrieve/Update/Delete Member
- **URL**: `/api/members/<id>/`
- **Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
- **Authentication**: Required

### Book Issue/Return Endpoints

#### 14. Issue Book
- **URL**: `/api/books/issue/`
- **Method**: `POST`
- **Authentication**: Required
- **Request Body**:
```json
{
  "book_id": 1,
  "member_id": 1
}
```
- **Response**: `201 Created`
```json
{
  "id": 1,
  "book": 1,
  "member": 1,
  "issue_date": "2024-01-15",
  "due_date": "2024-01-29",
  "return_date": null,
  "fine_amount": "0.00"
}
```

#### 15. Return Book
- **URL**: `/api/books/return/<issue_id>/`
- **Method**: `POST`
- **Authentication**: Required
- **Response**: `200 OK`
```json
{
  "id": 1,
  "book": 1,
  "member": 1,
  "issue_date": "2024-01-15",
  "due_date": "2024-01-29",
  "return_date": "2024-01-30",
  "fine_amount": "5.00"
}
```

### Report Endpoints

#### 16. Overdue Books Report
- **URL**: `/api/reports/overdue/`
- **Method**: `GET`
- **Authentication**: Required
- **Response**: `200 OK`
```json
[
  {
    "id": 1,
    "book": 1,
    "member": 1,
    "issue_date": "2024-01-01",
    "due_date": "2024-01-15",
    "return_date": null,
    "fine_amount": "0.00"
  }
]
```
**Note**: This endpoint also sends email notifications to members with overdue books.

### AI Recommendation Endpoints

#### 17. Book Recommendations
- **URL**: `/api/books/recommend/<member_id>/`
- **Method**: `GET`
- **Authentication**: Required
- **Response**: `200 OK`
```json
[
  {
    "id": 5,
    "title": "Foundation",
    "author": "Isaac Asimov",
    "isbn": "9780553293357",
    "category": 1,
    "total_copies": 3,
    "available_copies": 2
  }
]
```
**Note**: Recommendations are based on the member's previous book issues using AI embeddings.

## User Roles & Permissions

### Roles

1. **MEMBER**: Default role for new users
   - Can view books, categories, members
   - Can request management roles
   - Can view their own book issues

2. **LIBRARIAN**: Can manage library operations
   - All member permissions
   - Can issue/return books
   - Can view reports
   - Can manage books, categories, members

3. **ADMIN**: Full system access
   - All librarian permissions
   - Can approve/reject management requests
   - Can manage all users

### Permission Classes

- `IsAuthenticated`: Required for most endpoints
- `IsAdmin`: Admin-only endpoints
- `IsManagement`: Admin or Librarian only

## API Features

### Pagination
All list endpoints support pagination with 10 items per page by default.

### Search & Filtering
- **Search**: Available on books endpoint (`?search=keyword`)
- **Ordering**: Available on all list endpoints (`?ordering=field_name` or `?ordering=-field_name`)

### Example Queries

```bash
# Search books
GET /api/books/?search=dune

# Order books by title
GET /api/books/?ordering=title

# Get second page
GET /api/books/?page=2
```

## Database Models

### User
- Custom user model with email as username
- Roles: ADMIN, LIBRARIAN, MEMBER
- MemberProfile: Auto-generated member ID (MEM-000001)

### Book
- Title, author, ISBN
- Category (ForeignKey)
- Total and available copies
- Embedding (for AI recommendations)

### BookIssue
- Book and member references
- Issue date, due date, return date
- Fine amount calculation

### ManagementRequest
- User requests for Admin/Librarian roles
- Status: PENDING, APPROVED, REJECTED

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
```

### Applying Migrations

```bash
python manage.py migrate
```

### Django Admin

Access the admin panel at `http://127.0.0.1:8000/admin/` using your superuser credentials.

## Production Deployment

Before deploying to production:

1. Set `DEBUG = False` in `settings.py`
2. Generate a new `SECRET_KEY`
3. Update `ALLOWED_HOSTS` with your domain
4. Configure proper database credentials
5. Set up static file serving
6. Configure HTTPS
7. Set up proper email backend
8. Use environment variables for all sensitive data

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Verify database credentials in `.env`
- Check database exists: `psql -U postgres -l`

### Email Not Sending
- Verify Gmail App Password is correct
- Check email settings in `.env`
- Ensure `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are set

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check Python version (3.12+)

## License


This project is licensed under the MIT License. See the LICENSE file for details.

[Your Contributing Guidelines Here]

## Support

For issues and questions, please open an issue in the repository.
