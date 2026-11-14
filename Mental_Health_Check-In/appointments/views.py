from datetime import date, datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import AppointmentForm, get_available_slots, get_counselors
from .models import Appointment


@login_required
def appointments(request):
    form = AppointmentForm(request.POST or None, student=request.user)

    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                Appointment.objects.create(
                    student=request.user,
                    counselor=form.cleaned_data["counselor"],
                    date=form.cleaned_data["date"],
                    time=form.cleaned_data["time"],
                    notes=form.cleaned_data["notes"],
                    status=Appointment.Status.PENDING,
                )
        except IntegrityError:
            form.add_error(None, "Sorry, that slot was just taken. Please pick another.")
        else:
            messages.success(request, "Appointment booked! Status: Pending.")
            return redirect("appointments")

    upcoming = (
        Appointment.objects.filter(student=request.user, date__gte=date.today())
        .exclude(status=Appointment.Status.CANCELLED)
        .select_related("counselor")
    )

    return render(request, "pages/students/appointments.html", {
        "form": form,
        "counselors": get_counselors(),
        "today": date.today().isoformat(),
        "upcoming": upcoming,
    })


@login_required
def available_slots(request):
    try:
        counselor = get_counselors().get(pk=request.GET.get("counselor"))
        day = datetime.strptime(request.GET.get("date", ""), "%Y-%m-%d").date()
    except (ValueError, TypeError, get_counselors().model.DoesNotExist):
        return JsonResponse({"slots": []})

    slots = [
        {"value": t.strftime("%H:%M"), "label": t.strftime("%I:%M %p").lstrip("0")}
        for t in get_available_slots(counselor, day)
    ]
    return JsonResponse({"slots": slots})

@login_required
@require_POST
def cancel_appointment(request, pk):
    # Only the student who booked it can cancel it
    appointment = get_object_or_404(Appointment, pk=pk, student=request.user)

    if appointment.status in (Appointment.Status.CANCELLED, Appointment.Status.COMPLETED):
        messages.error(request, "This appointment can no longer be cancelled.")
    else:
        appointment.status = Appointment.Status.CANCELLED
        appointment.save(update_fields=["status"])
        messages.success(request, "Your appointment has been cancelled.")

    return redirect("appointments")