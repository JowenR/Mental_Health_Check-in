from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import LoginForm, SignUpForm
from django.contrib import messages


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

@login_required
def profile(request):
    if request.method == "POST":
        user = request.user
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()

        if not name or not email:
            messages.error(request, "Name and email cannot be empty.")
        elif User.objects.filter(email__iexact=email).exclude(pk=user.pk).exists():
            messages.error(request, "That email is already used by another account.")
        else:
            user.first_name = name
            user.email = email
            user.save()
            messages.success(request, "Profile updated!")
        return redirect(request.path)

    return render(request, "accounts/profile.html")
