from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class category_model(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.category_name}"
    


class BookModel(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    images = models.ImageField(upload_to="media_file", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(category_model,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    
class ReviewModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review
    


class BorrowModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True) 
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username +" "+ self.book.title}" 

