from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_piano", views.add_piano, name="add_piano"),
    path("piano_detail/<str:brand>/<str:finish>/<int:price>", views.piano_detail, name="piano_detail"),
    path("edit_piano/<str:brand>/<str:finish>/<int:price>", views.edit_piano, name="edit_piano"),
    path("remove_piano/<str:brand>/<str:finish>/<int:price>", views.remove_piano, name="remove_piano"),
]
