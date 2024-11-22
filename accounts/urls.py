from django.urls import path
from .views import signup, login_session, logout_session

urlpatterns = [
    path('', signup, name='sginup'),
    path('login_session/', login_session, name='login_session'),
    path('logout_session/', logout_session, name='logout_session')
]
