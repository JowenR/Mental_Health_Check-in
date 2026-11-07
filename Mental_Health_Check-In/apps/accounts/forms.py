from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm

INPUT_CLASSES = (
    "w-full h-[50px] px-[18px] rounded-[10px] border-[1.5px] border-ink "
    "font-form text-sm text-ink placeholder:text-ink/60 "
    "focus:outline-none focus:ring-4 focus:ring-indigo-800/20"
)
class SignUpForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your name",
            "class": INPUT_CLASSES,
            "autocomplete": "name",
        }),
    )
    identifier = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your email or student number",
            "class": INPUT_CLASSES,
            "autocomplete": "username",
        }),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "class": INPUT_CLASSES,
            "autocomplete": "new-password",
        }),
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm Password",
            "class": INPUT_CLASSES,
            "autocomplete": "new-password",
        }),
    )

    def clean_identifier(self):
        value = self.cleaned_data["identifier"].strip().lower()
        if User.objects.filter(username__iexact=value).exists():
            raise forms.ValidationError("This account already exists.")
        return value

    def clean_name(self):
        return " ".join(self.cleaned_data["name"].split())

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get("password")
        confirm = cleaned.get("confirm_password")

        if pw and confirm and pw != confirm:
            self.add_error("confirm_password", "Passwords do not match.")
        elif pw:
            try:
                validate_password(pw)
            except forms.ValidationError as e:
                self.add_error("password", e)
        return cleaned

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Email or Student ID",
            "class": INPUT_CLASSES,
            "autocomplete": "username",
        }),
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "class": INPUT_CLASSES,
            "autocomplete": "current-password",
        }),
    )

    def clean_username(self):
        return self.cleaned_data["username"].strip().lower()