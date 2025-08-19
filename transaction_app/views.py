from django.shortcuts import render, redirect
from .forms import DepositForm
from .models import transactionModel
from django.db.models import Sum
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required


# Create your views here.
def get_balance(user):
    deposits = transactionModel.objects.filter(
        user=user, transaction_type='DEPOSIT'
    ).aggregate(total=Sum('amount'))['total'] or 0

    borrows = transactionModel.objects.filter(
        user=user, transaction_type='BORROW'
    ).aggregate(total=Sum('amount'))['total'] or 0

    returns = transactionModel.objects.filter(
        user=user, transaction_type='RETURN'
    ).aggregate(total=Sum('amount'))['total'] or 0

    balance = deposits + returns + borrows   

    return balance


@login_required
def deposit(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = DepositForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)   # form এর ডাটা দিয়ে object তৈরি করে, কিন্তু save করে না database-এ এখনই।
                transaction.user = request.user         # Login user set করলাম karon form থেকে user বাদ দিয়েছো ,,multiple user ache bole
                transaction.save()                      # এখন database-এ save করলাম
                send_mail(
                    subject="Deposit Successful",
                    message=f"Hello {request.user.username},\n\nYou have successfully deposited ${transaction.amount} into your account.\n\nThank you for using our service!",
                    from_email=settings.EMAIL_HOST_USER,   
                    recipient_list=[request.user.email],    
                    fail_silently=False,
                )
                messages.success(request, 'Deposited money successfully. A confirmation email has been sent to your mail.')
                return redirect('profile')
        else:
            form = DepositForm()
        return render(request,'transactions/deposit.html',{'form':form})
    else:
        return redirect('login')

