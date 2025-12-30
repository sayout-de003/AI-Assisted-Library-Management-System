# /Users/sayantande/websoft/scripts/seed_data.py

import os
import django
import pickle
from sentence_transformers import SentenceTransformer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_lms.settings")
django.setup()  # MUST be called before importing models

from apps.library.models import Category, Book
from apps.users.models import User, MemberProfile

# optional: embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Seed categories
categories = ["Science Fiction", "Fantasy", "History", "Technology", "Mathematics"]
for cat_name in categories:
    Category.objects.get_or_create(name=cat_name)

# Seed books
books_data = [
    {"title": "Dune", "author": "Frank Herbert", "isbn": "9780441013593", "category": "Science Fiction", "total_copies": 5},
    {"title": "Foundation", "author": "Isaac Asimov", "isbn": "9780553293357", "category": "Science Fiction", "total_copies": 3},
    {"title": "Harry Potter and the Sorcerer's Stone", "author": "J.K. Rowling", "isbn": "9780590353427", "category": "Fantasy", "total_copies": 7},
    {"title": "Sapiens", "author": "Yuval Noah Harari", "isbn": "9780062316097", "category": "History", "total_copies": 4},
    {"title": "Clean Code", "author": "Robert C. Martin", "isbn": "9780132350884", "category": "Technology", "total_copies": 2},
    {"title": "Principles of Mathematical Analysis", "author": "Walter Rudin", "isbn": "9780070542358", "category": "Mathematics", "total_copies": 2},
]

for book_data in books_data:
    cat = Category.objects.get(name=book_data["category"])
    book, created = Book.objects.get_or_create(
        title=book_data["title"],
        author=book_data["author"],
        isbn=book_data["isbn"],
        category=cat,
        defaults={"total_copies": book_data["total_copies"], "available_copies": book_data["total_copies"]},
    )
    # embeddings
    emb = model.encode(book.title + " " + book.author)
    book.embedding = pickle.dumps(emb)
    book.save()

# Seed members
members_data = [
    {"email": "alice@example.com", "name": "Alice"},
    {"email": "bob@example.com", "name": "Bob"},
    {"email": "charlie@example.com", "name": "Charlie"},
]

for mem_data in members_data:
    user, created = User.objects.get_or_create(
        email=mem_data["email"],
        defaults={"name": mem_data["name"], "role": User.Role.MEMBER, "is_active": True, "is_staff": False},
    )
    MemberProfile.objects.get_or_create(user=user)

print("Seed data completed successfully.")
