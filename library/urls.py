
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('account_app.urls')),
    path('transactions/', include('transaction_app.urls')),
    path('books/', include('book_app.urls')),
    path('category/<slug:category_slug>/', views.home, name='category_name'),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)