from rest_framework import serializers
from .models import Book,Loan,Author

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields='__all__'
        read_only_fields=['ISBN','available_copies']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model=Loan
        fields='__all__'
        read_only_fields=['loan_id','loan_date']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields='__all__'
        