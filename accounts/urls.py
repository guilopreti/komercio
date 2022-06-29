from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view()),
    path("accounts/", views.UserView.as_view()),
    path("accounts/newest/<int:num>/", views.ListByDateView.as_view()),
    path("accounts/<pk>/", views.UpdateAccountView.as_view()),
    path("accounts/<pk>/management/", views.ChangeActiveView.as_view()),
]
