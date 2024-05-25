from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required


def homepage(request):
    return render(request, "crm/index.html")


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
    # Verifica se o formulário de adição de valor foi enviado
    if request.method == "POST" and "add_value" in request.POST:
        new_income = float(request.POST.get("monthlyIncome"))
        current_earnings = float(request.session.get("monthly_earnings", 0))
        request.session["monthly_earnings"] = current_earnings + new_income

    # Verifica se o formulário de subtração de valor foi enviado
    if request.method == "POST" and "subtract_value" in request.POST:
        new_expense = float(request.POST.get("monthlyExpense"))
        current_balance = float(request.session.get("monthly_balance", 0))
        request.session["monthly_balance"] = current_balance - new_expense

    monthly_earnings = request.session.get("monthly_earnings", 0)
    monthly_balance = request.session.get("monthly_balance", 0)

    # Calcula a diferença entre o valor de entrada e o valor de saída
    difference = monthly_earnings + monthly_balance

    context = {
        "monthly_earnings": monthly_earnings,
        "monthly_balance": monthly_balance,
        "difference": difference,
    }

    return render(request, "crm/dashboard.html", context)


@login_required(login_url="my_login")
def update_value(request):
    if request.method == "POST":
        new_earnings = float(request.POST.get("monthlyEarnings"))
        current_earnings = float(request.session.get("monthly_earnings", 0))
        request.session["monthly_earnings"] = current_earnings + new_earnings
    return redirect("dashboard")


@login_required(login_url="my_login")
def subtract_value(request):
    if request.method == "POST":
        new_expense = float(request.POST.get("monthlyExpense"))
        current_balance = float(request.session.get("monthly_balance", 0))
        request.session["monthly_balance"] = current_balance - new_expense
    return redirect("dashboard")


def user_logout(request):
    auth.logout(request)
    return redirect("")
