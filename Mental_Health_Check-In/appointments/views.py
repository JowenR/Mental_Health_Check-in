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

@login_required
def admin_appointments(request):
    tab = request.GET.get("tab", "all")
    S = Appointment.Status

    tabs = {
        "all": [S.PENDING, S.CONFIRMED, S.COMPLETED, S.CANCELLED],
        "upcoming": [S.PENDING, S.CONFIRMED],
        "completed": [S.COMPLETED],
        "cancelled": [S.CANCELLED],
    }
    if tab not in tabs:
        tab = "all"

    base = Appointment.objects.select_related("student", "counselor")
    appointments_list = base.filter(status__in=tabs[tab])
    if tab != "upcoming":
        appointments_list = appointments_list.order_by("-date", "-time")

    counts = {name: base.filter(status__in=st).count() for name, st in tabs.items()}

    return render(request, "pages/admin/appointments.html", {
        "appointments": appointments_list,
        "tab": tab,
        "counts": counts,
    })

@login_required
@require_POST
def admin_update_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    S = Appointment.Status

    # action -> (allowed current statuses, new status, success message)
    actions = {
        "confirm": ([S.PENDING], S.CONFIRMED, "Appointment confirmed."),
        "complete": ([S.CONFIRMED], S.COMPLETED, "Appointment marked as completed."),
        "cancel": ([S.PENDING, S.CONFIRMED], S.CANCELLED, "Appointment cancelled."),
        "undo_confirm": ([S.CONFIRMED], S.PENDING, "Confirmation undone. Appointment is Pending again."),
        "undo_complete": ([S.COMPLETED], S.CONFIRMED, "Completion undone. Appointment is Confirmed again."),
    }
    action = actions.get(request.POST.get("action"))

    if action and appointment.status in action[0]:
        appointment.status = action[1]
        appointment.save(update_fields=["status"])
        messages.success(request, action[2])
    else:
        messages.error(request, "That action isn't allowed for this appointment.")

    return redirect(f"{request.path.rsplit('/', 3)[0]}/?tab={request.POST.get('tab', 'upcoming')}")

@login_required
def admin_home(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    recent_appointments = (
        Appointment.objects.select_related("student", "counselor")
        .order_by("-created_at")[:8]
    )

    return render(request, "pages/admin/admin_home.html", {
        "total_users": User.objects.filter(is_staff=False).count(),
        "total_appointments": Appointment.objects.count(),
        "total_checkins": 0,          # TODO: connect to the check-in model
        "recent_appointments": recent_appointments,
        "recent_checkins": [],        # TODO: connect to the check-in model
    })