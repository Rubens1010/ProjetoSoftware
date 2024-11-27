from django.test import TestCase
from django.contrib.auth.models import User
from crm.models import FinancialData, TransactionRecord
from decimal import Decimal
from django.utils import timezone


class FinancialDataModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.financial_data = FinancialData.objects.create(
            user=self.user,
            monthly_income=Decimal("5000.00"),
            monthly_expense=Decimal("2000.00"),
            description="Monthly financial data",
        )

    def test_financial_data_creation(self):
        self.assertEqual(self.financial_data.user, self.user)
        self.assertEqual(self.financial_data.monthly_income, Decimal("5000.00"))
        self.assertEqual(self.financial_data.monthly_expense, Decimal("2000.00"))
        self.assertEqual(self.financial_data.description, "Monthly financial data")
        self.assertEqual(self.financial_data.date, timezone.now().date())

    def test_financial_data_default_values(self):
        financial_data = FinancialData.objects.create(user=self.user)
        self.assertEqual(financial_data.monthly_income, Decimal("0.00"))
        self.assertEqual(financial_data.monthly_expense, Decimal("0.00"))
        self.assertEqual(financial_data.description, "")

    def test_financial_data_str_representation(self):
        expected_str = "testuser - Income: 5000.00 Expense: 2000.00 Date: {}".format(
            self.financial_data.date
        )
        self.assertEqual(str(self.financial_data), expected_str)


class TransactionRecordModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.transaction = TransactionRecord.objects.create(
            user=self.user,
            amount=Decimal("1500.00"),
            transaction_type="income",
            description="Salary payment",
        )

    def test_transaction_record_creation(self):
        self.assertEqual(self.transaction.user, self.user)
        self.assertEqual(self.transaction.amount, Decimal("1500.00"))
        self.assertEqual(self.transaction.transaction_type, "income")
        self.assertEqual(self.transaction.description, "Salary payment")
        self.assertEqual(self.transaction.date.date(), timezone.now().date())

    def test_transaction_record_default_values(self):
        transaction = TransactionRecord.objects.create(
            user=self.user,
            amount=Decimal("100.00"),
            transaction_type="expense",
        )
        self.assertEqual(transaction.description, "")

    def test_transaction_record_str_representation(self):
        expected_str = "testuser - Income - 1500.00 - {}".format(
            self.transaction.date
        )
        self.assertEqual(str(self.transaction), expected_str)
