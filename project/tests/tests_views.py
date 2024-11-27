from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from crm.models import FinancialData, TransactionRecord


class ViewTests(TestCase):
    def setUp(self):
        # Criar usuário para autenticação
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        
        # URLs
        self.dashboard_url = reverse("dashboard")
        self.update_value_url = reverse("update_value")
        self.subtract_value_url = reverse("subtract_value")
        self.clear_transactions_url = reverse("clear_transactions")

    def test_homepage_view(self):
        response = self.client.get(reverse("homepage"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "crm/index.html")

    def test_register_view(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "crm/register.html")

    def test_my_login_view(self):
        response = self.client.get(reverse("my_login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "crm/my_login.html")

    def test_dashboard_view_authenticated_user(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "crm/dashboard_new.html")

    def test_dashboard_view_calculations(self):
        FinancialData.objects.create(
            user=self.user, monthly_income=Decimal("5000.00"), monthly_expense=Decimal("2000.00")
        )
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.context["difference"], Decimal("3000.00"))
        self.assertEqual(response.context["percentage"], Decimal("60.00"))

    def test_update_value_view(self):
        response = self.client.post(
            self.update_value_url,
            {"monthlyEarnings": "1000.00", "description": "Bonus"}
        )
        self.assertRedirects(response, self.dashboard_url)
        financial_data = FinancialData.objects.get(user=self.user)
        self.assertEqual(financial_data.monthly_income, Decimal("1000.00"))
        self.assertEqual(TransactionRecord.objects.count(), 1)

    def test_subtract_value_view(self):
        response = self.client.post(
            self.subtract_value_url,
            {"monthlyExpense": "500.00", "description": "Rent"}
        )
        self.assertRedirects(response, self.dashboard_url)
        financial_data = FinancialData.objects.get(user=self.user)
        self.assertEqual(financial_data.monthly_expense, Decimal("500.00"))
        self.assertEqual(TransactionRecord.objects.count(), 1)

    def test_clear_transactions_view(self):
        FinancialData.objects.create(user=self.user, monthly_income=Decimal("1000.00"))
        TransactionRecord.objects.create(
            user=self.user, amount=Decimal("1000.00"), transaction_type="income"
        )
        response = self.client.post(self.clear_transactions_url)
        self.assertRedirects(response, self.dashboard_url)
        self.assertEqual(FinancialData.objects.filter(user=self.user).count(), 0)
        self.assertEqual(TransactionRecord.objects.filter(user=self.user).count(), 0)

    def test_user_logout_view(self):
        response = self.client.get(reverse("user_logout"))
        self.assertRedirects(response, reverse("homepage"))
