from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("article/<int:pk>/", views.detail, name="detail"),
    path("article/<int:pk>/edit/", views.edit, name="edit"),
    path("article/<int:pk>/delete/", views.delete, name="delete"),

    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout_view"),
]
