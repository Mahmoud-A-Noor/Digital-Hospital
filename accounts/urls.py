from django.urls import path
from .views import profile, login, logout, register, otp_view

app_name = 'accounts'

urlpatterns = [
    path('profile/', profile, name="profile"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('register/', register, name="register"),
    path('otp/', otp_view, name="otp"),
]
