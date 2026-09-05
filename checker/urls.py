from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("medicine/", views.medicine_lookup, name="medicine_lookup"),
    path("interaction/", views.interaction_check, name="interaction_check"),
]
