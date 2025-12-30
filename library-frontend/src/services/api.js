import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  headers: { "Content-Type": "application/json" },
  timeout: 10000, // 10 second timeout
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Handle network errors
    if (!error.response) {
      console.error("Network Error:", error.message);
      return Promise.reject(new Error("Network Error: Please check if the backend server is running"));
    }

    // Handle 401 Unauthorized - try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem("refresh_token");
        if (!refreshToken) {
          throw new Error("No refresh token available");
        }

        const response = await axios.post(`${api.defaults.baseURL}/auth/refresh/`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem("access_token", access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (data) => api.post("/auth/login/", data),
  signup: (data) => api.post("/auth/signup/", data),
  logout: (data) => api.post("/auth/logout/", data),
};

export const managementAPI = {
  request: (data) => api.post("/management/request/", data),
};

export const booksAPI = {
  list: (page = 1) => api.get(`/books/?page=${page}`),
};


export const membersAPI = {
    list: () => api.get("/members/"),
    toggleApproval: (id) => api.post(`/members/${id}/toggle_approval/`),
  };
  
  export const categoriesAPI = {
    list: () => api.get("/categories/"),
  };
  
  export const issueAPI = {
    issue: (data) => api.post("/books/issue/", data),
    return: (data) => api.post("/books/return/", data),
  };
  
  export const searchAPI = {
    books: (query) => api.get(`/books/?search=${query}`),
  };
  
export default api;
