from rest_framework import serializers
from apps.users.models import User, MemberProfile

from apps.library.models import Book, Category, Member, BookIssue

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "name", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            name=validated_data["name"]
        )
        MemberProfile.objects.create(user=user)
        return user




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


class BookIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookIssue
        fields = "__all__"
        read_only_fields = ("issue_date", "fine_amount")
