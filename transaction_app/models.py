from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class transactionModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    TYPES = (('DEPOSIT','Deposit'),('BORROW','Borrow'),('RETURN','Return'))
    transaction_type = models.CharField(
        max_length=15,
        choices=TYPES,
        default='DEPOSIT',   # সবসময় deposit হবে
        editable=False       # form/admin এ দেখাবে না, সবসময় deposit save হবে
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.transaction_type