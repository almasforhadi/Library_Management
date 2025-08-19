
from django.urls import path
from . import views

urlpatterns = [
    path('details/reviews/<int:book_id>', views.review, name='review'),
    path('details/<int:id>', views.details, name='details'),
    path('details/borrow/<int:id>', views.borrow, name='borrow'),
    path('details/return_book/<int:id>', views.return_book, name='return_book'),
]