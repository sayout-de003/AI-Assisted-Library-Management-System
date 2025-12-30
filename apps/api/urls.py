from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from .views import (
    SignupAPI,
    LogoutAPIView,
    RequestManagementAPIView,
    ApproveManagementRequestAPIView,
    RejectManagementRequestAPIView,
    IssueBookAPIView,
    ReturnBookAPIView,
    OverdueReportAPIView,
    BookRecommendationAPIView,
)
from .viewsets import BookViewSet, CategoryViewSet, MemberViewSet

router = DefaultRouter()
router.register("books", BookViewSet)
router.register("categories", CategoryViewSet)
router.register("members", MemberViewSet)

# Custom login view with AllowAny permission
class PublicTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

# Custom refresh view with AllowAny permission
class PublicTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

urlpatterns = [
    # Auth
    path("auth/signup/", SignupAPI.as_view(), name="signup"),
    path("auth/login/", PublicTokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", PublicTokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", LogoutAPIView.as_view(), name="logout"),

    # Management
    path("management/request/", RequestManagementAPIView.as_view(), name="management-request"),
    path("management/approve/<int:request_id>/", ApproveManagementRequestAPIView.as_view(), name="management-approve"),
    path("management/reject/<int:request_id>/", RejectManagementRequestAPIView.as_view(), name="management-reject"),

    # Book issue/return & reports
    path("books/issue/", IssueBookAPIView.as_view(), name="issue-book"),
    path("books/return/<int:issue_id>/", ReturnBookAPIView.as_view(), name="return-book"),
    path("reports/overdue/", OverdueReportAPIView.as_view(), name="overdue-report"),
    path("books/recommend/<int:member_id>/", BookRecommendationAPIView.as_view(), name="book-recommendation"),

    # ViewSets
    path("", include(router.urls)),
]
