from django.db import transaction
from apps.users.models import User, ManagementRequest, ManagementProfile


from django.core.mail import send_mail
from django.conf import settings

from apps.users.models import ManagementRequest, ManagementProfile


@transaction.atomic
def approve_management_request(*, request_id, approved_by):

    req = (
        ManagementRequest.objects
        .select_for_update()
        .get(id=request_id, status=ManagementRequest.Status.PENDING)
    )

    user = req.user

    user.role = req.requested_role
    user.is_staff = True
    user.save(update_fields=["role", "is_staff"])

    if not ManagementProfile.objects.filter(
        user=user,
        role=req.requested_role
    ).exists():
        ManagementProfile.objects.create(
            user=user,
            role=req.requested_role
        )

    req.status = ManagementRequest.Status.APPROVED
    req.approved_by = approved_by
    req.save(update_fields=["status", "approved_by"])

    # EMAIL NOTIFICATION
    send_mail(
        subject="Management Request Approved",
        message=(
            f"Hello {user.name},\n\n"
            f"Your request for the role '{req.requested_role}' has been approved.\n"
            f"You can now access management features.\n\n"
            "Regards,\nLibrary Admin"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )



@transaction.atomic
def reject_management_request(*, request_id, rejected_by):

    req = (
        ManagementRequest.objects
        .select_for_update()
        .get(id=request_id, status=ManagementRequest.Status.PENDING)
    )

    req.status = ManagementRequest.Status.REJECTED
    req.approved_by = rejected_by
    req.save(update_fields=["status", "approved_by"])


