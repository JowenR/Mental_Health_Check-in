from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import SignUpForm


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data["identifier"]
            user = User.objects.create_user(
                username=identifier,
                email=identifier if "@" in identifier else "",
                password=form.cleaned_data["password"],
            )
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form})