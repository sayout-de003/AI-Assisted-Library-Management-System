from datetime import timedelta
from django.utils.timezone import now
from django.db import transaction
from .models import Book, BookIssue

FINE_PER_DAY = 5  # simple rule-based automation

@transaction.atomic
def issue_book(book: Book, member):
    if book.available_copies <= 0:
        raise ValueError("No copies available")

    book.available_copies -= 1
    book.save()

    return BookIssue.objects.create(
        book=book,
        member=member,
        due_date=now().date() + timedelta(days=14)
    )


@transaction.atomic
def return_book(issue: BookIssue):
    if issue.return_date:
        raise ValueError("Book already returned")

    issue.return_date = now().date()

    overdue_days = max(0, (issue.return_date - issue.due_date).days)
    issue.fine_amount = overdue_days * FINE_PER_DAY
    issue.save()

    book = issue.book
    book.available_copies += 1
    book.save()

    return issue


from django.core.mail import send_mail

def send_overdue_email(issue):
    send_mail(
        subject="Library Due Date Reminder",
        message=f"{issue.member.name}, please return '{issue.book.title}'.",
        from_email=None,
        recipient_list=[issue.member.email],
        fail_silently=True,
    )


# library_lms/apps/library/services.py

from sentence_transformers import SentenceTransformer
import pickle
import numpy as np
from .models import Book

# Initialize model (singleton)
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_book_embeddings():
    for book in Book.objects.all():
        emb = model.encode(book.title + " " + book.author)
        book.embedding = pickle.dumps(emb)
        book.save()

def recommend_books_for_member(member, top_k=5):
    issued_books = member.bookissue_set.all()
    issued_embeddings = []

    for issue in issued_books:
        if issue.book.embedding:
            emb = pickle.loads(issue.book.embedding)
            issued_embeddings.append(emb)

    if not issued_embeddings:
        return Book.objects.all()[:top_k]  # fallback

    avg_embedding = np.mean(issued_embeddings, axis=0)

    books = Book.objects.exclude(bookissue__member=member)
    scores = []

    for book in books:
        if book.embedding:
            emb = pickle.loads(book.embedding)
            score = np.dot(avg_embedding, emb) / (np.linalg.norm(avg_embedding) * np.linalg.norm(emb))
            scores.append((score, book))

    scores.sort(reverse=True, key=lambda x: x[0])
    recommended_books = [b for s, b in scores[:top_k]]
    return recommended_books
