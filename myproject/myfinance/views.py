from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import *
from decimal import Decimal
from django.db.models import Sum, Q
from datetime import date


def dashboard(request):
    summaries = FinanceSummary.objects.all()[:4]

    bills = UpcomingBill.objects.all()
    expense_data = ExpenseBreakdown.objects.all()
    activities = RecentActivity.objects.all()
    recent_transactions = RecentTransaction.objects.all()

    context = {
        "summaries": summaries,
        "bills": bills,
        "expense_data": expense_data,
        "activities": activities,
        "recent_transactions": recent_transactions,
    }

    return render(request, "myfinance/dashboard.html", context)


def delete_transaction(request, id):
    transaction = get_object_or_404(Transaction, id=id)

    transaction.delete()

    messages.success(request, "Transaction deleted successfully.")

    return redirect("transactions")


def transactions(request):

    search = request.GET.get("search", "")
    transaction_type = request.GET.get("type", "All")

    transactions_list = Transaction.objects.all()
    if search:
        transactions_list = transactions_list.filter(
            Q(title__icontains=search)
            | Q(category__icontains=search)
            | Q(notes__icontains=search)
            | Q(payment_method__icontains=search)
        )

    if transaction_type != "All":
        transactions_list = transactions_list.filter(transaction_type=transaction_type)

    total_income = Transaction.objects.filter(transaction_type="Income").aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0")

    total_expenses = Transaction.objects.filter(transaction_type="Expense").aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0")

    net_balance = total_income - total_expenses

    summaries = [
        {
            "title": "Total Income",
            "amount": f"₹{total_income:,.2f}",
            "subtitle": "Money received",
            "icon": "fa-solid fa-arrow-trend-up",
            "color": "green",
        },
        {
            "title": "Total Expenses",
            "amount": f"₹{total_expenses:,.2f}",
            "subtitle": "Money spent",
            "icon": "fa-solid fa-arrow-trend-down",
            "color": "red",
        },
        {
            "title": "Net Balance",
            "amount": f"₹{net_balance:,.2f}",
            "subtitle": "Current balance",
            "icon": "fa-solid fa-wallet",
            "color": "purple",
        },
    ]

    context = {
        "summaries": summaries,
        "transactions": transactions_list,
        "search": search,
    }

    return render(request, "myfinance/transactions.html", context)


def bills(request):

    total_bills = Bill.objects.aggregate(total=Sum("amount"))["total"] or Decimal("0")

    paid_this_month = Bill.objects.filter(
        status="Paid",
        due_date__year=date.today().year,
        due_date__month=date.today().month,
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0")

    pending_bills = Bill.objects.filter(status="Pending").aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0")
    bills_list = Bill.objects.all()

    summaries = [
        {
            "title": "Total Bills",
            "amount": f"₹{total_bills:,.0f}",
            "subtitle": "Current balance",
            "icon": "fa-solid fa-indian-rupee-sign",
            "color": "purple",
        },
        {
            "title": "Paid This Month",
            "amount": f"₹{paid_this_month:,.0f}",
            "subtitle": "All time income",
            "icon": "fa-regular fa-envelope-open",
            "color": "green",
        },
        {
            "title": "Pending Bills",
            "amount": f"₹{pending_bills:,.0f}",
            "subtitle": "All time expenses",
            "icon": "fa-solid fa-circle-exclamation",
            "color": "red",
        },
    ]

    context = {
        "summaries": summaries,
        "bills_list": bills_list,
    }

    return render(request, "myfinance/bills.html", context)


def reports(request):
    summaries = FinanceSummary.objects.all()[:4]
    categories = ExpenseCategory.objects.all()
    top_spendings = TopSpending.objects.all()[:5]
    insights = SmartInsight.objects.first()

    context = {
        "summaries": summaries,
        "categories": categories,
        "top_spendings": top_spendings,
        "insights": insights,
    }
    return render(request, "myfinance/reports.html", context)


def budgets(request):

    budgets = Budget.objects.all()

    context = {
        "budgets": budgets,
    }

    return render(
        request,
        "myfinance/budgets.html",
        context,
    )


def delete_budget(request, id):

    budget = get_object_or_404(Budget, id=id)

    if request.method == "POST":
        budget.delete()
        messages.success(request, "Budget deleted successfully.")

    return redirect("budgets")


def accounts(request):

    summaries = AccountSummary.objects.all()

    account_sections = [
        {
            "title": "Bank Accounts",
            "icon": "fa-solid fa-building-columns",
            "accounts": BankAccount.objects.filter(account_category="bank"),
        },
        {
            "title": "UPI",
            "icon": "fa-solid fa-mobile-screen-button",
            "accounts": BankAccount.objects.filter(account_category="upi"),
        },
        {
            "title": "Credit Cards",
            "icon": "fa-regular fa-credit-card",
            "accounts": BankAccount.objects.filter(account_category="credit"),
        },
    ]

    context = {
        "summaries": summaries,
        "account_sections": account_sections,
    }

    return render(
        request,
        "myfinance/accounts.html",
        context,
    )


def delete_account(request, id):

    account = get_object_or_404(BankAccount, id=id)

    if request.method == "POST":
        account.delete()
        messages.success(request, "Account deleted successfully.")

    return redirect("accounts")


def settings(request):
    return render(request, "myfinance/settings.html")


# Log out Success Page
def logged_out(request):
    return render(request, "myfinance/logged_out.html")


def login_page(request):
    return render(request, "myfinance/login.html")


def signup_page(request):
    return render(request, "myfinance/signup.html")


def income_source(request):
    return render(request, "myfinance/income_source.html")


def monthly_income(request):
    return render(request, "myfinance/monthly_income.html")


def manage_money(request):
    return render(request, "myfinance/manage_money.html")


def first_account(request):
    return render(request, "myfinance/first_account.html")


def first_budget(request):
    return render(request, "myfinance/first_budget.html")


def first_bill(request):
    return render(request, "myfinance/first_bill.html")
