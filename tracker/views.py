from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TrackingHistory, CurrentBalance
from decimal import Decimal
from django.db.models import Sum, F
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db import IntegrityError


def register_view(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not all([username, first_name, last_name, email, password]):
            messages.warning(request, "All fields are required.")
            return redirect("register")

        # Check if user with the given email or username exists
        if User.objects.filter(Q(email=email) | Q(username=username)).exists():
            messages.warning(
                request, "A user with that email or username already exists."
            )
            return redirect("register")

        try:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
        except IntegrityError:
            messages.error(
                request,
                "An error occurred while creating your account. Please try again.",
            )
            return render(
                request,
                "tracker/register.html",
                {
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                },
            )

        login(request, user)
        messages.success(request, "Account created successfully.")
        return redirect("index")

    return render(request, "tracker/register.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        # Check for empty fields
        if not email or not password:
            messages.warning(request, "All fields are required.")
            return redirect("login")

        # Get the user by email
        user = User.objects.filter(email=email).first()

        # Check if the user exists
        if not user:
            messages.error(
                request, "No account exists with this email. Please register."
            )
            return redirect("login")

        # Authenticate the user (Django's authenticate function uses username, not email)
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("index")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("login")

    return render(request, "tracker/login.html")


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")


@login_required(login_url="login")
def index(request):
    if request.method == "POST":
        description = request.POST.get("description").strip()
        amount_str = request.POST.get("amount").strip()
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
        messages.success(request, "Transaction deleted successfully.")

        # Check if any transactions exist
        if not TrackingHistory.objects.exists():
            # Reset balance to zero if all transactions are deleted
            current_balance.balance = Decimal("0.00")
            current_balance.save()

    return redirect("index")


def all_transactions(request):
    transactions = TrackingHistory.objects.all().order_by("-created_at")
    context = {"transactions": transactions}
    return render(request, "tracker/all_transactions.html", context)
