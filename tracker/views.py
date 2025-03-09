from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TrackingHistory, CurrentBalance
from decimal import Decimal


def index(request):
    if request.method == "POST":
        description = request.POST.get("description", "").strip()
        amount_str = request.POST.get("amount", "").strip()

        # Validate description
        if not description:
            messages.warning(request, "Description is required.")
            return redirect("index")

        # Validate amount
        if not amount_str:
            messages.warning(request, "Amount is required.")
            return redirect("index")

        try:
            amount = Decimal(amount_str)  # ✅ Convert directly to Decimal
        except ValueError:
            messages.warning(request, "Enter a valid numeric amount.")
            return redirect("index")

        # Get or create the current balance
        current_balance, _ = CurrentBalance.objects.get_or_create(id=1)

        # Determine transaction type
        expense_type = "Debit" if amount < 0 else "Credit"

        # Save the tracking history
        TrackingHistory.objects.create(
            current_balance=current_balance,
            description=description,
            amount=amount,
            expense_type=expense_type,
        )

        # ✅ Ensure both values are Decimal before updating balance
        current_balance.balance += amount  # Now, both are Decimal
        current_balance.save()

        messages.success(request, "Transaction recorded successfully.")
        return redirect("index")

    return render(request, "tracker/index.html")
