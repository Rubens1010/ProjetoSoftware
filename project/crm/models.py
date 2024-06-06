from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FinancialData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    monthly_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - Income: {self.monthly_income} Expense: {self.monthly_expense} Date: {self.date}"
