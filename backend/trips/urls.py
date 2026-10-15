from django.urls import path

from .views import HealthView, PlanTripView

urlpatterns = [
    path("plan/", PlanTripView.as_view()),
    path("health/", HealthView.as_view()),
]
