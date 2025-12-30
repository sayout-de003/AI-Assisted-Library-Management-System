from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book, Category, Member, BookIssue

admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Member)
admin.site.register(BookIssue)
