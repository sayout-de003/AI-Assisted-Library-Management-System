# Frontend Development Guide - Library Management System

Complete step-by-step guide to build a simple frontend application for the Library Management System API.

## Table of Contents

1. [API Endpoints with Pagination](#api-endpoints-with-pagination)
2. [Frontend Setup](#frontend-setup)
3. [Project Structure](#project-structure)
4. [Step-by-Step Implementation](#step-by-step-implementation)
5. [Complete Code Examples](#complete-code-examples)

---

## API Endpoints with Pagination

### Base Configuration
- **Base URL**: `http://127.0.0.1:8000/api/`
- **Pagination**: All list endpoints return paginated results
- **Page Size**: 10 items per page
- **Pagination Response Format**:
```json
{
  "count": 50,
  "next": "http://127.0.0.1:8000/api/books/?page=2",
  "previous": null,
  "results": [...]
}
```

### Complete API List

#### Authentication Endpoints (No Auth Required)

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/api/auth/signup/` | User registration | `{email, name, password}` | `{message}` |
| POST | `/api/auth/login/` | Get JWT tokens | `{email, password}` | `{access, refresh}` |
| POST | `/api/auth/refresh/` | Refresh access token | `{refresh}` | `{access}` |
| POST | `/api/auth/logout/` | Logout (blacklist token) | `{refresh}` | `{message}` |

#### Paginated List Endpoints (Auth Required)

| Method | Endpoint | Description | Query Params | Pagination |
|--------|----------|-------------|--------------|------------|
| GET | `/api/books/` | List all books | `?page=1&search=keyword&ordering=title` | ✅ Yes |
| GET | `/api/categories/` | List all categories | `?page=1&ordering=name` | ✅ Yes |
| GET | `/api/members/` | List all members | `?page=1&ordering=name` | ✅ Yes |

#### Detail Endpoints (Auth Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/books/<id>/` | Get book details |
| POST | `/api/books/` | Create new book |
| PUT | `/api/books/<id>/` | Update book |
| PATCH | `/api/books/<id>/` | Partial update book |
| DELETE | `/api/books/<id>/` | Delete book |
| GET | `/api/categories/<id>/` | Get category details |
| POST | `/api/categories/` | Create category |
| PUT/PATCH | `/api/categories/<id>/` | Update category |
| DELETE | `/api/categories/<id>/` | Delete category |
| GET | `/api/members/<id>/` | Get member details |
| POST | `/api/members/` | Create member |
| PUT/PATCH | `/api/members/<id>/` | Update member |
| DELETE | `/api/members/<id>/` | Delete member |

#### Action Endpoints (Auth Required)

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| POST | `/api/books/issue/` | Issue book to member | `{book_id, member_id}` |
| POST | `/api/books/return/<issue_id>/` | Return a book | - |
| GET | `/api/reports/overdue/` | Get overdue books | - |
| GET | `/api/books/recommend/<member_id>/` | Get book recommendations | - |
| POST | `/api/management/request/` | Request management role | `{requested_role}` |
| POST | `/api/management/approve/<request_id>/` | Approve request (Admin) | - |
| POST | `/api/management/reject/<request_id>/` | Reject request (Admin) | - |

---

## Frontend Setup

### Step 1: Initialize React Project

```bash
# Create new React app
npx create-react-app library-frontend
cd library-frontend

# Install required dependencies
npm install axios react-router-dom
```

### Step 2: Install Additional Dependencies (Optional but Recommended)

```bash
# For better UI components
npm install @mui/material @emotion/react @emotion/styled
# OR use Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Step 3: Project Structure

```
library-frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── BookList.jsx
│   │   ├── BookCard.jsx
│   │   ├── Pagination.jsx
│   │   ├── SearchBar.jsx
│   │   └── Loading.jsx
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Signup.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Books.jsx
│   │   ├── Members.jsx
│   │   └── Categories.jsx
│   ├── services/
│   │   └── api.js
│   ├── utils/
│   │   └── auth.js
│   ├── context/
│   │   └── AuthContext.jsx
│   ├── App.js
│   └── index.js
└── package.json
```

---

## Step-by-Step Implementation

### Step 1: Create API Service Layer

Create `src/services/api.js`:

```javascript
import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
          refresh: refreshToken,
        });
        
        const { access } = response.data;
        localStorage.setItem('access_token', access);
        
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

// Authentication APIs
export const authAPI = {
  signup: (data) => api.post('/auth/signup/', data),
  login: (data) => api.post('/auth/login/', data),
  logout: (data) => api.post('/auth/logout/', data),
  refresh: (data) => api.post('/auth/refresh/', data),
};

// Books API with pagination
export const booksAPI = {
  list: (params = {}) => {
    const { page = 1, search = '', ordering = '' } = params;
    const queryParams = new URLSearchParams();
    if (page) queryParams.append('page', page);
    if (search) queryParams.append('search', search);
    if (ordering) queryParams.append('ordering', ordering);
    
    return api.get(`/books/?${queryParams.toString()}`);
  },
  get: (id) => api.get(`/books/${id}/`),
  create: (data) => api.post('/books/', data),
  update: (id, data) => api.put(`/books/${id}/`, data),
  patch: (id, data) => api.patch(`/books/${id}/`, data),
  delete: (id) => api.delete(`/books/${id}/`),
  issue: (data) => api.post('/books/issue/', data),
  return: (issueId) => api.post(`/books/return/${issueId}/`),
  recommend: (memberId) => api.get(`/books/recommend/${memberId}/`),
};

// Categories API with pagination
export const categoriesAPI = {
  list: (params = {}) => {
    const { page = 1, ordering = '' } = params;
    const queryParams = new URLSearchParams();
    if (page) queryParams.append('page', page);
    if (ordering) queryParams.append('ordering', ordering);
    
    return api.get(`/categories/?${queryParams.toString()}`);
  },
  get: (id) => api.get(`/categories/${id}/`),
  create: (data) => api.post('/categories/', data),
  update: (id, data) => api.put(`/categories/${id}/`, data),
  patch: (id, data) => api.patch(`/categories/${id}/`, data),
  delete: (id) => api.delete(`/categories/${id}/`),
};

// Members API with pagination
export const membersAPI = {
  list: (params = {}) => {
    const { page = 1, ordering = '' } = params;
    const queryParams = new URLSearchParams();
    if (page) queryParams.append('page', page);
    if (ordering) queryParams.append('ordering', ordering);
    
    return api.get(`/members/?${queryParams.toString()}`);
  },
  get: (id) => api.get(`/members/${id}/`),
  create: (data) => api.post('/members/', data),
  update: (id, data) => api.put(`/members/${id}/`, data),
  patch: (id, data) => api.patch(`/members/${id}/`, data),
  delete: (id) => api.delete(`/members/${id}/`),
};

// Reports API
export const reportsAPI = {
  overdue: () => api.get('/reports/overdue/'),
};

// Management API
export const managementAPI = {
  request: (data) => api.post('/management/request/', data),
  approve: (requestId) => api.post(`/management/approve/${requestId}/`),
  reject: (requestId) => api.post(`/management/reject/${requestId}/`),
};

export default api;
```

### Step 2: Create Authentication Context

Create `src/context/AuthContext.jsx`:

```javascript
import React, { createContext, useState, useContext, useEffect } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('access_token');
    if (token) {
      // You can decode JWT to get user info or make an API call
      // For now, we'll just check token existence
      setUser({ token });
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      const response = await authAPI.login({ email, password });
      const { access, refresh } = response.data;
      
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      
      setUser({ token: access });
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      };
    }
  };

  const signup = async (email, name, password) => {
    try {
      await authAPI.signup({ email, name, password });
      return { success: true };
    } catch (error) {
      return { 
        success: false, 
        error: error.response?.data || 'Signup failed' 
      };
    }
  };

  const logout = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        await authAPI.logout({ refresh: refreshToken });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, signup, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```

### Step 3: Create Pagination Component

Create `src/components/Pagination.jsx`:

```javascript
import React from 'react';

const Pagination = ({ currentPage, totalPages, onPageChange, count }) => {
  const pages = [];
  const maxVisiblePages = 5;
  
  let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
  let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
  
  if (endPage - startPage < maxVisiblePages - 1) {
    startPage = Math.max(1, endPage - maxVisiblePages + 1);
  }

  for (let i = startPage; i <= endPage; i++) {
    pages.push(i);
  }

  if (totalPages <= 1) return null;

  return (
    <div className="pagination">
      <div className="pagination-info">
        Showing page {currentPage} of {totalPages} (Total: {count} items)
      </div>
      
      <div className="pagination-controls">
        <button
          onClick={() => onPageChange(1)}
          disabled={currentPage === 1}
          className="pagination-btn"
        >
          First
        </button>
        
        <button
          onClick={() => onPageChange(currentPage - 1)}
          disabled={currentPage === 1}
          className="pagination-btn"
        >
          Previous
        </button>

        {pages.map((page) => (
          <button
            key={page}
            onClick={() => onPageChange(page)}
            className={`pagination-btn ${currentPage === page ? 'active' : ''}`}
          >
            {page}
          </button>
        ))}

        <button
          onClick={() => onPageChange(currentPage + 1)}
          disabled={currentPage === totalPages}
          className="pagination-btn"
        >
          Next
        </button>
        
        <button
          onClick={() => onPageChange(totalPages)}
          disabled={currentPage === totalPages}
          className="pagination-btn"
        >
          Last
        </button>
      </div>
    </div>
  );
};

export default Pagination;
```

### Step 4: Create Book List Component with Pagination

Create `src/components/BookList.jsx`:

```javascript
import React, { useState, useEffect } from 'react';
import { booksAPI } from '../services/api';
import Pagination from './Pagination';
import BookCard from './BookCard';
import Loading from './Loading';
import SearchBar from './SearchBar';

const BookList = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [count, setCount] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [ordering, setOrdering] = useState('');

  const fetchBooks = async (page = 1, search = '', order = '') => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await booksAPI.list({ 
        page, 
        search, 
        ordering: order 
      });
      
      const { count, next, previous, results } = response.data;
      
      setBooks(results);
      setCount(count);
      
      // Calculate total pages
      const pages = Math.ceil(count / 10);
      setTotalPages(pages);
      
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch books');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBooks(currentPage, searchQuery, ordering);
  }, [currentPage, searchQuery, ordering]);

  const handlePageChange = (page) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSearch = (query) => {
    setSearchQuery(query);
    setCurrentPage(1); // Reset to first page on new search
  };

  const handleOrderingChange = (e) => {
    setOrdering(e.target.value);
    setCurrentPage(1);
  };

  if (loading && books.length === 0) {
    return <Loading />;
  }

  return (
    <div className="book-list-container">
      <div className="book-list-header">
        <h1>Books Library</h1>
        
        <div className="book-list-controls">
          <SearchBar onSearch={handleSearch} placeholder="Search books..." />
          
          <select 
            value={ordering} 
            onChange={handleOrderingChange}
            className="ordering-select"
          >
            <option value="">Sort by...</option>
            <option value="title">Title (A-Z)</option>
            <option value="-title">Title (Z-A)</option>
            <option value="author">Author (A-Z)</option>
            <option value="-author">Author (Z-A)</option>
            <option value="created_at">Newest First</option>
            <option value="-created_at">Oldest First</option>
          </select>
        </div>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <div className="books-grid">
        {books.length === 0 ? (
          <p>No books found.</p>
        ) : (
          books.map((book) => (
            <BookCard key={book.id} book={book} />
          ))
        )}
      </div>

      <Pagination
        currentPage={currentPage}
        totalPages={totalPages}
        count={count}
        onPageChange={handlePageChange}
      />
    </div>
  );
};

export default BookList;
```

### Step 5: Create Book Card Component

Create `src/components/BookCard.jsx`:

```javascript
import React from 'react';

const BookCard = ({ book }) => {
  return (
    <div className="book-card">
      <div className="book-card-header">
        <h3>{book.title}</h3>
        <span className="book-status">
          {book.available_copies > 0 ? 'Available' : 'Unavailable'}
        </span>
      </div>
      
      <div className="book-card-body">
        <p className="book-author">By {book.author}</p>
        <p className="book-isbn">ISBN: {book.isbn}</p>
        <div className="book-copies">
          <span>Available: {book.available_copies}</span>
          <span>Total: {book.total_copies}</span>
        </div>
      </div>
      
      <div className="book-card-footer">
        <button className="btn-primary">View Details</button>
        {book.available_copies > 0 && (
          <button className="btn-secondary">Issue Book</button>
        )}
      </div>
    </div>
  );
};

export default BookCard;
```

### Step 6: Create Search Bar Component

Create `src/components/SearchBar.jsx`:

```javascript
import React, { useState } from 'react';

const SearchBar = ({ onSearch, placeholder = "Search..." }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  const handleChange = (e) => {
    setQuery(e.target.value);
    // Optional: Debounce for real-time search
    // You can add debounce here if needed
  };

  return (
    <form onSubmit={handleSubmit} className="search-bar">
      <input
        type="text"
        value={query}
        onChange={handleChange}
        placeholder={placeholder}
        className="search-input"
      />
      <button type="submit" className="search-btn">
        Search
      </button>
    </form>
  );
};

export default SearchBar;
```

### Step 7: Create Loading Component

Create `src/components/Loading.jsx`:

```javascript
import React from 'react';

const Loading = () => {
  return (
    <div className="loading-container">
      <div className="loading-spinner"></div>
      <p>Loading...</p>
    </div>
  );
};

export default Loading;
```

### Step 8: Create Login Page

Create `src/pages/Login.jsx`:

```javascript
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(email, password);
    
    if (result.success) {
      navigate('/dashboard');
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Login</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          
          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
        
        <p className="auth-link">
          Don't have an account? <Link to="/signup">Sign up</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
```

### Step 9: Create Signup Page

Create `src/pages/Signup.jsx`:

```javascript
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Signup = () => {
  const [formData, setFormData] = useState({
    email: '',
    name: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { signup } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);

    const result = await signup(
      formData.email,
      formData.name,
      formData.password
    );

    if (result.success) {
      navigate('/login');
    } else {
      setError(result.error);
    }

    setLoading(false);
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Sign Up</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Name</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>
          
          <div className="form-group">
            <label>Confirm Password</label>
            <input
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
            />
          </div>
          
          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Signing up...' : 'Sign Up'}
          </button>
        </form>
        
        <p className="auth-link">
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
};

export default Signup;
```

### Step 10: Create Dashboard Page

Create `src/pages/Dashboard.jsx`:

```javascript
import React from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <div className="dashboard">
      <nav className="navbar">
        <h1>Library Management System</h1>
        <div className="nav-links">
          <Link to="/books">Books</Link>
          <Link to="/members">Members</Link>
          <Link to="/categories">Categories</Link>
          <button onClick={handleLogout} className="btn-logout">
            Logout
          </button>
        </div>
      </nav>

      <div className="dashboard-content">
        <h2>Welcome to the Library Management System</h2>
        <div className="dashboard-cards">
          <Link to="/books" className="dashboard-card">
            <h3>Books</h3>
            <p>Manage library books</p>
          </Link>
          <Link to="/members" className="dashboard-card">
            <h3>Members</h3>
            <p>Manage library members</p>
          </Link>
          <Link to="/categories" className="dashboard-card">
            <h3>Categories</h3>
            <p>Manage book categories</p>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
```

### Step 11: Create Main App Component

Update `src/App.js`:

```javascript
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import BookList from './components/BookList';
import './App.css';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  return user ? children : <Navigate to="/login" />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/books"
            element={
              <ProtectedRoute>
                <BookList />
              </ProtectedRoute>
            }
          />
          <Route path="/" element={<Navigate to="/dashboard" />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
```

### Step 12: Add Basic CSS

Create/Update `src/App.css`:

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f5f5;
}

/* Auth Pages */
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.auth-card {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.auth-card h2 {
  margin-bottom: 30px;
  text-align: center;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #555;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.btn-primary {
  width: 100%;
  padding: 12px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 10px;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-primary:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.auth-link {
  text-align: center;
  margin-top: 20px;
}

.auth-link a {
  color: #007bff;
  text-decoration: none;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 20px;
}

/* Dashboard */
.navbar {
  background-color: #007bff;
  color: white;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-links {
  display: flex;
  gap: 20px;
  align-items: center;
}

.nav-links a {
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-links a:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.btn-logout {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.dashboard-content {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.dashboard-card {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  color: inherit;
  transition: transform 0.3s;
}

.dashboard-card:hover {
  transform: translateY(-5px);
}

.dashboard-card h3 {
  margin-bottom: 10px;
  color: #007bff;
}

/* Book List */
.book-list-container {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.book-list-header {
  margin-bottom: 30px;
}

.book-list-controls {
  display: flex;
  gap: 20px;
  margin-top: 20px;
  flex-wrap: wrap;
}

.search-bar {
  display: flex;
  gap: 10px;
  flex: 1;
  min-width: 300px;
}

.search-input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.search-btn {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.ordering-select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

/* Book Card */
.book-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.book-card-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 15px;
}

.book-card-header h3 {
  flex: 1;
  margin-right: 10px;
}

.book-status {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  background-color: #28a745;
  color: white;
}

.book-author {
  color: #666;
  margin-bottom: 10px;
}

.book-isbn {
  font-size: 14px;
  color: #999;
  margin-bottom: 10px;
}

.book-copies {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
  font-size: 14px;
}

.book-card-footer {
  display: flex;
  gap: 10px;
}

.btn-secondary {
  padding: 8px 16px;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

/* Pagination */
.pagination {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  margin-top: 40px;
}

.pagination-info {
  color: #666;
  font-size: 14px;
}

.pagination-controls {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
}

.pagination-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.pagination-btn:hover:not(:disabled) {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.pagination-btn.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Loading */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #007bff;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
```

---

## Quick Start Summary

1. **Initialize Project**: `npx create-react-app library-frontend`
2. **Install Dependencies**: `npm install axios react-router-dom`
3. **Create API Service**: Set up `src/services/api.js` with all API functions
4. **Create Auth Context**: Set up authentication state management
5. **Create Components**: Build reusable components (Pagination, BookCard, etc.)
6. **Create Pages**: Build Login, Signup, Dashboard, and List pages
7. **Add Routing**: Set up protected routes in App.js
8. **Style**: Add CSS for a polished UI

## Testing the Frontend

1. Start the backend server: `python manage.py runserver`
2. Start the frontend: `npm start`
3. Open `http://localhost:3000`
4. Sign up a new user or login
5. Navigate to Books page to see paginated list

## Next Steps

- Add form validation
- Implement CRUD operations (Create, Update, Delete)
- Add book issue/return functionality
- Implement member management
- Add category management
- Create overdue reports page
- Add book recommendations feature

---

**Note**: Make sure CORS is enabled on your Django backend. Add this to `settings.py`:

```python
INSTALLED_APPS = [
    # ... existing apps
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ... existing middleware
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

And install: `pip install django-cors-headers`

