from django.db import models

# Create your models here.
from django.db import models
from apps.core.models import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

from django.db import models
from apps.core.models import BaseModel
from transformers import AutoTokenizer, AutoModel
import torch

class Book(BaseModel):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    total_copies = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField()
    embedding = models.BinaryField(null=True, blank=True)  # store serialized embedding



class Member(BaseModel):
    name = models.CharField(max_length=255)
    membership_id = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class BookIssue(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    member = models.ForeignKey(Member, on_delete=models.PROTECT)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    @property
    def is_overdue(self):
        return self.return_date is None and self.due_date < models.functions.Now()
