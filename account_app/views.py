from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from transaction_app.views import get_balance
from transaction_app.models import transactionModel
from book_app.models import BorrowModel

# Create your views here.
def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        else:
            form = SignupForm()
        return render(request,'account_app/signup.html',{'form':form})
    else:
        return redirect('profile')



def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data = request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request,user)
                    messages.success(request,"Logged in successfully.")
                    return redirect('profile')
        else:
            form = AuthenticationForm()
        return render(request,'account_app/login.html',{'form':form})
    else:
        return redirect('profile')



@never_cache
@login_required
def user_logout(request):
    if  request.user.is_authenticated:
        logout(request)
        return redirect('login')


@never_cache
@login_required
def profile(request):
    if request.user.is_authenticated:
      user_transactions = transactionModel.objects.filter(user = request.user).order_by('created_at')
      borrows = BorrowModel.objects.filter(user=request.user, returned_at__isnull=True)
      borrows_history = BorrowModel.objects.filter(user=request.user).order_by('-borrowed_at')
      balance = get_balance(request.user)
      
      return render(request,'account_app/profile.html',{
          'balance':balance,
          'transactions':user_transactions,
          'borrows_history': borrows_history,
          'borrows':borrows
          })
    
    else:
        return redirect('login')