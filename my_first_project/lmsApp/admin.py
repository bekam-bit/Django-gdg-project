from django.contrib import admin
from .models import Author, Book, Category, Loan, Member
from .orm_queries import (
    books_with_loan_count,
    categories_with_book_count,
    filtered_books,
    members_with_active_loans,
    never_loaned_books,
)
from django.db.models import Q

# Register your models here.
class AvailbilityFilter(admin.SimpleListFilter):
    title="Availability"
    parameter_name="availability"

    def lookups(self, request, model_admin):
        return(
            ("available","Available"),
            ("not_available","Not Available"),
            )
    
    def queryset(self, request, queryset):
        if self.value()=="available":
            return queryset.filter(available_copies__gt=0)
        if self.value()=="not_available":
            return queryset.filter(available_copies__lte=0)
        return queryset


class AuthorFilter(admin.SimpleListFilter):
    title = "Author"
    parameter_name = "author"

    def lookups(self, request, model_admin):
        return [(author.pk, author.author_name) for author in Author.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(author_id=self.value())
        return queryset


class NeverLoanedFilter(admin.SimpleListFilter):
    title = "Loan status"
    parameter_name = "loan_status"

    def lookups(self, request, model_admin):
        return (
            ("never", "Never loaned"),
        )

    def queryset(self, request, queryset):
        if self.value() == "never":
            return never_loaned_books(queryset)
        return queryset


class AuthorCategoryFilter(admin.SimpleListFilter):
    title = "Author + Category"
    parameter_name = "author_category"

    def lookups(self, request, model_admin):
        pairs = Book.objects.values_list(
            "author_id",
            "author__author_name",
            "category__category_id",
            "category__category_name",
        ).distinct()
        return [
            (f"{author_id}:{category_id}", f"{author_name} / {category_name}")
            for author_id, author_name, category_id, category_name in pairs
        ]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        try:
            author_id, category_id = self.value().split(":", 1)
        except ValueError:
            return queryset
        author = Author.objects.filter(pk=author_id).first()
        category = Category.objects.filter(pk=category_id).first()
        if not author or not category:
            return queryset
        return filtered_books(
            queryset,
            category.category_name,
            author.author_name,
        )

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=('title','author','available_copies','loan_count')
    list_filter=(AuthorFilter,'category',AuthorCategoryFilter,AvailbilityFilter,NeverLoanedFilter)
    search_fields=('title','ISBN')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return books_with_loan_count(queryset)

    @admin.display(ordering='loan_count', description='Loans')
    def loan_count(self, obj):
        return obj.loan_count


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("author_name", "author_email")
    search_fields = ("author_name", "author_email")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "book_count")
    search_fields = ("category_name",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return categories_with_book_count(queryset)

    @admin.display(ordering='book_count', description='Books')
    def book_count(self, obj):
        return obj.book_count


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("member_name", "email", "joined_date", "active_loans")
    search_fields = ("member_name", "email")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return members_with_active_loans(queryset)

    @admin.display(ordering='active_loans', description='Active loans')
    def active_loans(self, obj):
        return obj.active_loans


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("book", "member", "loan_date", "return_date", "returned")
    list_filter = ("returned", "loan_date")