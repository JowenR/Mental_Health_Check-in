from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import AdminAccount, Student

admin.site.unregister(User)


@admin.register(Student)
class StudentAdmin(UserAdmin):
    list_display = ("username", "first_name", "email", "is_active", "date_joined")
    list_filter = ("is_active",)

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=False)

    def save_model(self, request, obj, form, change):
        obj.is_staff = False
        obj.is_superuser = False
        super().save_model(request, obj, form, change)


@admin.register(AdminAccount)
class AdminAccountAdmin(UserAdmin):
    list_display = ("username", "first_name", "email", "is_superuser", "is_active")
    list_filter = ("is_superuser", "is_active")

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=True)

    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        super().save_model(request, obj, form, change)