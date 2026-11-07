from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, SignUpForm


class RoleLoginView(auth_views.LoginView):
    template_name = "login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.get_redirect_url()
        if next_url:
            return next_url
        if self.request.user.is_staff:
            return reverse("admin_home")
        return reverse("home")


def signup(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("admin_home")
        return redirect("home")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data["identifier"]
            user = User.objects.create_user(
                username=identifier,
                email=identifier if "@" in identifier else "",
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["name"],
            )
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})