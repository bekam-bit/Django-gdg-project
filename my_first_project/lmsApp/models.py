from django.db import models
from django.utils import timezone

# Create your models here.
class Author(models.Model):
    author_id=models.AutoField(primary_key=True)
    author_name=models.CharField(max_length=150)
    author_email=models.EmailField(max_length=100)
    author_bio=models.TextField(blank=True,null=True)

    def __str__(self):
        return self.author_name

class Category(models.Model):
    category_id=models.AutoField(primary_key=True)
    category_name=models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    
class Book(models.Model):
    book_id=models.AutoField(primary_key=True)
    ISBN=models.CharField(max_length=50)
    title=models.CharField(max_length=200)
    total_copies=models.IntegerField()
    available_copies=models.IntegerField(null=True, blank=True)
    publication_date=models.DateField()
    author=models.ForeignKey(Author,on_delete=models.CASCADE,related_name='books')
    category=models.ManyToManyField(Category,related_name='books')

    def __str__(self):
        return self.title
    
    @property
    def is_available(self):
        return self.available_copies>0
    
    def save(self,*args,**kwargs):
        if self.pk:
            active_loans=self.loans.filter(returned=False).count()
            self.available_copies=max(self.total_copies-active_loans,0)
        elif self.available_copies is None:
            self.available_copies=self.total_copies
        super().save(*args,**kwargs)

class Member(models.Model):
    member_id=models.AutoField(primary_key=True)
    member_name=models.CharField(max_length=150)
    email=models.EmailField(max_length=100)
    joined_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.member_name}"

class Loan(models.Model):
    loan_id=models.AutoField(primary_key=True)
    loan_date=models.DateField(default=timezone.now)
    return_date=models.DateField(null=True,blank=True)
    book=models.ForeignKey(Book,on_delete=models.PROTECT,related_name='loans')
    member=models.ForeignKey(Member,on_delete=models.PROTECT,related_name='loans')
    returned=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} loaned to {self.member.member_name}"
    
    @property
    def is_overdue(self):
        if self.returned:
            return False
        if self.return_date and self.return_date<timezone.now().date():
            return True
        return False
    
