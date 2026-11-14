from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, SignUpForm
from .models import CounselorProfile, StudentProfile


class RoleLoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.get_redirect_url()
        if next_url:
            return next_url
        if self.request.user.is_staff:
            return reverse("admin_home")
        return reverse("student_home")


class ChangePasswordView(SuccessMessageMixin, auth_views.PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = "/profile/"  # back to the profile page, where the toast shows
    success_message = "Password changed successfully!"


def signup(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("admin_home")
        return redirect("student_home")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["student_id"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["name"],
            )
            login(request, user)
            return redirect("student_home")
    else:
        form = SignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


def is_valid_facebook_url(url):
    """Accept only http(s) links on facebook.com / fb.com / fb.me (blocks javascript: etc.)."""
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    allowed = ("facebook.com", "fb.com", "fb.me")
    return parsed.scheme in ("http", "https") and any(
        host == d or host.endswith("." + d) for d in allowed
    )


@login_required
def profile(request):
    user = request.user

    # Each role gets its own extra details
    counselor = None
    student = None
    if user.is_staff:
        counselor, _ = CounselorProfile.objects.get_or_create(user=user)
    else:
        student, _ = StudentProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        fb_url = request.POST.get("facebook_url", "").strip()

        # Validate everything first, so nothing is saved if something is wrong
        if not name or not email:
            messages.error(request, "Name and email cannot be empty.")
        elif User.objects.filter(email__iexact=email).exclude(pk=user.pk).exists():
            messages.error(request, "That email is already used by another account.")
        elif student and fb_url and not is_valid_facebook_url(fb_url):
            messages.error(
                request,
                "Please enter a valid Facebook link, like https://facebook.com/your.name",
            )
        else:
            # student_id / username is intentionally NOT updated here
            user.first_name = name
            user.email = email
            user.save()

            if counselor:
                counselor.specialization = request.POST.get("specialization", "").strip()[:120]
                counselor.office_location = request.POST.get("office_location", "").strip()[:120]
                counselor.contact_number = request.POST.get("contact_number", "").strip()[:30]
                counselor.save()
            elif student:
                student.course = request.POST.get("course", "").strip()[:120]
                student.year_level = request.POST.get("year_level", "").strip()[:30]
                student.contact_number = request.POST.get("contact_number", "").strip()[:30]
                student.facebook_url = fb_url
                student.save()

            messages.success(request, "Profile updated!")
        return redirect(request.path)

    return render(
        request,
        "accounts/profile.html",
        {"counselor": counselor, "student": student},
    )


MOODS = [
    {"key": "great", "label": "Great", "img": "icons/moods/great.svg", "color": "#22c55e"},
    {"key": "good",  "label": "Good",  "img": "icons/moods/good.svg",  "color": "#84cc16"},
    {"key": "okay",  "label": "Okay",  "img": "icons/moods/okay.svg",  "color": "#eab308"},
    {"key": "bad",   "label": "Bad",   "img": "icons/moods/bad.svg",   "color": "#f97316"},
    {"key": "awful", "label": "Awful", "img": "icons/moods/awful.svg", "color": "#ef4444"},
]


@login_required
def student_home(request):
    return render(request, "pages/students/student_home.html", {"moods": MOODS})


def check_in(request):
    return render(request, "pages/students/check_in.html")


def appointments(request):
    return render(request, "pages/students/appointments.html")


def resources(request):
    return render(request, "pages/students/resources.html")


def admin_users(request):
    User = get_user_model()
    students = (
        User.objects.filter(is_staff=False)
        .order_by("first_name", "last_name", "username")
        .prefetch_related("appointments__counselor")
    )
    return render(request, "pages/admin/users.html", {"students": students})