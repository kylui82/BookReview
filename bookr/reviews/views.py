import utils
from django.shortcuts import render
from .models import *
from .utils import *
# import get_object_or_404()
from django.shortcuts import get_object_or_404


def index(request):
    return render(request, "base.html")


def book_search(request):
    search = request.GET.get('search')
    return render(request, "search-results.html", {"search_text": search})


def book_list(request):
    books = Book.objects.all()
    books_list = []
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        books_list.append({'book': book, 'book_rating': book_rating, 'number_of_reviews': number_of_reviews})
    context = {'book_list': books_list}
    # return render(request, 'books_list.html', context)
    return render(request, 'base_extended.html', context)


def book(request, id):
    book = get_object_or_404(Book, pk=id)
    reviews = book.review_set.all()

    if reviews:
        book_rating = average_rating([review.rating for review in reviews])
    else:
        book_rating = None
    context = {'book': book, 'book_rating': book_rating,'reviews':reviews}
    # return render(request, 'books_list.html', context)
    return render(request, 'book.html', context)
