from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import AdminAccount, Student

admin.site.unregister(User)


@admin.register(Student)
class StudentAdmin(UserAdmin):
    list_display = ("student_name", "student_id", "email")
    list_display_links = ("student_name",)
    search_fields = ("first_name", "username", "email")
    list_filter = ()
    ordering = ("first_name",)

    @admin.display(description="Name", ordering="first_name")
    def student_name(self, obj):
        return obj.first_name or "-"

    @admin.display(description="Student ID", ordering="username")
    def student_id(self, obj):
        return obj.username

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