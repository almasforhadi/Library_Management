from django.contrib import admin
from .models import category_model, BookModel, BorrowModel, ReviewModel

# Register your models here.
# admin.site.register(category_model)
admin.site.register(BookModel)
admin.site.register(BorrowModel)
admin.site.register(ReviewModel)

class category_admin(admin.ModelAdmin):
     prepopulated_fields = {
          'slug' : ('category_name',)
     }
     list_display = ['category_name', 'slug' ]

admin.site.register(category_model, category_admin)
