from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.tokens import RefreshToken




from apps.users.models import ManagementRequest, User
from apps.users.services import approve_management_request,reject_management_request
from apps.users.permissions import IsAdmin
from .serializers import SignupSerializer


class SignupAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Signup successful"}, status=status.HTTP_201_CREATED)


class RequestManagementAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        requested_role = request.data.get("requested_role")

        if requested_role not in [User.Role.ADMIN, User.Role.LIBRARIAN]:
            return Response({"error": "Invalid role request"}, status=400)

        if ManagementRequest.objects.filter(
            user=request.user,
            status=ManagementRequest.Status.PENDING
        ).exists():
            return Response({"error": "Pending request already exists"}, status=400)

        ManagementRequest.objects.create(
            user=request.user,
            requested_role=requested_role
        )

        return Response({"message": "Management request submitted"}, status=201)


class ApproveManagementRequestAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, request_id):
        approve_management_request(
            request_id=request_id,
            approved_by=request.user
        )
        return Response({"message": "Management request approved"}, status=200)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logged out successfully"},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )


class RejectManagementRequestAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, request_id):
        reject_management_request(
            request_id=request_id,
            rejected_by=request.user
        )
        return Response(
            {"message": "Management request rejected"},
            status=status.HTTP_200_OK
        )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from apps.library.models import Book, Member, BookIssue
from apps.library.services import issue_book, return_book
from .serializers import BookIssueSerializer

class IssueBookAPIView(APIView):
    def post(self, request):
        book = Book.objects.get(id=request.data["book_id"])
        member = Member.objects.get(id=request.data["member_id"])

        issue = issue_book(book, member)
        return Response(BookIssueSerializer(issue).data, status=201)


class ReturnBookAPIView(APIView):
    def post(self, request, issue_id):
        issue = BookIssue.objects.get(id=issue_id)
        issue = return_book(issue)
        return Response(BookIssueSerializer(issue).data)


class OverdueReportAPIView(APIView):
    def get(self, request):
        overdue = BookIssue.objects.filter(
            return_date__isnull=True,
            due_date__lt=now().date()
        )
        return Response(BookIssueSerializer(overdue, many=True).data)


from apps.library.services import send_overdue_email

class OverdueReportAPIView(APIView):
    def get(self, request):
        overdue = BookIssue.objects.filter(
            return_date__isnull=True,
            due_date__lt=now().date()
        )

        for issue in overdue:
            send_overdue_email(issue)

        return Response(BookIssueSerializer(overdue, many=True).data)


# library_lms/apps/api/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from apps.library.models import Member
from apps.library.services import recommend_books_for_member
from .serializers import BookSerializer

class BookRecommendationAPIView(APIView):
    def get(self, request, member_id):
        member = Member.objects.get(id=member_id)
        books = recommend_books_for_member(member)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
