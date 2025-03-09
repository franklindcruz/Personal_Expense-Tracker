from django.db import models

# Create your models here.


class CurrentBalance(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Current Balance: {self.balance}"


class TrackingHistory(models.Model):
    current_balance = models.ForeignKey(CurrentBalance, on_delete=models.CASCADE)
    expense_type = models.CharField(
        max_length=200, choices=[("Credit", "Credit"), ("Debit", "Debit")]
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.expense_type}: {self.amount}  - {self.description}"
            if self.description
            else f"{self.expense_type}: {self.amount}"
        )
