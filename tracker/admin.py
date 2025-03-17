from django.contrib import admin
from .models import *

# Register your models here.

admin.site.site_header = "Expense Tracker"
admin.site.site_title = "Expense Tracker"
admin.site.site_url = "http://127.0.0.1:8000/"


@admin.action(description="Mark selected transaction as Credit")
def make_credit(modeladmin, request, queryset):
    for q in queryset:
        if q.amount < 0:
            q.amount = q.amount * -1
            q.save()

    queryset.update(expense_type="Credit")


@admin.action(description="Mark selected transaction as Debit")
def make_debit(modeladmin, request, queryset):
    for q in queryset:
        # obj = TrackingHistory.objects.get(id=q.id)
        # if obj.amount > 0:
        #     obj.amount = obj.amount * -1
        #     obj.save()
        if q.amount > 0:
            q.amount = q.amount * -1
            q.save()

    queryset.update(expense_type="Debit")


class TrackingHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "expense_type",
        "amount",
        "current_balance",
        "created_at",
        "display_transaction_status",
    )

    actions = [make_credit, make_debit]

    def display_transaction_status(self, obj):

        if obj.amount < 0:
            return "Negative"
        else:
            return "Positive"

    search_fields = ("description", "expense_type")

    ordering = ["-created_at"]

    list_filter = ("expense_type", "created_at")


admin.site.register(TrackingHistory, TrackingHistoryAdmin)

admin.site.register(CurrentBalance)
