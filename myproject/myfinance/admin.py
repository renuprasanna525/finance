from django.contrib import admin
from .models import *

admin.site.register(FinanceSummary)
admin.site.register(UpcomingBill)
admin.site.register(ExpenseBreakdown)
admin.site.register(RecentActivity)
admin.site.register(RecentTransaction)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "transaction_type",
        "amount",
        "category",
        "transaction_date",
    )
    list_display = (
        "title",
        "transaction_type",
        "amount",
        "category",
        "payment_method",
        "transaction_date",
    )

    list_filter = ("transaction_type", "category", "transaction_date", "payment_method")

    search_fields = ("title", "category")


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "bill_number",
        "amount",
        "due_date",
        "status",
        "category",
    )

    list_filter = (
        "status",
        "category",
        "due_date",
    )

    search_fields = (
        "title",
        "bill_number",
        "category",
    )


# Reports page
@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "amount",
        "percentage",
        "category_type",
    )

    list_filter = ("category_type",)

    search_fields = ("name",)


@admin.register(TopSpending)
class TopSpendingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "amount",
        "spending_date",
    )

    search_fields = ("category",)


@admin.register(SmartInsight)
class SmartInsightAdmin(admin.ModelAdmin):
    list_display = ("title",)


# Budgets Page
@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "spent",
        "limit",
        "status",
        "start_date",
        "end_date",
        "get_remaining",
    )

    def get_remaining(self, obj):
        return obj.remaining

    get_remaining.short_description = "Remaining"

    list_filter = ("status",)

    search_fields = ("name",)


# Accounts Page
@admin.register(AccountSummary)
class AccountSummaryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "amount",
        "subtitle",
        "color",
    )

    search_fields = ("title",)


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = (
        "bank_name",
        "account_type",
        "account_category",
        "account_id",
        "balance",
    )

    search_fields = (
        "bank_name",
        "account_id",
    )

    list_filter = ("account_type", "account_category",)
