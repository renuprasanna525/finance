from django.urls import path
from . import views, api_views

urlpatterns = [
    path("", views.login_page, name="login"),
    path("signup/", views.signup_page, name="signup"),
    path("income-source/", views.income_source, name="income_source"),
    path("monthly-income/", views.monthly_income, name="monthly_income"),
    path("manage-money/", views.manage_money, name="manage_money"),
    path("first-account/", views.first_account, name="first_account"),
    path("first-budget/", views.first_budget, name="first_budget"),
    path("first-bill/", views.first_bill, name="first_bill"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("transactions/", views.transactions, name="transactions"),
    path("bills/", views.bills, name="bills"),
    path("reports/", views.reports, name="reports"),
    path("budgets/", views.budgets, name="budgets"),
    path("accounts/", views.accounts, name="accounts"),
    path("settings/", views.settings, name="settings"),
    # Logout Success Page
    path("logged-out/", views.logged_out, name="logged_out"),
    # urls.py
    path(
        "transaction/delete/<int:id>/",
        views.delete_transaction,
        name="delete_transaction",
    ),
    path(
        "budgets/delete/<int:id>/",
        views.delete_budget,
        name="delete_budget",
    ),
    path(
        "accounts/delete/<int:id>/",
        views.delete_account,
        name="delete_account",
    ),
    path(
        "api/finance/summary/",
        api_views.finance_summary_api,
        name="finance_summary_api",
    ),
    path(
        "api/finance/transactions/",
        api_views.finance_transactions_api,
        name="finance_transactions_api",
    ),
    path(
        "api/finance/bills/",
        api_views.finance_bills_api,
        name="finance_bills_api",
    ),
    path(
        "api/finance/budgets/",
        api_views.finance_budgets_api,
        name="finance_budgets_api",
    ),
    path(
        "api/finance/accounts/",
        api_views.finance_accounts_api,
        name="finance_accounts_api",
    ),
    path(
        "api/finance/reports/",
        api_views.finance_reports_api,
        name="finance_reports_api",
    ),
]
