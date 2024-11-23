from django.urls import path
from .views import signup, login_session, logout_session, login_jwt, logout_jwt, user_delete

urlpatterns = [
    path("", signup, name="sginup"),
    path("login_session/", login_session, name="login_session"),
    path("logout_session/", logout_session, name="logout_session"),
    path("login_jwt/", login_jwt, name="login_jwt"),
    path("logout_jwt/", logout_jwt, name="logout_jwt"),
    path("user_delete/", user_delete, name="user_delete"),
]
