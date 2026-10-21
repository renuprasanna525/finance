import hmac
import os

from decimal import Decimal

from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import (
    BankAccount,
    Bill,
    Budget,
    ExpenseCategory,
    FinanceSummary,
    SmartInsight,
    TopSpending,
    Transaction,
)


@require_GET
def finance_summary_api(request):
    # The API must not operate without a configured secret.
    api_key = os.environ.get("FINTRACK_API_KEY")

    if not api_key:
        return JsonResponse(
            {"error": "API authentication is not configured."},
            status=503,
        )

    # Authenticate the calling server.
    authorization = request.headers.get("Authorization", "")
    scheme, separator, supplied_key = authorization.partition(" ")

    if (
        scheme.lower() != "bearer"
        or not separator
        or not hmac.compare_digest(supplied_key, api_key)
    ):
        return JsonResponse(
            {"error": "Authentication required."},
            status=401,
        )

    # Calculate totals from actual transaction records.
    total_income = Transaction.objects.filter(transaction_type="Income").aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0")

    total_expenses = Transaction.objects.filter(transaction_type="Expense").aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0")

    return JsonResponse(
        {
            "currency": "INR",
            "total_income": str(total_income),
            "total_expenses": str(total_expenses),
            "net_balance": str(total_income - total_expenses),
            "scope": "all_time",
        }
    )


@require_GET
def finance_transactions_api(request):
    # Authenticate the calling server.
    api_key = os.environ.get("FINTRACK_API_KEY")

    if not api_key:
        return JsonResponse(
            {"error": "API authentication is not configured."},
            status=503,
        )

    authorization = request.headers.get("Authorization", "")
    scheme, separator, supplied_key = authorization.partition(" ")

    if (
        scheme.lower() != "bearer"
        or not separator
        or not hmac.compare_digest(supplied_key, api_key)
    ):
        return JsonResponse(
            {"error": "Authentication required."},
            status=401,
        )

    # Return up to 100 most recent transactions.
    records = Transaction.objects.all().order_by("-transaction_date", "-id")[:100]

    transactions = [
        {
            "id": item.id,
            "title": item.title,
            "category": item.category,
            "transaction_type": item.transaction_type,
            "amount": str(item.amount),
            "payment_method": item.payment_method,
            "transaction_date": str(item.transaction_date),
            "icon": item.icon.url if item.icon else None,
        }
        for item in records
    ]

    return JsonResponse(
        {
            "count": len(transactions),
            "transactions": transactions,
            "limit": 100,
        }
    )


@require_GET
def finance_bills_api(request):
    # Authenticate the calling server.
    api_key = os.environ.get("FINTRACK_API_KEY")

    if not api_key:
        return JsonResponse(
            {"error": "API authentication is not configured."},
            status=503,
        )

    authorization = request.headers.get("Authorization", "")
    scheme, separator, supplied_key = authorization.partition(" ")

    if (
        scheme.lower() != "bearer"
        or not separator
        or not hmac.compare_digest(supplied_key, api_key)
    ):
        return JsonResponse(
            {"error": "Authentication required."},
            status=401,
        )

    # Return up to 100 bills, ordered by due date.
    records = Bill.objects.all().order_by("due_date", "id")[:100]

    bills = [
        {
            "id": item.id,
            "title": item.title,
            "amount": str(item.amount),
            "due_date": str(item.due_date),
            "status": item.status,
            "category": item.category,
            "bill_number": item.bill_number,
            "icon": item.icon.url if item.icon else None,
        }
        for item in records
    ]

    return JsonResponse(
        {
            "count": len(bills),
            "bills": bills,
            "limit": 100,
        }
    )


@require_GET
def finance_budgets_api(request):
    # Authenticate the calling server.
    api_key = os.environ.get("FINTRACK_API_KEY")

    if not api_key:
        return JsonResponse(
            {"error": "API authentication is not configured."},
            status=503,
        )

    authorization = request.headers.get("Authorization", "")
    scheme, separator, supplied_key = authorization.partition(" ")

    if (
        scheme.lower() != "bearer"
        or not separator
        or not hmac.compare_digest(supplied_key, api_key)
    ):
        return JsonResponse(
            {"error": "Authentication required."},
            status=401,
        )

    # Return up to 100 budgets, ordered by most recent start date.
    records = Budget.objects.all().order_by("-start_date", "-id")[:100]

    budgets = [
        {
            "id": item.id,
            "name": item.name,
            "start_date": str(item.start_date),
            "end_date": str(item.end_date),
            "spent": str(item.spent),
            "limit": str(item.limit),
            "status": item.status,
            "remaining": str(item.remaining),
            "used_percentage": item.used_percentage,
        }
        for item in records
    ]

    return JsonResponse(
        {
            "count": len(budgets),
            "budgets": budgets,
            "limit": 100,
        }
    )


@require_GET
def finance_accounts_api(request):
    api_key = os.environ.get("FINTRACK_API_KEY")

    if not api_key:
        return JsonResponse(
            {"error": "API authentication is not configured."},
            status=503,
        )

    authorization = request.headers.get("Authorization", "")
    scheme, separator, supplied_key = authorization.partition(" ")

    if (
        scheme.lower() != "bearer"
        or not separator
        or not hmac.compare_digest(supplied_key, api_key)
    ):
        return JsonResponse(
            {"error": "Authentication required."},
            status=401,
        )

    records = BankAccount.objects.all().order_by("bank_name", "id")[:100]

    accounts = [
        {
            "id": item.id,
            "bank_name": item.bank_name,
            "account_type": item.account_type,
            "account_category": item.account_category,
            "account_id": (
                f"****{str(item.account_id)[-4:]}" if item.account_id else None
            ),
            "balance": str(item.balance),
        }
        for item in records
    ]

    return JsonResponse(
        {
            "count": len(accounts),
            "accounts": accounts,
            "limit": 100,
        }
    )


@require_GET
def finance_reports_api(request):
    api_key = os.environ.get("FINTRACK_API_KEY")

    if not api_key:
        return JsonResponse(
            {"error": "API authentication is not configured."},
            status=503,
        )

    authorization = request.headers.get("Authorization", "")
    scheme, separator, supplied_key = authorization.partition(" ")

    if (
        scheme.lower() != "bearer"
        or not separator
        or not hmac.compare_digest(supplied_key, api_key)
    ):
        return JsonResponse(
            {"error": "Authentication required."},
            status=401,
        )

    summaries = [
        {
            "title": item.title,
            "amount": item.amount,
            "subtitle": item.subtitle,
            "icon": item.icon,
            "color": item.color,
        }
        for item in FinanceSummary.objects.all()[:4]
    ]

    categories = [
        {
            "id": item.id,
            "name": item.name,
            "amount": str(item.amount),
            "percentage": item.percentage,
            "category_type": item.category_type,
            "color": item.color,
            "icon": item.icon.url if item.icon else None,
        }
        for item in ExpenseCategory.objects.all()
    ]

    top_spendings = [
        {
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "amount": str(item.amount),
            "spending_date": str(item.spending_date),
            "image": item.image.url if item.image else None,
        }
        for item in TopSpending.objects.all()[:5]
    ]

    insight = SmartInsight.objects.first()
    insights = None

    if insight:
        insights = {
            "title": insight.title,
            "point_1": insight.point_1,
            "point_2": insight.point_2,
            "point_3": insight.point_3,
        }

    return JsonResponse(
        {
            "summaries": summaries,
            "categories": categories,
            "top_spendings": top_spendings,
            "insights": insights,
        }
    )
