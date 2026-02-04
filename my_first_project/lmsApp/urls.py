from django.urls import path
from . import bookViews,authorViews

urlpatterns=[
    path('',bookViews.home,name='home'),
    path('authors/',authorViews.author_list,name='author_list'),
    path('authors/<int:author_id>',authorViews.author_details,name='author_details'),
    path('books/',bookViews.book_list,name='book_list'),
    path('books/<int:book_id>',bookViews.book_details,name='book_detail'),
    path('books/add',bookViews.AddBook,name="book_add"),
    path('books/update/<int:book_id>',bookViews.UpdateBook,name="book_update"),
    path('books/delete/<int:book_id>',bookViews.DeleteBook,name="book_delete"),
    path('books/<int:book_id>/<int:member_id>/loan/',bookViews.loanMgtView.as_view(),name='loanMgt'),
]