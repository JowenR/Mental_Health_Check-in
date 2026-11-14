from django.urls import path
from . import views

urlpatterns = [
    path("", views.appointments, name="appointments"),
    path("slots/", views.available_slots, name="appointment_slots"),
]