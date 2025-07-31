# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """Custom user with avatar image."""
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    # (Username, email, etc are inherited from AbstractUser)
    def __str__(self):
        return self.get_full_name() or self.username

class Drink(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price_pence = models.PositiveIntegerField(help_text="Price in pence")  # e.g. 150 for £1.50
    color = models.CharField(max_length=7, help_text="HTML colour code (e.g. #RRGGBB)")

    def __str__(self):
        return self.name

class Session(models.Model):
    name = models.CharField(max_length=100, blank=True, help_text="Session name or description")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    drinks = models.ManyToManyField(Drink, related_name='sessions', help_text="Drinks available this session")

    def __str__(self):
        if self.end_time:
            return f"Session {self.id} ({self.start_time.date()} – {self.end_time.date()})"
        else:
            return f"Session {self.id} (active since {self.start_time.date()})"

    def is_active(self):
        return self.end_time is None

class Consumption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consumptions')
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='consumptions')
    timestamp = models.DateTimeField(default=timezone.now)
    price_pence = models.PositiveIntegerField(help_text="Price (in pence) at time of consumption")

    def __str__(self):
        return f"{self.user} had a {self.drink.name} on {timezone.localtime(self.timestamp).strftime('%Y-%m-%d %H:%M')}"
