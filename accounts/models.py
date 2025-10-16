from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings  # ✅ use settings.AUTH_USER_MODEL for FK


# -----------------------------
# 1️⃣ Custom User Model
# -----------------------------
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


# -----------------------------
# 2️⃣ Password Reset OTP
# -----------------------------
class PasswordResetOTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.email} - {self.otp}"


# -----------------------------
# 3️⃣ Sensor Reading
# -----------------------------
class SensorReading(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    ph = models.FloatField()
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()

    def __str__(self):
        return f"Sensor Reading at {self.timestamp}"


# -----------------------------
# 4️⃣ Daily Summary
# -----------------------------
class DailySummary(models.Model):
    date = models.DateField(unique=True)
    temperature = models.FloatField()
    ph = models.FloatField()
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()

    def __str__(self):
        return f"Daily Summary for {self.date}"
