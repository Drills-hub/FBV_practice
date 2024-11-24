from django.urls import path
from .views import (
    signup,
    login_session,
    logout_session,
    login_jwt,
    logout_jwt,
    token_refresh,
    user_delete,
    user_password,
    user_update,
    user_profile,
)

urlpatterns = [
    path("", signup, name="sginup"),
    path("login_session/", login_session, name="login_session"),
    path("logout_session/", logout_session, name="logout_session"),
    path("login_jwt/", login_jwt, name="login_jwt"),
    path("logout_jwt/", logout_jwt, name="logout_jwt"),
    path("token_refresh/", token_refresh, name='token_refresh'),
    path("user_delete/", user_delete, name="user_delete"),
    path("user_password/", user_password, name="user_password/"),
    path("user_update/<str:username>/", user_update, name="user_update"),
    path("profile/<str:username>/", user_profile, name="user_profile"),
]
