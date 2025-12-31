import requests

BASE_URL = "http://127.0.0.1:8000/api"  # Change to your backend URL
USERNAME = "testuser@example.com"
PASSWORD = "testpassword"

def login():
    url = f"{BASE_URL}/token/"
    data = {"email": USERNAME, "password": PASSWORD}
    resp = requests.post(url, data=data)
    if resp.status_code != 200:
        raise Exception(f"Login failed: {resp.status_code} {resp.text}")
    token = resp.json().get("access")
    if not token:
        raise Exception("Access token not found in response.")
    print("Login successful. Access token acquired.")
    return token

def test_get_me(headers):
    url = f"{BASE_URL}/members/me/"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"GET /members/me/ failed: {resp.status_code} {resp.text}")
    data = resp.json()
    required_keys = {"id", "name", "membership_id", "email", "is_active"}
    missing = required_keys - data.keys()
    if missing:
        raise Exception(f"GET /members/me/ missing keys: {missing}")
    print("GET /members/me/ passed.")

def test_books(headers):
    url = f"{BASE_URL}/books/"
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"GET /books/ failed: {resp.status_code} {resp.text}")
    data = resp.json()
    if "results" not in data:
        raise Exception("GET /books/ response missing 'results'")
    if not isinstance(data["results"], list):
        raise Exception("GET /books/ 'results' is not a list")
    print(f"GET /books/ passed. Total books: {len(data['results'])}")

def test_issue_return(headers, book_id):
    # Issue book
    url = f"{BASE_URL}/books/{book_id}/issue/"
    resp = requests.post(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"Issue book {book_id} failed: {resp.status_code} {resp.text}")
    print(f"Book {book_id} issued successfully.")

    # Return book
    url = f"{BASE_URL}/books/{book_id}/return/"
    resp = requests.post(url, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"Return book {book_id} failed: {resp.status_code} {resp.text}")
    print(f"Book {book_id} returned successfully.")

if __name__ == "__main__":
    token = login()
    headers = {"Authorization": f"Bearer {token}"}

    try:
        test_get_me(headers)
        test_books(headers)
        # Pick a sample book_id to test issue/return
        sample_book_id = 1
        test_issue_return(headers, sample_book_id)
        print("All tests passed successfully!")
    except Exception as e:
        print("TEST FAILED:", e)
