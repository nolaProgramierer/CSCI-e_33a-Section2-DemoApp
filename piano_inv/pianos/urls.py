from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_piano", views.add_piano, name="add_piano"),
]
