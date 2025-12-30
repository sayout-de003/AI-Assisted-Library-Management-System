from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.library.models import Book, Category, BookIssue, Member
from apps.users.models import User, MemberProfile, ManagementRequest
from apps.library.services import issue_book, return_book


class LMSAPITestCase(TestCase):
    def setUp(self):
        # Create a category for books
        self.category = Category.objects.create(name="Fiction")

        # Create a member user
        self.member_user = User.objects.create_user(
            email="member1@example.com",
            name="Member User",
            password="password123",
            role=User.Role.MEMBER
        )
        self.member_profile = MemberProfile.objects.create(user=self.member_user)
        
        # Create a Member object for library operations
        import uuid
        self.member = Member.objects.create(
            name=self.member_user.name,
            email=self.member_user.email,
            membership_id=f"MEM-{uuid.uuid4().hex[:6].upper()}"
        )

        # Create a management user (e.g., librarian)
        self.librarian_user = User.objects.create_user(
            email="librarian@example.com",
            name="Librarian User",
            password="password123",
            role=User.Role.LIBRARIAN
        )
        
        # Create admin user for management request approval
        self.admin_user = User.objects.create_user(
            email="admin@example.com",
            name="Admin User",
            password="password123",
            role=User.Role.ADMIN
        )

        # Setup API client
        self.client = APIClient()

    # Helper to create books
    def _create_dummy_book(self, copies=1):
        import uuid
        return Book.objects.create(
            title="Dummy Book",
            author="Author",
            isbn=f"TEST-{uuid.uuid4().hex[:10]}",
            total_copies=copies,
            available_copies=copies,
            category=self.category
        )

    # Test issuing a book decreases available copies
    def test_issue_book_decrement_available(self):
        book = self._create_dummy_book(copies=5)
        issue = issue_book(book, self.member)
        book.refresh_from_db()
        self.assertEqual(book.available_copies, 4)
        self.assertIsNotNone(issue)

    # Test returning a book increases available copies
    def test_return_book_increment_available(self):
        book = self._create_dummy_book(copies=5)
        issue = issue_book(book, self.member)
        return_book(issue)
        book.refresh_from_db()
        self.assertEqual(book.available_copies, 5)

    # Test that issuing a book with 0 copies raises ValueError
    def test_invalid_issue_when_no_copies(self):
        book = self._create_dummy_book(copies=0)
        with self.assertRaisesMessage(ValueError, "No copies available"):
            issue_book(book, self.member)

    # Test management request creation and approval
    def test_management_request_and_approval(self):
        # Create a management request
        request_obj = ManagementRequest.objects.create(
            user=self.member_user,
            requested_role=User.Role.LIBRARIAN
        )

        # Check request exists
        self.assertEqual(request_obj.status, ManagementRequest.Status.PENDING)

        # Approve the request
        request_obj.status = ManagementRequest.Status.APPROVED
        request_obj.approved_by = self.admin_user
        request_obj.save()

        request_obj.refresh_from_db()
        self.assertEqual(request_obj.status, ManagementRequest.Status.APPROVED)
        self.assertEqual(request_obj.approved_by, self.admin_user)

    # Test book recommendation API endpoint
    def test_book_recommendation(self):
        self.client.force_authenticate(user=self.admin_user)
        book = self._create_dummy_book()
        url = reverse("book-recommendation", kwargs={"member_id": self.member.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)  # Should return a list of books
