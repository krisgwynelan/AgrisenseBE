from django.urls import path
from . import views
from .views import store_sensor_reading, store_daily_summary


urlpatterns = [
    path('register/', views.register_user),
    path('login/', views.login_user),
    path('request-reset/', views.send_reset_otp),
    path('verify-otp/', views.verify_otp),
    path('reset-password/', views.reset_password),

   path('store-reading/', store_sensor_reading, name='store_sensor_reading'),
   path('store-daily-summary/', store_daily_summary, name='store_daily_summary'),
]