from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class FinancialData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    monthly_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateField(default=timezone.now)
    description = models.TextField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} - Income: {self.monthly_income} Expense: {self.monthly_expense} Date: {self.date}"


class TransactionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(
        max_length=10, choices=[("income", "Income"), ("expense", "Expense")]
    )
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type.capitalize()} - {self.amount} - {self.date}"
