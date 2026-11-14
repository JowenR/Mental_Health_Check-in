from django.conf import settings
from django.db import models
from django.db.models import Q


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="appointments"
    )
    counselor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="counselor_appointments"
    )
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "time"]
        constraints = [
            # A counselor can't be double-booked
            models.UniqueConstraint(
                fields=["counselor", "date", "time"],
                condition=~Q(status="cancelled"),
                name="unique_counselor_slot",
            ),
            # A student can't be in two places at the same time
            models.UniqueConstraint(
                fields=["student", "date", "time"],
                condition=~Q(status="cancelled"),
                name="unique_student_slot",
            ),
        ]

    def __str__(self):
        return f"{self.student} with {self.counselor} on {self.date} {self.time}"