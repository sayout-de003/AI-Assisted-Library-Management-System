from rest_framework.viewsets import ModelViewSet
from apps.library.models import Book, Category, Member
from .serializers import BookSerializer, CategorySerializer, MemberSerializer
from rest_framework.permissions import IsAuthenticated

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at', 'id')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["title", "author", "isbn"]


class MemberViewSet(ModelViewSet):
    queryset = Member.objects.all().order_by('-created_at', 'id')
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]
