from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TrackingHistory, CurrentBalance
from decimal import Decimal
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.db.models import F


def index(request):
    if request.method == "POST":
        description = request.POST.get("description", "").strip()
        amount_str = request.POST.get("amount", "").strip()
        print(type(amount_str))
        # Validate description
        if not description:
            messages.warning(request, "Description is required.")
            return redirect("index")

        # Validate amount
        if not amount_str:
            messages.warning(request, "Amount is required.")
            return redirect("index")

        try:
            amount = Decimal(amount_str)  # Convert directly to Decimal
        except ValueError:
            messages.warning(request, "Enter a valid numeric amount.")
            return redirect("index")

        # Get or create the current balance
        current_balance, _ = CurrentBalance.objects.get_or_create(id=1)

        # Determine transaction type
        expense_type = "Debit" if amount < 0 else "Credit"

        if amount == 0:
            messages.warning(request, "Amount cannot be zero.")
            return redirect("index")

        # Save the tracking history
        transaction_history = TrackingHistory.objects.create(
            current_balance=current_balance,
            description=description,
            amount=amount,
            expense_type=expense_type,
        )

        #  Ensure both values are Decimal before updating balance
        current_balance.balance += transaction_history.amount  # Now, both are Decimal
        current_balance.save()

        messages.success(request, "Transaction recorded successfully.")
        return redirect("index")

    current_balance, _ = CurrentBalance.objects.get_or_create(id=1)
    income = (
        TrackingHistory.objects.filter(expense_type="Credit").aggregate(Sum("amount"))[
            "amount__sum"
        ]  # this will return a dictionary with the sum of the 'amount' field for transactions with 'expense_type' equal to 'Credit'
        or 0
    )
    expense = (
        TrackingHistory.objects.filter(expense_type="Debit").aggregate(Sum("amount"))[
            "amount__sum"
        ]  # this will return a dictionary with the sum of the 'amount' field for transactions with 'expense_type' equal to 'Debit'
        or 0
    )
    context = {
        "transactions": TrackingHistory.objects.all().order_by("-created_at"),
        "current_balance": current_balance,
        "income": income,
        "expense": expense,
    }
    return render(request, "tracker/index.html", context)


def deleteTransaction(request, id):
    transaction = TrackingHistory.objects.filter(id=id).first()

    if transaction:  # Ensure transaction exists before proceeding
        current_balance, _ = CurrentBalance.objects.get_or_create(id=1)

        # Reduce balance only if it won't go negative
        current_balance.balance = F("balance") - transaction.amount
        current_balance.save()

        # Delete the transaction
        transaction.delete()

        # Check if any transactions exist
        if not TrackingHistory.objects.exists():
            # Reset balance to zero if all transactions are deleted
            current_balance.balance = Decimal("0.00")
            current_balance.save()

    return redirect("index")