from django.shortcuts import render, redirect
from book_app.models import category_model, BookModel

# Create your views here.

def home(request, category_slug = None):
    all_categories = category_model.objects.all()
    all_books = BookModel.objects.all()

    filtered_books = None

    if category_slug:
       fetch_category =  category_model.objects.get(slug = category_slug)
       filtered_books = BookModel.objects.filter(category = fetch_category)
    else:
       all_books = BookModel.objects.all()

    return render(request,'home.html',{
        'all_categories':all_categories,
        'filtered_books': filtered_books,
        'all_books': all_books,
        })