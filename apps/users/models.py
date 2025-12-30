from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models, transaction
from apps.core.models import TimeStampedModel
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        LIBRARIAN = "LIBRARIAN", "Librarian"
        MEMBER = "MEMBER", "Member"

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self):
        return self.email


class MemberProfile(TimeStampedModel):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="member_profile"
    )

    member_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    def save(self, *args, **kwargs):
        if not self.member_id:
            with transaction.atomic():
                last = (
                    MemberProfile.objects
                    .select_for_update()
                    .order_by("-id")
                    .values_list("member_id", flat=True)
                    .first()
                )
                number = int(last.split("-")[1]) + 1 if last else 1
                self.member_id = f"MEM-{number:06d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.member_id


class ManagementProfile(TimeStampedModel):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="management_profiles"
    )

    role = models.CharField(
        max_length=20,
        choices=User.Role.choices
    )

    management_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    def save(self, *args, **kwargs):
        if self.role not in [User.Role.ADMIN, User.Role.LIBRARIAN]:
            raise ValueError("Invalid management role")

        if not self.management_id:
            prefix = "ADM" if self.role == User.Role.ADMIN else "LIB"

            with transaction.atomic():
                last = (
                    ManagementProfile.objects
                    .select_for_update()
                    .filter(management_id__startswith=prefix)
                    .order_by("-id")
                    .values_list("management_id", flat=True)
                    .first()
                )
                number = int(last.split("-")[1]) + 1 if last else 1
                self.management_id = f"{prefix}-{number:06d}"

        super().save(*args, **kwargs)


class ManagementRequest(TimeStampedModel):

    class Status(models.TextChoices):
        PENDING = "PENDING"
        APPROVED = "APPROVED"
        REJECTED = "REJECTED"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="management_requests"
    )

    requested_role = models.CharField(
        max_length=20,
        choices=User.Role.choices
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    approved_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="approved_management_requests"
    )
