from django.db.models import Count, Q


def books_with_loan_count(queryset):
    return queryset.annotate(loan_count=Count('loans'))


def never_loaned_books(queryset):
    return queryset.filter(loans=None)


def filtered_books(queryset, category_name, author_name):
    return queryset.filter(
        category__category_name=category_name,
        author__author_name=author_name,
    ).distinct()


def members_with_active_loans(queryset):
    return queryset.annotate(active_loans=Count('loans', filter=Q(loans__returned=False)))


def categories_with_book_count(queryset):
    return queryset.annotate(book_count=Count('books'))