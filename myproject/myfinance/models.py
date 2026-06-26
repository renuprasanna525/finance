from django.db import models


class FinanceSummary(models.Model):
    title = models.CharField(max_length=100)
    amount = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)  # FontAwesome class
    color = models.CharField(max_length=30)  # purple, green, red, yellow

    def __str__(self):
        return self.title


class UpcomingBill(models.Model):
    icon = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    due_text = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title


class ExpenseBreakdown(models.Model):
    CATEGORY_COLORS = (
        ("#3B5BDB", "Blue"),
        ("#8B5CF6", "Purple"),
        ("#F43F5E", "Pink"),
        ("#F4B000", "Yellow"),
        ("#10B981", "Green"),
    )

    category = models.CharField(max_length=100)
    percentage = models.PositiveIntegerField()
    color = models.CharField(max_length=20, choices=CATEGORY_COLORS)
    center_image = models.ImageField(upload_to="expense_center/", blank=True, null=True)

    def __str__(self):
        return f"{self.category} ({self.percentage}%)"


class RecentActivity(models.Model):
    image = models.ImageField(upload_to="recent_activity/")
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=100)
    amount = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class RecentTransaction(models.Model):
    image = models.ImageField(upload_to="transactions/")
    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    TRANSACTION_TYPES = (
        ("income", "Income"),
        ("expense", "Expense"),
    )

    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_TYPES, default="expense"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ("Income", "Income"),
        ("Expense", "Expense"),
    )

    PAYMENT_METHODS = (
        ("UPI", "UPI"),
        ("Bank Transfer", "Bank Transfer"),
        ("Card", "Card"),
        ("Cash", "Cash"),
    )

    title = models.CharField(max_length=200)

    category = models.CharField(max_length=100)

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_method = models.CharField(
        max_length=30, choices=PAYMENT_METHODS, blank=True, null=True
    )

    transaction_date = models.DateField()

    icon = models.ImageField(upload_to="transactions/", blank=True, null=True)

    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-transaction_date"]

    def __str__(self):
        return self.title


# Bills Page
class Bill(models.Model):
    STATUS_CHOICES = (
        ("Paid", "Paid"),
        ("Pending", "Pending"),
        ("Expired", "Expired"),
    )

    title = models.CharField(max_length=200)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    due_date = models.DateField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    category = models.CharField(max_length=100, blank=True, null=True)

    bill_number = models.CharField(max_length=50, blank=True, null=True)

    # Upload image/icon from admin panel
    icon = models.ImageField(upload_to="bills/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["due_date"]

    def __str__(self):
        return self.title


# Reports Page
class ExpenseCategory(models.Model):
    CATEGORY_CHOICES = (
        ("food", "Food"),
        ("shopping", "Shopping"),
        ("bills", "Bills & Utilities"),
        ("transport", "Transportation"),
        ("entertainment", "Entertainment"),
    )

    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="expense_categories/")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    percentage = models.PositiveIntegerField()
    category_type = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, unique=True
    )

    class Meta:
        ordering = ["-percentage"]

    def __str__(self):
        return self.name

    @property
    def color(self):
        colors = {
            "food": "#f43f5e",
            "shopping": "#f97316",
            "bills": "#e11d48",
            "transport": "#9333ea",
            "entertainment": "#3b82f6",
        }
        return colors.get(self.category_type, "#6366f1")


class TopSpending(models.Model):
    image = models.ImageField(upload_to="top_spending/")
    name = models.CharField(max_length=150, default="Unknown")
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    spending_date = models.DateField()

    class Meta:
        ordering = ["-amount"]

    def __str__(self):
        return self.name


class SmartInsight(models.Model):
    title = models.CharField(max_length=200)
    point_1 = models.CharField(max_length=255)
    point_2 = models.CharField(max_length=255, blank=True)
    point_3 = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title


# Budgets Page:
class Budget(models.Model):
    STATUS_CHOICES = (
        ("near_limit", "Near Limit"),
        ("safe", "Safe"),
    )

    image = models.ImageField(upload_to="budgets/")
    name = models.CharField(max_length=150)

    start_date = models.DateField()
    end_date = models.DateField()

    spent = models.DecimalField(max_digits=10, decimal_places=2)
    limit = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="safe")

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.name

    @property
    def remaining(self):
        return self.limit - self.spent

    @property
    def used_percentage(self):
        if self.limit > 0:
            return round((self.spent / self.limit) * 100)
        return 0

    @property
    def progress_class(self):
        if self.status == "near_limit":
            return "near-limit-fill"
        return "safe-fill"

    @property
    def progress_width(self):
        return f"progress-{self.used_percentage}"


# Accounts Page
class AccountSummary(models.Model):
    title = models.CharField(max_length=100)
    amount = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)  # FontAwesome class
    color = models.CharField(max_length=30)  # green, red, purple, yellow

    class Meta:
        verbose_name_plural = "Account Summaries"

    def __str__(self):
        return self.title


class BankAccount(models.Model):
    image = models.ImageField(upload_to="bank_accounts/")
    bank_name = models.CharField(max_length=150)

    ACCOUNT_CHOICES = (
        ("Savings Account", "Savings Account"),
        ("Current Account", "Current Account"),
        ("Salary Account", "Salary Account"),
    )
    ACCOUNT_CATEGORY = (
        ("bank", "Bank Accounts"),
        ("upi", "UPI"),
        ("credit", "Credit Cards"),
    )

    account_type = models.CharField(
        max_length=50, choices=ACCOUNT_CHOICES, default="Savings Account"
    )
    account_category = models.CharField(
        max_length=20,
        choices=ACCOUNT_CATEGORY,
        default="bank"
    )

    account_id = models.CharField(max_length=20, help_text="Example: XXXXXXXX12")

    balance = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ["bank_name"]

    def __str__(self):
        return self.bank_name
