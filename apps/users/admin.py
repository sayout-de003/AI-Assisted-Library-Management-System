from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

# Import your local models and services
from .models import User, ManagementRequest
from .services import approve_management_request


@admin.action(description="Approve selected management requests")
def approve_selected_requests(modeladmin, request, queryset):
    """
    Admin action to bulk approve management requests.
    """
    approved_count = 0

    for req in queryset:
        if req.status == ManagementRequest.Status.PENDING:
            approve_management_request(
                request_id=req.id,
                approved_by=request.user
            )
            approved_count += 1

    if approved_count > 0:
        messages.success(request, f"{approved_count} management requests approved.")
    else:
        messages.info(request, "No pending requests were selected.")


@admin.register(ManagementRequest)
class ManagementRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "requested_role", "status", "approved_by", "created_at")
    list_filter = ("status", "requested_role")
    actions = [approve_selected_requests]
    
    # Optional: Make these fields read-only in the detailed view to prevent tampering
    readonly_fields = ("created_at",)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """
    Custom User Admin that supports 'email' as the username field
    and displays custom fields like 'role'.
    """
    model = User

    # Controls the columns in the list view
    list_display = (
        "email",
        "name",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
    )

    search_fields = (
        "email",
        "name",
    )

    ordering = ("-created_at",)

    # Layout for the "Change User" page
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("name",)}),
        (
            _("Role & Permissions"),
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "created_at")}),
    )

    # Layout for the "Add User" page
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "password1",
                    "password2",
                    "role",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )

    filter_horizontal = (
        "groups",
        "user_permissions",
    )