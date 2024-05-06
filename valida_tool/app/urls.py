from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("validation/<int:validation_id>", views.validation, name="validation"),
    path("guide/<int:validation_id>", views.guide, name="guide")
]