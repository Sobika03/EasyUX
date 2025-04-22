from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from core.models import Organization

class CustomUser(AbstractUser):
    organization = models.ForeignKey(Organization, blank=True, null=True, on_delete=models.PROTECT)
    must_change_password = models.BooleanField(default=False)

    # Set related_name to avoid clash with the default User model
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Change this to a unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Change this to a unique related_name
        blank=True
    )

    def __str__(self):
        return self.username


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_days = models.PositiveIntegerField()  # e.g. 30 for monthly, 365 for yearly
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

from django.utils.timezone import now, timedelta

class Subscription(models.Model):
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField()

    def is_active(self):
        return self.end_date >= now()

    def __str__(self):
        return f"{self.organization.name} - {self.plan.name}"