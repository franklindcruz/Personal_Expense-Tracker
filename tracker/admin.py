from django.contrib import admin
from .models import TrackingHistory, CurrentBalance

# Customize the Django admin headers for a more branded experience.
admin.site.site_header = "Expense Tracker"
admin.site.site_title = "Expense Tracker"
admin.site.index_title = "Welcome to Expense Tracker Admin"
admin.site.site_url = "http://127.0.0.1:8000/"

@admin.action(description="Mark selected transaction as Credit")
def make_credit(modeladmin, request, queryset):
    # For each selected transaction, ensure the amount is positive.
    for transaction in queryset:
        if transaction.amount < 0:
            transaction.amount = -transaction.amount
            transaction.save()
    queryset.update(expense_type="Credit")

@admin.action(description="Mark selected transaction as Debit")
def make_debit(modeladmin, request, queryset):
    # For each selected transaction, ensure the amount is negative.
    for transaction in queryset:
        if transaction.amount > 0:
            transaction.amount = -transaction.amount
            transaction.save()
    queryset.update(expense_type="Debit")

@admin.register(TrackingHistory)
class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "expense_type",
        "amount",
        "current_balance",
        "created_at",
        "transaction_status",
    )
    actions = [make_credit, make_debit]
    search_fields = ("description", "expense_type")
    ordering = ["-created_at"]
    list_filter = ("expense_type", "created_at")

    def transaction_status(self, obj):
        """Display whether the transaction is negative or positive."""
        return "Negative" if obj.amount < 0 else "Positive"
    transaction_status.short_description = "Transaction Status"

@admin.register(CurrentBalance)
class CurrentBalanceAdmin(admin.ModelAdmin):
    list_display = ("balance", "created_at")
