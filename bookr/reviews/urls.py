from django.contrib import admin
from django.urls import path
from . import views
import reviews.views

urlpatterns = [
    path('', views.index, name='Welcome'),
    path('books/<int:id>/', views.book, name='View Book'),
    path('books/', views.book_list, name='Books List'),
    path('book-search', reviews.views.book_search)
]
