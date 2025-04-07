from django.urls import path
from .views import profile_view,login_view,signup_view

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
]