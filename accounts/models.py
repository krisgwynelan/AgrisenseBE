from django.db import models
from django.contrib.auth.models import User

class PasswordResetOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - OTP: {self.otp}"

class SensorReading(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    ph = models.FloatField()
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()

    def __str__(self):
        return f"Sensor Reading at {self.timestamp}"

class DailySummary(models.Model):
    date = models.DateField(unique=True)
    temperature = models.FloatField()
    ph = models.FloatField()
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()

    def __str__(self):
        return f"Daily Summary for {self.date}"
