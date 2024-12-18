from decimal import Decimal

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.shortcuts import redirect, render
from django.utils import timezone

from crm.forms import CreateUserForm, FinancialDataForm, LoginForm
from crm.models import FinancialData, TransactionRecord


def homepage(request):
    return render(request, "crm/index.html")


def finance(request):
    return render(request, "crm/finance.html")


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("my_login")

    context = {"registerform": form}
    return render(request, "crm/register.html", context=context)


def my_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")

    context = {"loginform": form}
    return render(request, "crm/my_login.html", context=context)

@login_required(login_url="my_login")
def dashboard(request):
    financial_data, created = FinancialData.objects.get_or_create(user=request.user)
    form = FinancialDataForm(request.POST or None, instance=financial_data)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("dashboard")

    monthly_earnings = financial_data.monthly_income or Decimal("0.00")
    monthly_expense = financial_data.monthly_expense or Decimal("0.00")
    difference = monthly_earnings - monthly_expense

    # Calcula a porcentagem da diferença em relação aos ganhos
    if monthly_earnings != 0:  # Evitar divisão por zero
        percentage = (difference / monthly_earnings) * 100
    else:
        percentage = Decimal("0.00")  # Definir como 0 se não houver ganhos

    transactions = TransactionRecord.objects.filter(user=request.user).order_by("-date")

    context = {
        "form": form,
        "monthly_earnings": monthly_earnings,
        "monthly_expense": monthly_expense,
        "difference": difference,
        "percentage": percentage,
        "transactions": transactions,
    }

    return render(request, "crm/dashboard_new.html", context)


@login_required(login_url="my_login")
def update_value(request):
    if request.method == "POST":
        financial_data, created = FinancialData.objects.get_or_create(user=request.user)
        new_earnings = Decimal(request.POST.get("monthlyEarnings"))
        description = request.POST.get("description", "")

        current_earnings = financial_data.monthly_income or Decimal("0.00")
        financial_data.monthly_income = current_earnings + new_earnings
        financial_data.date = request.POST.get("date", timezone.now().date())
        financial_data.save()

        # Criar o registro do extrato
        TransactionRecord.objects.create(
            user=request.user,
            amount=new_earnings,
            transaction_type="income",
            description=description,
        )

    return redirect("dashboard")


@login_required(login_url="my_login")
def subtract_value(request):
    if request.method == "POST":
        financial_data, created = FinancialData.objects.get_or_create(user=request.user)
        new_expense = Decimal(request.POST.get("monthlyExpense"))
        description = request.POST.get("description", "")
        current_expense = financial_data.monthly_expense or Decimal("0.00")
        financial_data.monthly_expense = current_expense + new_expense
        financial_data.date = request.POST.get("date", timezone.now().date())
        financial_data.save()

        TransactionRecord.objects.create(
            user=request.user,
            amount=new_expense,
            transaction_type="expense",
            description=description,
        )
    return redirect("dashboard")


@login_required(login_url="my_login")
def clear_transactions(request):
    if request.method == "POST":
        # Exclui todas as transações para o usuário autenticado
        FinancialData.objects.filter(user=request.user).delete()
        TransactionRecord.objects.filter(user=request.user).delete()
        return redirect("dashboard")


def user_logout(request):
    auth.logout(request)
    return redirect("")
