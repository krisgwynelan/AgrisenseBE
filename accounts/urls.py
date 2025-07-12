from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user),
    path('login/', views.login_user),
    path('request-reset/', views.send_reset_otp),
    path('verify-otp/', views.verify_otp),
    path('reset-password/', views.reset_password),
]
