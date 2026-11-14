"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from apps.core.decorators import admin_required, student_required
from apps.accounts.views import student_home, check_in, resources
from django.conf import settings
from django.conf.urls.static import static
from appointments import views as appointment_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("student-home/", student_required(student_home), name="student_home"),
    path("check-in/", student_required(check_in), name="check_in"),
    path("appointments/", student_required(appointment_views.appointments), name="appointments"),
    path("appointments/slots/", student_required(appointment_views.available_slots), name="appointment_slots"),
    path("resources/", student_required(resources), name="resources"),
    path("admin-panel/", admin_required(TemplateView.as_view(template_name="pages/admin/admin_home.html")), name="admin_home"),
    path("", include("apps.accounts.urls")),
    path("appointments/<int:pk>/cancel/", student_required(appointment_views.cancel_appointment), name="cancel_appointment"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)