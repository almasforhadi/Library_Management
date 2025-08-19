from django.shortcuts import render, redirect, get_object_or_404
from .models import BookModel, BorrowModel, ReviewModel
from .forms import ReviewForm
from transaction_app.views import get_balance
from transaction_app.models import transactionModel
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def review(request, book_id):
    book = get_object_or_404(BookModel, pk=book_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)   # DB te save hoye jabe na ekhane
            review.user = request.user         # current user set korchi
            review.book = book                 # book bind korchi
            review.save()                      # ekhon save hobe
            return redirect('home')
    else:
        form = ReviewForm()

    return render(request, 'book_app/review.html', {'form': form,'book': book})   



def details(request, id):
    book_item = BookModel.objects.get(pk=id)
    all_comments = ReviewModel.objects.all()
    return render(request, 'book_app/details.html', {'book': book_item,'all_comments':all_comments})


@login_required
def borrow(request, id):
    if request.user.is_autenticated:
        book = BookModel.objects.get(pk=id)
        balance = get_balance(request.user)

        if balance < book.price:
            messages.error(request,'You dont have enough balance to borrow this book.')
            return render(request,'book_app/details.html',{'book': book})
        
        transactionModel.objects.create(
            user=request.user,
            transaction_type='BORROW',
            amount=-book.price       # subtract instead of add
        )
        BorrowModel.objects.create(user = request.user, book = book)
        send_mail(
            subject='Borrowing book!',
            message=f'Welcome! "{book.title}"  is borrowed successfully.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email], 
            fail_silently=False
        )
        messages.success(request,f'Borrowing book "{book.title}" request is successfully executed')
        return redirect('profile')
    else:
        return redirect('login')



@login_required
def return_book(request,id):
     borrow = BorrowModel.objects.get(pk=id)
     if borrow.returned_at:
         return redirect('profile')
     #create return transaction
     transactionModel.objects.create(
        user=request.user,
        transaction_type='RETURN',
        amount=borrow.book.price
    )
     # Mark as returned
     borrow.returned_at = timezone.now()
     borrow.save()
     return redirect('profile')