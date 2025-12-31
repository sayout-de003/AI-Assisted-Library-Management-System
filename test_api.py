import requests
from django.contrib.auth import get_user_model
import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_lms.settings")
django.setup()

User = get_user_model()

# Test user details
EMAIL = "testuser@example.com"
PASSWORD = "TestPassword123"

# 1. Check if the user exists, else create it
if User.objects.filter(email=EMAIL).exists():
    user = User.objects.get(email=EMAIL)
    print("User already exists:", user.email)
else:
    user = User.objects.create_user(email=EMAIL, password=PASSWORD)
    user.is_active = True
    user.save()
    print("User created:", user.email)

# 2. Login via API
login_url = "http://127.0.0.1:8000/api/auth/login/"
login_data = {"email": EMAIL, "password": PASSWORD}
login_resp = requests.post(login_url, json=login_data)

if login_resp.status_code == 200:
    tokens = login_resp.json()
    access_token = tokens.get("access")
    print("Login successful, access token:", access_token)
else:
    print("Login failed:", login_resp.status_code, login_resp.text)
    exit(1)

# 3. Test /api/members/me/ endpoint
members_url = "http://127.0.0.1:8000/api/members/me/"
headers = {"Authorization": f"Bearer {access_token}"}
members_resp = requests.get(members_url, headers=headers)

if members_resp.status_code == 200:
    print("Members endpoint response:", members_resp.json())
else:
    print("Members endpoint failed:", members_resp.status_code, members_resp.text)
