from datetime import date, time

from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Appointment

User = get_user_model()

# Edit these to your clinic hours
SLOT_TIMES = [time(h) for h in (9, 10, 11, 13, 14, 15, 16)]


def get_counselors():
    return User.objects.filter(is_active=True, is_staff=True).order_by("first_name", "username")


def get_available_slots(counselor, day):
    """Slots for this counselor on this day: not booked, not in the past."""
    if day < date.today():
        return []

    taken = set(
        Appointment.objects.filter(counselor=counselor, date=day)
        .exclude(status=Appointment.Status.CANCELLED)
        .values_list("time", flat=True)
    )

    now = timezone.localtime()
    slots = []
    for t in SLOT_TIMES:
        if t in taken:
            continue
        if day == now.date() and t <= now.time():
            continue
        slots.append(t)
    return slots


class AppointmentForm(forms.Form):
    counselor = forms.ModelChoiceField(queryset=User.objects.none())
    date = forms.DateField()
    time = forms.TimeField(input_formats=["%H:%M"])
    notes = forms.CharField(required=False)

    def __init__(self, *args, student=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.student = student
        self.fields["counselor"].queryset = get_counselors()

    def clean_date(self):
        d = self.cleaned_data["date"]
        if d < date.today():
            raise forms.ValidationError("You can't book a past date.")
        return d

    def clean(self):
        data = super().clean()
        counselor, d, t = data.get("counselor"), data.get("date"), data.get("time")

        if counselor and d and t:
            if t not in get_available_slots(counselor, d):
                raise forms.ValidationError("That time slot is no longer available.")

            student_conflict = (
                Appointment.objects.filter(student=self.student, date=d, time=t)
                .exclude(status=Appointment.Status.CANCELLED)
                .exists()
            )
            if student_conflict:
                raise forms.ValidationError("You already have an appointment at that time.")
        return data