import random
from datetime import datetime

from django.contrib import auth


def read():
    from reviews.models import Book, Contributor, Publisher, BookContributor, Review
    Book.objects.all().delete()
    Contributor.objects.all().delete()
    Publisher.objects.all().delete()
    BookContributor.objects.all().delete()
    Review.objects.all().delete()
    auth.get_user_model().objects.all().delete()

    file1 = open('WebDevWithDjangoData.csv', 'r')
    lines = file1.readlines()
    start = -1
    table_name = ''
    for line in lines:
        line = line.strip(",\n")

        if 'content:' in line:
            table_name = line.split(",")[0].split(":")[1]
            print(table_name)
            start = 0
        elif start == 0:
            fields = line.split(',')
            start = 1
        elif start == 1 and line != "":
            data = line.split(',')
            insert_data(table_name, data)

    file1.close()


def insert_data(table, data):
    from datetime import date
    from reviews.models import Book, Contributor, Publisher, BookContributor, Review
    if table == "Publisher":
        publisher = Publisher.objects.create(name=data[0], website=data[1], email=data[2])
    elif table == "Book":
        publisher = Publisher.objects.get(name=data[3])
        datetime1 = datetime.strptime(data[1], '%Y/%m/%d')
        book = Book.objects.create(title=data[0], publication_date=datetime1, isbn=data[2],
                                   publisher=publisher)
    elif table == "Contributor":
        contributor = Contributor.objects.create(first_names=data[0], last_names=data[1],
                                                 email=data[2])
    elif table == "BookContributor":
        book = Book.objects.get(title=data[0])
        contributor = Contributor.objects.get(email=data[1])
        book_contributor = BookContributor(book=book, contributor=contributor, role=data[2])
        book_contributor.save()
    elif table == "Review":
        user_id = random.randint(1, 100)
        book = Book.objects.get(title=data[5])
        datetime1 = datetime.strptime(data[2], '%Y-%m-%d %H:%M:%S.%f')
        datetime2 = datetime.strptime(data[3], '%Y-%m-%d %H:%M:%S.%f')
        user = auth.get_user_model().objects.create_user(email=data[4], username=user_id)
        review = Review.objects.create(content=data[0], rating=data[1], date_created=datetime1,
                                       date_edited=datetime2, creator=user, book=book)
        print(user_id)
        print(review.date_created)

