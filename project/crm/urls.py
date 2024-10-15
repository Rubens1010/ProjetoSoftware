from django.urls import path

from . import views


urlpatterns = [
    path("", views.homepage, name=""),
    path("register", views.register, name="register"),
    path("my_login", views.my_login, name="my_login"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("update_value", views.update_value, name="update_value"),
    path("subtract_value", views.subtract_value, name="subtract_value"),
    path("user-logout", views.user_logout, name="user-logout"),
    path("clear_transactions/", views.clear_transactions, name="clear_transactions"),
    path("finance/", views.finance, name="finance"),
]
